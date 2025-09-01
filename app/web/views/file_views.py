import os
import tempfile
import uuid
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename

bp = Blueprint("files", __name__)

# Create uploads directory if it doesn't exist
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)


@bp.route("/upload", methods=["POST"])
def upload_file():
    """Handle file uploads and return JSON response"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Use provided file_id or generate a new one
        file_id = request.form.get('file_id')
        if not file_id:
            file_id = str(uuid.uuid4())
            filename = secure_filename(file.filename or "")
            if filename:
                # Keep the original extension
                file_extension = os.path.splitext(filename)[1]
                file_id = file_id + file_extension
        
        # Save the file
        file_path = os.path.join(UPLOADS_DIR, file_id)
        file.save(file_path)
        
        return jsonify({
            "file_id": file_id,
            "filename": file.filename,
            "status": "success"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e), "status": "failed"}), 500


@bp.route("/download/<string:file_id>", methods=["GET"])
def download_file(file_id):
    """Serve uploaded files for download"""
    try:
        file_path = os.path.join(UPLOADS_DIR, file_id)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        return send_file(file_path, as_attachment=True, download_name=file_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/delete/<string:file_id>", methods=["DELETE"])
def delete_file(file_id):
    """Delete an uploaded file"""
    try:
        file_path = os.path.join(UPLOADS_DIR, file_id)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        # Delete the file
        os.remove(file_path)
        
        return jsonify({
            "file_id": file_id,
            "status": "deleted"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e), "status": "failed"}), 500
