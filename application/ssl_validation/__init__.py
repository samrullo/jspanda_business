import os
from flask import Blueprint
from flask import send_from_directory
from flask import current_app
from flask import redirect, url_for
import logging

_logger = logging.getLogger(__name__)
logging.basicConfig()
_logger.setLevel(logging.INFO)

ssl_validation_bp = Blueprint('ssl_vaidation_bp', __name__)


@ssl_validation_bp.route('/.well-known/pki-validation/<filename>')
def serve_ssl_validation_file(filename):
    file_path = os.path.join(current_app.config.get('SSL_VALIDATION_FOLDER'), filename)
    _logger.info(f"{file_path} file exists? {os.path.exists(file_path)}")
    return send_from_directory(current_app.config.get('SSL_VALIDATION_FOLDER'), filename, conditional=True)
    # return f"you are trying to access a file from well-known {filename}"
