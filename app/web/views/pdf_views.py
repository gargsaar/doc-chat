import os
from flask import Blueprint, g, jsonify
from werkzeug.exceptions import Unauthorized
from app.web.hooks import login_required, handle_file_upload, load_model
from app.web.db.models import Pdf
from app.web.db.models.conversation import Conversation
from app.web.db.models.message import Message
from app.web.db import db
from app.web.tasks.embeddings import process_document  # type: ignore
from app.web import files
from app.chat.create_embeddings import delete_embeddings_for_pdf

bp = Blueprint("pdf", __name__, url_prefix="/api/pdfs")


@bp.route("/", methods=["GET"])
@login_required
def list():
    pdfs = Pdf.query.filter_by(user_id=g.user.id).order_by(Pdf.created_on.desc()).all()

    return Pdf.as_dicts(pdfs)


@bp.route("/", methods=["POST"])
@login_required
@handle_file_upload
def upload_file(file_id, file_path, file_name):
    # First ensure the file is properly saved and readable
    if not os.path.exists(file_path):
        return {"error": "File was not properly uploaded"}, 500
    
    # Check if file is a valid PDF by trying to read a few bytes
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
            if not header.startswith(b'%PDF-'):
                return {"error": "File is not a valid PDF"}, 400
    except Exception as e:
        return {"error": f"Error validating PDF file: {str(e)}"}, 500
    
    res, status_code = files.upload(file_path, file_id)
    if status_code >= 400:
        return res, status_code

    pdf = Pdf.create(id=file_id, name=file_name, user_id=g.user.id)

    # TODO: Defer this to be processed by the worker
    try:
        process_document.delay(pdf.id)
    except Exception as e:
        # Log the error but don't fail the upload
        print(f"Error processing document {pdf.id}: {str(e)}")
        # You might want to set a status field on the PDF to indicate processing failed

    return pdf.as_dict()


@bp.route("/<string:pdf_id>", methods=["GET"])
@login_required
@load_model(Pdf)
def show(pdf):
    return jsonify(
        {
            "pdf": pdf.as_dict(),
            "download_url": files.create_download_url(pdf.id),
        }
    )


@bp.route("/<string:pdf_id>", methods=["DELETE"])
@login_required
@load_model(Pdf)
def delete(pdf):
    """Delete a PDF document, its file, embeddings, and database record"""
    try:
        # Ensure the user owns this PDF
        if pdf.user_id != g.user.id:
            return {"error": "Unauthorized"}, 403
        
        pdf_id = pdf.id
        user_id = str(pdf.user_id)
        
        print(f"Starting deletion process for PDF {pdf_id}")
        
        # 1. Delete related conversations and messages first (cascade deletion)
        try:
            # Find all conversations for this PDF
            conversations = Conversation.query.filter_by(pdf_id=pdf_id).all()
            print(f"Found {len(conversations)} conversations to delete")
            
            for conversation in conversations:
                # Delete all messages in this conversation
                messages = Message.query.filter_by(conversation_id=conversation.id).all()
                print(f"Deleting {len(messages)} messages from conversation {conversation.id}")
                for message in messages:
                    db.session.delete(message)
                
                # Delete the conversation
                db.session.delete(conversation)
            
            # Commit the conversation and message deletions
            db.session.commit()
            print(f"Successfully deleted conversations and messages for PDF {pdf_id}")
            
        except Exception as e:
            print(f"Warning: Could not delete conversations for PDF {pdf_id}: {str(e)}")
            db.session.rollback()
            # Continue with deletion even if conversation deletion fails
        
        # 2. Delete embeddings from ChromaDB
        try:
            delete_embeddings_for_pdf(pdf_id, user_id)
            print(f"Successfully deleted embeddings for PDF {pdf_id}")
        except Exception as e:
            print(f"Warning: Could not delete embeddings for PDF {pdf_id}: {str(e)}")
            # Continue with deletion even if embeddings deletion fails
        
        # 3. Delete file from uploads
        try:
            res, status_code = files.delete(pdf_id)
            if status_code >= 400:
                print(f"Warning: Could not delete file for PDF {pdf_id}: {res}")
                # Continue with deletion even if file deletion fails
            else:
                print(f"Successfully deleted file for PDF {pdf_id}")
        except Exception as e:
            print(f"Warning: Could not delete file for PDF {pdf_id}: {str(e)}")
            # Continue with deletion even if file deletion fails
        
        # 4. Delete PDF database record
        db.session.delete(pdf)
        db.session.commit()
        print(f"Successfully deleted database record for PDF {pdf_id}")
        
        return {"message": "Document deleted successfully"}, 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting PDF {pdf.id}: {str(e)}")
        return {"error": f"Failed to delete document: {str(e)}"}, 500
