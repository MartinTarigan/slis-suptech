from __future__ import annotations

import csv
from datetime import datetime
from typing import IO, Dict, Any, Tuple, List

import pandas as pd
from sqlalchemy.orm import Session

from slis.models import SanctionSource, SanctionSnapshot, SanctionEntity
import re


def normalize_name(name: str | None) -> str | None:
    if not name:
        return None
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name or None


def parse_dob(dob_str: str | None) -> Tuple[int | None, int | None, int | None]:
    """
    Parser DOB yang Robust untuk Import Data ke Database.
    Output: (Year, Month, Day) sebagai integer.
    
    Capabilities:
    1. Menangani nama bulan Indonesia (Juli -> 7, Mei -> 5).
    2. Menangani nama bulan Inggris (July -> 7).
    3. Mendeteksi format YYYY-MM-DD (ISO) dan DD-MM-YYYY (Indo/UK).
    4. Mendeteksi tahun saja.
    """
    if not dob_str or not dob_str.strip():
        return None, None, None

    # 1. Lowercase dan bersihkan whitespace
    s = dob_str.lower().strip()

    # 2. Dictionary Mapping Bulan (Nama -> Angka String)
    month_map = {
        # Indonesia
        'januari': '01', 'februari': '02', 'maret': '03', 'april': '04',
        'mei': '05', 'juni': '06', 'juli': '07', 'agustus': '08',
        'september': '09', 'oktober': '10', 'november': '11', 'desember': '12',
        # Inggris Full
        'january': '01', 'february': '02', 'march': '03', 'may': '05',
        'june': '06', 'july': '07', 'august': '08', 'october': '10', 'december': '12',
        # Singkatan (3 huruf)
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'jun': '06',
        'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }

    # 3. Ganti nama bulan dengan angka di dalam string
    for name, digit in month_map.items():
        if name in s:
            s = s.replace(name, digit)

    # 4. Split berdasarkan delimiter umum (spasi, strip, slash, titik, koma)
    parts_raw = re.split(r'[-/.\s,]+', s)
    # Filter hanya yang angka
    parts = [int(p) for p in parts_raw if p.isdigit()]

    year, month, day = None, None, None

    # 5. Logika Penentuan Posisi (Heuristic)
    if len(parts) == 3:
        p1, p2, p3 = parts[0], parts[1], parts[2]
        
        # Format A: YYYY-MM-DD (ISO) -> 1996 07 30
        if p1 > 1000:
            year, month, day = p1, p2, p3
            
        # Format B: DD-MM-YYYY (Indo/UK) -> 30 07 1996
        elif p3 > 1000:
            year = p3
            
            # Cek ambiguitas (MM-DD vs DD-MM)
            # Jika angka tengah > 12, pasti itu hari (MM-DD-YYYY style US)
            if p2 > 12:
                month, day = p1, p2
            else:
                # Default assume DD-MM (Indo/UK)
                day, month = p1, p2

    elif len(parts) == 1:
        # Cuma ada 1 angka, cek apakah tahun
        if parts[0] > 1000 and parts[0] < 2100:
            year = parts[0]

    # 6. Validasi Logika Kalender
    # Pastikan month 1-12, day 1-31. Jika tidak valid, reset ke None agar tidak error saat insert DB.
    if month and (month < 1 or month > 12):
        month = None
    if day and (day < 1 or day > 31):
        day = None
        
    return year, month, day


def _load_sanction_file_to_df(file_obj: IO[bytes], filename: str) -> pd.DataFrame:
    """
    Load CSV/XLSX ke DataFrame (semua kolom string).
    """
    name_lower = filename.lower()
    file_obj.seek(0)

    if name_lower.endswith(".csv"):
        df = pd.read_csv(file_obj, dtype=str).fillna("")
    elif name_lower.endswith(".xlsx") or name_lower.endswith(".xls"):
        df = pd.read_excel(file_obj, dtype=str).fillna("")
    else:
        raise ValueError("Unsupported sanction file format. Use CSV or Excel.")
    return df


def import_sanction_file(
    db: Session,
    source_code: str,
    file_obj,
    filename: str,
    version_label: str | None = None,
    effective_date: datetime | None = None,
) -> Tuple[SanctionSnapshot, int]:
    """
    Import 1 file sanction list ke:
      - sanction_snapshot
      - sanction_entity

    Menggunakan mapping dari sanction_source.column_mapping.
    """
    
    source: SanctionSource | None = (
        db.query(SanctionSource)
        .filter(SanctionSource.code == source_code)
        .one_or_none()
    )
    if source is None:
        raise ValueError(f"sanction_source with code '{source_code}' not found")

    mapping: Dict[str, Any] = source.column_mapping or {}
    col_full_name = mapping.get("full_name")
    col_dob = mapping.get("dob")
    col_citizenship = mapping.get("citizenship")
    col_country_of_res = mapping.get("country_of_residence")
    col_country_of_birth = mapping.get("country_of_birth")

    if not col_full_name:
        raise ValueError(
            "column_mapping.full_name is required for this source to import"
        )

    df = _load_sanction_file_to_df(file_obj, filename)

    if col_full_name not in df.columns:
        raise ValueError(
            f"Expected full_name column '{col_full_name}' not found in file. "
            f"Columns available: {list(df.columns)}"
        )

    
    snapshot = SanctionSnapshot(
        source_id=source.id,
        version_label=version_label or filename,
        effective_date=effective_date.date() if isinstance(effective_date, datetime) else None,
        record_count=len(df),
        is_active=True,
        raw_file_name=filename,
    )
    db.add(snapshot)
    db.flush()

    
    used_cols = {
    c
    for c in [
        col_full_name,
        col_dob,
        col_citizenship,
        col_country_of_res,
        col_country_of_birth,
    ]
    if c
}

    entities: List[SanctionEntity] = []

    for _, row in df.iterrows():
        
        full_name_raw = str(row[col_full_name]).strip() if col_full_name in df.columns else ""
        if not full_name_raw:
            continue  

        dob_raw = str(row[col_dob]).strip() if col_dob and col_dob in df.columns else ""
        citizenship_raw = (
            str(row[col_citizenship]).strip()
            if col_citizenship and col_citizenship in df.columns
            else ""
        )
        country_res_raw = (
            str(row[col_country_of_res]).strip()
            if col_country_of_res and col_country_of_res in df.columns
            else ""
        )
        country_birth_raw = (
            str(row[col_country_of_birth]).strip()
            if col_country_of_birth and col_country_of_birth in df.columns
            else ""
        )

        dob_year, dob_month, dob_day = parse_dob(dob_raw if dob_raw else None)

        row_dict = {c: (str(row[c]) if c in row and row[c] != "" else None) for c in df.columns}
        extra_data = {k: v for k, v in row_dict.items() if k not in used_cols}

        ent = SanctionEntity(
            source_id=source.id,
            snapshot_id=snapshot.id,
            external_id=None,
            primary_name=full_name_raw,
            primary_name_normalized=normalize_name(full_name_raw),
            date_of_birth_raw=dob_raw or None,
            dob_year=dob_year,
            dob_month=dob_month,
            dob_day=dob_day,
            citizenship=citizenship_raw or None,
            citizenship_normalized=normalize_name(citizenship_raw) if citizenship_raw else None,
            country_of_residence=country_res_raw or None,
            country_of_birth=country_birth_raw or None,
            extra_data=extra_data,
            is_active=True,
        )
        entities.append(ent)

    if entities:
        db.bulk_save_objects(entities)

    snapshot.record_count = len(entities)
    db.commit()
    db.refresh(snapshot)

    return snapshot, len(entities)
