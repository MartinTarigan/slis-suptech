from slis import create_app
from slis.celery_app import celery_app as celery, init_celery


# Buat app Flask dan integrasikan dengan Celery
flask_app = create_app()
init_celery(flask_app)

from slis.tasks import run_screening_task


@celery.task
def ping():
    """
    Task uji coba.
    Nanti kita ganti/extend dengan task screening.
    """
    return "pong from Celery"
