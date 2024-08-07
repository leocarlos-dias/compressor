from flask import Blueprint, request, send_file
from app.services.image_service import ImageService
from app.models.image_model import ImageModel
from app.utils.error_handler import APIError

api = Blueprint("api", __name__)


@api.route("/compress", methods=["POST"])
def compress_image():
    image_file = request.files.get("image")
    if not image_file:
        raise APIError(400, "MISSING_IMAGE", "No image file provided")

    compression_level = request.form.get("compression_level", "medium")

    if compression_level not in ["low", "medium", "high"]:
        raise APIError(400, "INVALID_COMPRESSION_LEVEL", "Compression level must be low, medium, or high",)

    try:
        image_model = ImageModel(file=image_file)
    except ValueError as e:
        raise APIError(400, "INVALID_IMAGE", str(e))

    image_service = ImageService()
    try:
        compressed_image = image_service.compress(image_model, compression_level)
    except Exception as e:
        raise APIError(500, "COMPRESSION_ERROR", f"Error compressing image: {str(e)}")

    return send_file(compressed_image, mimetype=image_file.mimetype, as_attachment=True, download_name=f"compressed_{image_file.filename}",)
