from PIL import Image
import io
from app.models.image_model import ImageModel


class ImageService:
    def compress(self, image_model: ImageModel, compression_level: str = "medium") -> io.BytesIO:
        try:
            # Abrir a imagem e converter para bytes
            image_model.file.seek(0)
            image_bytes = image_model.file.read()

            image = Image.open(io.BytesIO(image_bytes))

            # Converter para RGB se for RGBA
            if image.mode == "RGBA":
                image = image.convert("RGB")

            # Redimensionar a imagem se for muito grande
            max_size = (1920, 1080)  # Full HD
            image.thumbnail(max_size, Image.LANCZOS)

            # Definir qualidade com base no nível de compressão
            if compression_level == "low":
                jpeg_quality = 80
                png_compression = 6
            elif compression_level == "medium":
                jpeg_quality = 70
                png_compression = 7
            else:  # high
                jpeg_quality = 60
                png_compression = 9

            # Comprimir a imagem
            output = io.BytesIO()

            if image.format == "PNG":
                image.save(output, format="PNG", optimize=True, compress_level=png_compression)
            elif image.format in ["JPEG", "JPG"]:
                image.save(output, format="JPEG", optimize=True, quality=jpeg_quality)
            else:
                # Para outros formatos, use JPEG
                image.save(output, format="JPEG", optimize=True, quality=jpeg_quality)

            output.seek(0)

            # Verifica se a compressão foi efetiva
            if len(output.getvalue()) >= len(image_bytes):
                # Se não foi efetiva, retorna a imagem original
                return io.BytesIO(image_bytes)

            return output
        except Exception as e:
            raise Exception(f"Error compressing image: {str(e)}")
