from flask import Blueprint, request, send_file
from app.services.image_service import ImageService
from app.models.file_model import FileModel
from app.services.pdf_service import PDFService
from app.utils.error_handler import APIError

api = Blueprint("api", __name__)


@api.route("/compress/image", methods=["POST"])
def compress_image():
    image_file = request.files.get("image")
    if not image_file:
        raise APIError(400, "MISSING_IMAGE", "No image file provided")

    try:
        image_model = FileModel(file=image_file)
    except ValueError as e:
        raise APIError(400, "INVALID_IMAGE", str(e))

    image_service = ImageService()
    try:
        compressed_image = image_service.compress(image_model)
    except Exception as e:
        raise APIError(500, "COMPRESSION_ERROR", f"Error compressing image: {str(e)}")

    return send_file(compressed_image, mimetype=image_file.mimetype, as_attachment=True, download_name=f"compressed_{image_file.filename}")


@api.route("/compress/pdf", methods=["POST"])
def compress_pdf():
    pdf_file = request.files.get("pdf")
    if not pdf_file:
        raise APIError(400, "MISSING_PDF", "No PDF file provided")

    try:
        pdf_model = FileModel(file=pdf_file)
    except ValueError as e:
        raise APIError(400, "INVALID_PDF", str(e))

    pdf_service = PDFService()
    try:
        compressed_pdf = pdf_service.compress(pdf_model)
    except Exception as e:
        raise APIError(500, "COMPRESSION_ERROR", f"Error compressing PDF: {str(e)}")

    return send_file(compressed_pdf, mimetype=pdf_file.mimetype, as_attachment=True, download_name=f"compressed_{pdf_file.filename}")
