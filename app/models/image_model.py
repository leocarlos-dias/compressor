from pydantic import BaseModel, validator
from werkzeug.datastructures import FileStorage


class ImageModel(BaseModel):
    file: FileStorage

    @validator("file")
    def validate_image(cls, v):
        if v.filename.split(".")[-1].lower() not in ["png", "jpg", "jpeg"]:
            raise ValueError("Invalid file format. Only PNG, JPG, and JPEG are allowed.")
        return v

    class Config:
        arbitrary_types_allowed = True
