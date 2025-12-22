from __future__ import annotations

from datetime import date, datetime, timezone
from typing import List, Optional

import logging
import jellyfish
import re

import os

from typing import List, Dict, Any, Optional

from slis.matching.geo import generate_geographic_insights

DEV_FAST_MODE = os.getenv("SLIS_DEV_FAST_MODE", "1") == "1"
DEV_MAX_TRANSACTIONS = int(os.getenv("SLIS_DEV_MAX_TRANSACTIONS", "20"))
DEV_MAX_SANCTIONS = int(os.getenv("SLIS_DEV_MAX_SANCTIONS", "200"))


from slis.models import (
    ScreeningJob,
    ScreeningResult,
    Transaction,
    SanctionEntity,
)

from slis.matching.dob import calculate_dob_score_flexible


logger = logging.getLogger(__name__)


def _normalize_name(name: Optional[str]) -> str:
    """Normalisasi nama: lowercase, buang simbol, rapikan spasi."""
    if not name:
        return ""
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    return " ".join(s.split())

def _normalize_country(value: Optional[str]) -> str:
    """Normalisasi citizenship/country (ID, Indonesia -> id / indonesia)."""
    if not value:
        return ""
    s = str(value).lower()
    s = re.sub(r"[^a-z0-9]", "", s)
    return s


def _parse_dob(value: Optional[str]) -> Optional[date]:
    """Parse string tanggal lahir ke date, beberapa format umum."""
    if not value:
        return None
    if isinstance(value, date):
        return value
    s = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def get_transaction_name(tx: Transaction, role: str = "sender") -> str:
    """
    Ambil nama pengirim/penerima dari berbagai kemungkinan field.

    role = "sender" atau "receiver"
    """
    if role == "sender":
        candidates = [
            getattr(tx, "sender_name", None),
            getattr(tx, "sender_name_normalized", None),
            getattr(tx, "nama_pengirim", None),
        ]
    else:
        candidates = [
            getattr(tx, "receiver_name", None),
            getattr(tx, "receiver_name_normalized", None),
            getattr(tx, "nama_penerima", None),
        ]

    for val in candidates:
        if val:
            return str(val)
    return ""


def get_sanction_name(s: SanctionEntity) -> str:
    """
    Ambil nama sanksi dari berbagai kemungkinan field.
    """
    candidates = [
        getattr(s, "primary_name", None),
        getattr(s, "full_name", None),
        getattr(s, "name", None),
    ]
    for val in candidates:
        if val:
            return str(val)
    return ""


def compute_name_score(name1: str | None, name2: str | None) -> float:
    """Skor nama pakai Jaro-Winkler (0–100)."""
    if not name1 or not name2:
        return 0.0
    n1 = _normalize_name(name1)
    n2 = _normalize_name(name2)
    if not n1 or not n2:
        return 0.0
    return float(jellyfish.jaro_winkler_similarity(n1, n2) * 100.0)

def combine_scores(
    name_score: float,
    dob_score: float,
    citizenship_score: float,
    has_dob: bool,
    has_citizenship: bool,
) -> tuple[float, str]:
    if has_dob and has_citizenship:
        final = 0.5 * name_score + 0.3 * dob_score + 0.2 * citizenship_score
        scheme = "NAME_DOB_CITIZENSHIP"
    elif has_dob:
        final = 0.7 * name_score + 0.3 * dob_score
        scheme = "NAME_DOB"
    elif has_citizenship:
        final = 0.7 * name_score + 0.3 * citizenship_score
        scheme = "NAME_CITIZENSHIP"
    else:
        final = name_score
        scheme = "NAME_ONLY"
    return final, scheme

def _match_single_entity(
    query_data: Dict[str, Any], 
    sanction_data: Dict[str, Any], 
    thresholds: Dict[str, float]
) -> Optional[Dict[str, Any]]:
    """
    Helper function untuk membandingkan satu query dengan satu entitas sanksi.
    Menangani logika skor Nama, DOB, Citizenship, dan Geo Insights.
    """
    name_score = compute_name_score(query_data["name_norm"], sanction_data["name_norm"])
    if name_score < thresholds["name"]:
        return None

    dob_score = 0.0
    has_dob = False
    dob_match_desc = None
    
    q_dob = query_data.get("dob")
    s_dob = sanction_data.get("dob_raw")
    
    if q_dob and s_dob:
        q_dob_str = str(q_dob) if isinstance(q_dob, date) else q_dob
        score, desc = calculate_dob_score_flexible(q_dob_str, s_dob, sanction_data.get("source"))
        dob_score = float(score)
        dob_match_desc = desc
        has_dob = True

    cit_score = 0.0
    has_cit = False
    q_cit = query_data.get("cit_norm")
    s_cit = sanction_data.get("cit_norm")
    
    if q_cit and s_cit:
        if q_cit == s_cit:
            cit_score = 100.0
        has_cit = True

    final_score, scheme = combine_scores(name_score, dob_score, cit_score, has_dob, has_cit)
    if final_score < thresholds["final"]:
        return None

    geo_insights = []
    q_cit_raw = query_data.get("cit_raw")
    if q_cit_raw:
        cust_geo = {"Citizenship": q_cit_raw, "Country_of_Residence": None, "Place_of_Birth": None}
        sanc_geo = {"Citizenship": sanction_data.get("cit_raw")}
        geo_insights = generate_geographic_insights(cust_geo, sanc_geo)

    return {
        "sanction_id": sanction_data["id"],
        "sanction_name": sanction_data["name"],
        "sanction_source": sanction_data["source"],
        "sanction_dob": s_dob,
        "sanction_citizenship": sanction_data.get("cit_raw"),
        "name_score": round(name_score, 2),
        "dob_score": round(dob_score, 2),
        "citizenship_score": round(cit_score, 2),
        "final_score": round(final_score, 2),
        "scheme": scheme,
        "match_details": dob_match_desc,
        "geographic_insights": geo_insights
    }


# Engine utama 
def run_screening_for_job(db, job_id: int) -> None:
    job: ScreeningJob | None = db.query(ScreeningJob).get(job_id)
    if not job:
        logger.error("ScreeningJob %s tidak ditemukan", job_id)
        return

    logger.info("Mulai screening job_id=%s, batch_id=%s", job.id, job.batch_id)
    job.status = "RUNNING"
    job.finished_at = None
    db.add(job)
    db.commit()

    try:
        tx_query = db.query(Transaction).filter(Transaction.batch_id == job.batch_id)
        if DEV_FAST_MODE:
            tx_query = tx_query.limit(DEV_MAX_TRANSACTIONS)
        txs: List[Transaction] = tx_query.all()
        
        sanctions_query = db.query(SanctionEntity).filter(SanctionEntity.is_active.is_(True))
        if DEV_FAST_MODE:
            sanctions_query = sanctions_query.limit(DEV_MAX_SANCTIONS)
        sanctions: List[SanctionEntity] = sanctions_query.all()

        raw_sanction_count = len(sanctions)
        job.total_transactions = len(txs)
        
        if not txs or not sanctions:
            job.total_sanctions = raw_sanction_count
            job.status = "DONE"
            job.total_matches = 0
            job.finished_at = datetime.now(timezone.utc)
            db.add(job)
            db.commit()
            return

        thresholds = {
            "name": job.threshold_name_score or 70.0,
            "final": job.threshold_score or 60.0
        }

        # OPTIMASI DEDUPLIKASI
        unique_sanction_map = {} 
        for s in sanctions:
            sanction_name = get_sanction_name(s)
            if not sanction_name: continue
            
            norm_name = _normalize_name(sanction_name)
            
            if norm_name not in unique_sanction_map:
                unique_sanction_map[norm_name] = {
                    "id": s.id,
                    "source_id": s.source_id,
                    "name": sanction_name,
                    "name_norm": norm_name,
                    "dob_raw": s.date_of_birth_raw,
                    "cit_raw": s.citizenship,
                    "cit_norm": _normalize_country(s.citizenship),
                    "source": s.source.code if s.source else "UNKNOWN"
                }

        sanction_list_data = list(unique_sanction_map.values())
        
        job.total_sanctions = len(sanction_list_data)
        db.add(job)
        db.commit()

        logger.info(f"Deduplikasi Sanksi: {raw_sanction_count} raw -> {len(sanction_list_data)} unique.")

        results_to_insert: List[ScreeningResult] = []

        for tx in txs:
            parties = [
                ("sender", get_transaction_name(tx, "sender")),
                ("receiver", get_transaction_name(tx, "receiver"))
            ]

            for role, party_name in parties:
                if not party_name: continue
                
                query_data = {
                    "name_norm": _normalize_name(party_name),
                    "dob": None,
                    "cit_raw": None,
                    "cit_norm": None
                }

                # Loop hanya ke data sanksi yang SUDAH UNIK
                for s_data in sanction_list_data:
                    match = _match_single_entity(query_data, s_data, thresholds)
                    if match:
                        res = ScreeningResult(
                            job_id=job.id,
                            transaction_id=tx.id,
                            sanction_entity_id=match["sanction_id"],
                            sanction_source_id=match["sanction_id"], 
                            target_role=role,
                            name_score=match["name_score"],
                            dob_score=match["dob_score"],
                            citizenship_score=match["citizenship_score"],
                            final_score=match["final_score"],
                            geographic_insights=match["geographic_insights"]
                        )
                        results_to_insert.append(res)

            # Flush Batch Insert
            if len(results_to_insert) >= 1000:
                db.bulk_save_objects(results_to_insert)
                db.commit()
                logger.info("Flushed 1000 screening results ke DB")
                results_to_insert.clear()

        # Final Flush
        if results_to_insert:
            db.bulk_save_objects(results_to_insert)
            db.commit()

        # Summary
        total_matches = db.query(ScreeningResult).filter(ScreeningResult.job_id == job.id).count()
        job.total_matches = total_matches
        job.status = "DONE"
        job.finished_at = datetime.now(timezone.utc)
        db.add(job)
        db.commit()

        logger.info(f"Job {job.id} selesai: total_matches={total_matches}")

    except Exception:
        logger.exception("Error saat menjalankan screening job_id=%s", job_id)
        db.rollback()
        job = db.get(ScreeningJob, job_id)
        if job:
            job.status = "FAILED"
            job.error_message = "Internal error saat screening (lihat log backend)."
            db.commit()


def search_single_entity(
    db, name: str, dob: Optional[str] = None, citizenship: Optional[str] = None,
    limit: int = 50, name_threshold: float = 40.0, final_threshold: float = 50.0,
) -> list[dict]:
    
    query_name = (name or "").strip()
    if not query_name: return []

    sanctions = db.query(SanctionEntity).filter(SanctionEntity.is_active.is_(True)).all()
    if not sanctions: return []

    # Optimasi Deduplikasi
    unique_sanction_map = {}
    for s in sanctions:
        s_name = get_sanction_name(s)
        if not s_name: continue
        norm = _normalize_name(s_name)
        if norm not in unique_sanction_map:
            unique_sanction_map[norm] = {
                "id": s.id,
                "name": s_name,
                "name_norm": norm,
                "dob_raw": s.date_of_birth_raw,
                "cit_raw": s.citizenship,
                "cit_norm": _normalize_country(s.citizenship),
                "source": s.source.code if s.source else "UNKNOWN"
            }
            
    sanction_list_data = list(unique_sanction_map.values())

    query_data = {
        "name_norm": _normalize_name(query_name),
        "dob": _parse_dob(dob) if dob else None,
        "cit_raw": citizenship,
        "cit_norm": _normalize_country(citizenship) if citizenship else ""
    }
    
    thresholds = {"name": name_threshold, "final": final_threshold}
    matches = []

    for s_data in sanction_list_data:
        match = _match_single_entity(query_data, s_data, thresholds)
        if match:
            matches.append(match)

    matches.sort(key=lambda m: m["final_score"], reverse=True)
    return matches[:limit]

def search_entities_bulk(
    db, queries: List[Dict[str, Any]], limit: int = 20,
    name_threshold: float = 60.0, final_threshold: float = 60.0,
) -> List[Dict[str, Any]]:
    
    if not queries: return []

    # Optimasi Deduplikasi
    sanctions_orm = db.query(SanctionEntity).filter(SanctionEntity.is_active.is_(True)).all()
    unique_sanction_map = {}
    
    for s in sanctions_orm:
        s_name = s.primary_name_normalized or _normalize_name(s.primary_name)
        if s_name not in unique_sanction_map:
            unique_sanction_map[s_name] = {
                "id": s.id,
                "name": s.primary_name,
                "name_norm": s_name,
                "dob_raw": s.date_of_birth_raw,
                "cit_raw": s.citizenship,
                "cit_norm": _normalize_country(s.citizenship),
                "source": s.source.code if s.source else "UNKNOWN"
            }
            
    sanction_list_data = list(unique_sanction_map.values())

    thresholds = {"name": name_threshold, "final": final_threshold}
    bulk_results = []

    for q in queries:
        req_id = q.get("id")
        req_name = q.get("name", "")
        
        if not req_name:
            bulk_results.append({"request_id": req_id, "matches": [], "error": "Name required"})
            continue

        query_data = {
            "name_norm": _normalize_name(req_name),
            "dob": q.get("dob"),
            "cit_raw": q.get("citizenship"),
            "cit_norm": _normalize_country(q.get("citizenship"))
        }
        
        matches = []
        for s_data in sanction_list_data:
            match = _match_single_entity(query_data, s_data, thresholds)
            if match:
                matches.append(match)

        matches.sort(key=lambda x: x["final_score"], reverse=True)
        
        bulk_results.append({
            "request_id": req_id,
            "query_data": q,
            "matches": matches[:limit],
            "match_count": len(matches)
        })

    return bulk_results