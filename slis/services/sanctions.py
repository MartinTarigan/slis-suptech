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
    Versi simple parser DOB:
    - support YYYY
    - YYYY-MM-DD
    - DD-MM-YYYY
    - format lain basic
    """
    if dob_str is None:
        return None, None, None

    s = dob_str.strip()
    if not s:
        return None, None, None

    
    fmts = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%Y",
    ]
    for fmt in fmts:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.year, dt.month, dt.day
        except ValueError:
            continue

    
    import re as _re

    m = _re.search(r"\b(19\d{2}|20\d{2})\b", s)
    if m:
        year = int(m.group(1))
        return year, None, None

    return None, None, None


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
