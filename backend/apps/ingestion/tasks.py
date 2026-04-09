from celery import shared_task

from .models import UploadSession
from .services import run_ingestion_pipeline


@shared_task(name='ingestion.run_upload_pipeline')
def run_upload_pipeline(session_id: int):
    session = UploadSession.objects.select_related('book').get(pk=session_id)
    run_ingestion_pipeline(session)
    return session.status
