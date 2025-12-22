from celery import Celery
from config import Config

# INI INSTANCE CELERY YANG DIPAKAI SEMUA
celery_app = Celery(
    "slis",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
    include=["slis.tasks.db_job"]
)

# (opsional) set queue default
celery_app.conf.task_default_queue = "default"


@celery_app.task(name="slis.run_screening_task")
def run_screening_task(job_id: int) -> None:
    """
    Celery task untuk menjalankan screening berdasarkan satu ScreeningJob.

    - Cuma terima job_id
    - Transaksi + sanction di-load dari database di dalam service
    """
    from slis.db import SessionLocal
    from slis.services.screening import run_screening_for_job

    db = SessionLocal()
    try:
        run_screening_for_job(db=db, job_id=job_id)
    finally:
        db.close()
