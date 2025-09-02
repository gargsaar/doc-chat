import json
import os
import shutil
import tempfile
import uuid
from typing import Tuple, Dict, Any, Optional
from werkzeug.utils import secure_filename

# Use local uploads directory instead of external service
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)


def upload(local_file_path: str, file_id: Optional[str] = None) -> Tuple[Dict[str, str], int]:
    """Upload/copy a file to the uploads directory"""
    try:
        if not os.path.exists(local_file_path):
            return {"error": "Source file not found", "status": "failed"}, 404
        
        # Use provided file_id or generate a new one
        if not file_id:
            file_id = str(uuid.uuid4())
            # Keep the original extension
            file_extension = os.path.splitext(local_file_path)[1]
            if file_extension:
                file_id = file_id + file_extension
        
        # Copy the file to uploads directory
        destination_path = os.path.join(UPLOADS_DIR, file_id)
        shutil.copy2(local_file_path, destination_path)
        
        return {
            "file_id": file_id,
            "status": "success"
        }, 200
        
    except Exception as e:
        return {"error": str(e), "status": "failed"}, 500


def create_download_url(file_id):
    """Create a download URL for the file (relative path)"""
    return f"/download/{file_id}"


def delete(file_id: str) -> Tuple[Dict[str, str], int]:
    """Delete a file from the upload directory"""
    try:
        file_path = os.path.join(UPLOADS_DIR, file_id)
        if not os.path.exists(file_path):
            return {"error": "File not found", "status": "failed"}, 404
        
        os.remove(file_path)
        return {
            "file_id": file_id,
            "status": "deleted"
        }, 200
        
    except Exception as e:
        return {"error": str(e), "status": "failed"}, 500


def download(file_id):
    return _Download(file_id)


class _Download:
    def __init__(self, file_id):
        self.file_id = file_id
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = ""

    def download(self):
        """Copy file from uploads directory to temp location"""
        source_path = os.path.join(UPLOADS_DIR, self.file_id)
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"File {self.file_id} not found")
        
        self.file_path = os.path.join(self.temp_dir.name, self.file_id)
        shutil.copy2(source_path, self.file_path)
        return self.file_path

    def cleanup(self):
        self.temp_dir.cleanup()

    def __enter__(self):
        return self.download()

    def __exit__(self, exc, value, tb):
        self.cleanup()
        return False
