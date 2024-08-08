from flask import Blueprint, request, send_file
from app.services.image_service import ImageService
from app.models.image_model import ImageModel
from app.models.file_model import FileModel
from app.services.file_service import FileService
from app.utils.error_handler import APIError

api = Blueprint("api", __name__)


@api.route("/compress/image", methods=["POST"])
def compress_image():
    image_file = request.files.get("image")
    if not image_file:
        raise APIError(400, "MISSING_IMAGE", "No image file provided")

    try:
        image_model = ImageModel(file=image_file)
    except ValueError as e:
        raise APIError(400, "INVALID_IMAGE", str(e))

    image_service = ImageService()
    try:
        compressed_image = image_service.compress(image_model)
    except Exception as e:
        raise APIError(500, "COMPRESSION_ERROR", f"Error compressing image: {str(e)}")

    return send_file(compressed_image, mimetype=image_file.mimetype, as_attachment=True, download_name=f"compressed_{image_file.filename}")


@api.route("/compress/file", methods=["POST"])
def compress_pdf():
    file_file = request.files.get("file")
    if not file_file:
        raise APIError(400, "MISSING_FILE", "No file file provided")

    try:
        file_model = FileModel(file=file_file)
    except ValueError as e:
        raise APIError(400, "INVALID_FILE", str(e))

    file_service = FileService()
    try:
        compressed_pdf = file_service.compress(file_model)
    except Exception as e:
        raise APIError(500, "COMPRESSION_ERROR", f"Error compressing file: {str(e)}")

    return send_file(compressed_pdf, mimetype=file_file.mimetype, as_attachment=True, download_name=f"compressed_{file_file.filename}")
