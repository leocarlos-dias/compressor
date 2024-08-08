import io
from pikepdf import Pdf
from app.models.file_model import FileModel


class FileService:
    def compress(self, file_model: FileModel) -> io.BytesIO:
        try:
            file_model.file.seek(0)
            file_bytes = file_model.file.read()

            pdf = Pdf.open(io.BytesIO(file_bytes))

            output = io.BytesIO()

            pdf.save(output, linearize=False, compress_streams=True, recompress_flate=True)

            output.seek(0)

            if len(output.getvalue()) >= len(file_bytes):
                return io.BytesIO(file_bytes)

            return output
        except Exception as e:
            raise Exception(f"Error compressing PDF: {str(e)}")
