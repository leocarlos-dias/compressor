from pydantic import BaseModel, validator
from werkzeug.datastructures import FileStorage


class FileModel(BaseModel):
    file: FileStorage

    @validator("file")
    def validate_file(cls, v):
        if v.filename.split(".")[-1].lower() in ["png", "jpg", "jpeg"]:
            return v
        elif v.filename.split(".")[-1].lower() == "pdf":
            return v
        else:
            raise ValueError("Invalid file format. Only PNG, JPG, JPEG and PDF are allowed.")

    class Config:
        arbitrary_types_allowed = True
