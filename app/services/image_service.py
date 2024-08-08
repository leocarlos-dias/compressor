from PIL import Image
import io
from app.models.file_model import FileModel


class ImageService:
    def compress(self, image_model: FileModel, compression_level: str = "medium") -> io.BytesIO:
        try:
            image_model.file.seek(0)
            image_bytes = image_model.file.read()

            with Image.open(io.BytesIO(image_bytes)) as image:
                if image.mode == "RGBA":
                    image = image.convert("RGB")

                max_size = (1920, 1080)
                image.thumbnail(max_size, Image.LANCZOS)

                jpeg_quality, png_compression = self._get_compression_settings(compression_level)

                output = io.BytesIO()
                image_format = image.format.upper()

                self._save_image(image, output, image_format, jpeg_quality, png_compression)

                output.seek(0)

                if len(output.getvalue()) >= len(image_bytes):
                    return io.BytesIO(image_bytes)

                return output

        except Exception as e:
            raise RuntimeError(f"Error compressing image: {str(e)}")

    @staticmethod
    def _get_compression_settings(compression_level: str):
        levels = {
            "low": (90, 3),
            "medium": (70, 7),
            "high": (30, 9),
        }
        return levels.get(compression_level.lower(), levels["medium"])

    @staticmethod
    def _save_image(image: Image, output: io.BytesIO, format: str, jpeg_quality: int, png_compression: int):
        save_params = {
            "JPEG": {"format": "JPEG", "quality": jpeg_quality, "optimize": True},
            "JPG": {"format": "JPEG", "quality": jpeg_quality, "optimize": True},
            "PNG": {"format": "PNG", "compress_level": png_compression, "optimize": True},
        }

        params = save_params.get(format, save_params["JPEG"])
        image.save(output, **params)
