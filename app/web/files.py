import json
import os
import requests
import tempfile
from typing import Tuple, Dict, Any, Optional
from app.web.config import Config

upload_url = f"{Config.UPLOAD_URL}/upload"


def upload(local_file_path: str, file_id: Optional[str] = None) -> Tuple[Dict[str, str], int]:
    with open(local_file_path, "rb") as f:
        files_data = {"file": f}
        data = {}
        if file_id:
            data["file_id"] = file_id
        response = requests.post(upload_url, files=files_data, data=data)
        return json.loads(response.text), response.status_code


def create_download_url(file_id):
    return f"{Config.UPLOAD_URL}/download/{file_id}"


def delete(file_id: str) -> Tuple[Dict[str, str], int]:
    """Delete a file from the upload service"""
    response = requests.delete(f"{Config.UPLOAD_URL}/delete/{file_id}")
    return json.loads(response.text), response.status_code


def download(file_id):
    return _Download(file_id)


class _Download:
    def __init__(self, file_id):
        self.file_id = file_id
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = ""

    def download(self):
        self.file_path = os.path.join(self.temp_dir.name, self.file_id)
        response = requests.get(create_download_url(self.file_id), stream=True)
        with open(self.file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return self.file_path

    def cleanup(self):
        self.temp_dir.cleanup()

    def __enter__(self):
        return self.download()

    def __exit__(self, exc, value, tb):
        self.cleanup()
        return False
