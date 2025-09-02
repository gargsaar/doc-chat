from celery import shared_task
from typing import Any

from app.web.db.models import Pdf
from app.web.files import download
from app.chat.create_embeddings import create_embeddings_for_pdf


@shared_task()
def process_document(pdf_id: str) -> Any:  # Changed from int to str to match UUID
    print(f"=== PROCESS_DOCUMENT CALLED FOR PDF ID: {pdf_id} ===")
    pdf = Pdf.find_by(id=pdf_id)
    
    if not pdf:
        print(f"ERROR: PDF with ID {pdf_id} not found in database")
        return
    
    print(f"Found PDF record: {pdf.name} for user: {pdf.user_id}")
    
    try:
        with download(pdf.id) as pdf_path:
            print(f"Downloaded PDF to temporary path: {pdf_path}")
            # Pass user_id for database-level isolation
            create_embeddings_for_pdf(pdf.id, pdf_path, user_id=str(pdf.user_id))
    except Exception as e:
        print(f"ERROR in process_document for PDF {pdf_id}: {str(e)}")
        raise
