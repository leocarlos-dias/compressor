import io
from pikepdf import Pdf
from app.models.file_model import FileModel


class PDFService:
    def compress(self, file_model: FileModel) -> io.BytesIO:
        try:
            file_model.file.seek(0)
            pdf_bytes = file_model.file.read()

            pdf = Pdf.open(io.BytesIO(pdf_bytes))

            output = io.BytesIO()

            pdf.save(output, linearize=False, compress_streams=True, recompress_flate=True)

            output.seek(0)

            if len(output.getvalue()) >= len(pdf_bytes):
                return io.BytesIO(pdf_bytes)

            return output
        except Exception as e:
            raise Exception(f"Error compressing PDF: {str(e)}")
