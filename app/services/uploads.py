import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


def save_uploaded_file(file_storage, subdirectory: str) -> str | None:
    if not file_storage or not file_storage.filename:
        return None

    filename = secure_filename(file_storage.filename)
    if not filename:
        return None

    upload_root = current_app.config["UPLOAD_FOLDER"]
    target_directory = os.path.join(upload_root, subdirectory)
    os.makedirs(target_directory, exist_ok=True)

    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    file_storage.save(os.path.join(target_directory, unique_filename))
    return unique_filename
