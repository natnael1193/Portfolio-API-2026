import mimetypes
from typing import Literal
from io import BytesIO
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status
from app.config import get_settings

settings = get_settings()

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_DOC_TYPES   = {"application/pdf"}
MAX_IMAGE_SIZE      = 5 * 1024 * 1024   # 5 MB
MAX_DOC_SIZE        = 20 * 1024 * 1024  # 20 MB

Bucket = Literal["images", "documents"]

BUCKET_CONFIG: dict[str, dict] = {
    "images":    {"allowed": ALLOWED_IMAGE_TYPES, "max_bytes": MAX_IMAGE_SIZE},
    "documents": {"allowed": ALLOWED_DOC_TYPES,   "max_bytes": MAX_DOC_SIZE},
}


def _configure():
    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )


async def _validate(file: UploadFile, bucket: Bucket) -> tuple[bytes, str]:
    cfg = BUCKET_CONFIG[bucket]

    content_type = (
        file.content_type
        or mimetypes.guess_type(file.filename or "")[0]
        or "application/octet-stream"
    )

    if content_type not in cfg["allowed"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"File type '{content_type}' not allowed for bucket '{bucket}'. "
                f"Allowed: {', '.join(sorted(cfg['allowed']))}"
            ),
        )

    data = await file.read()

    if len(data) > cfg["max_bytes"]:
        mb = cfg["max_bytes"] // (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum size of {mb} MB",
        )

    return data, content_type


async def upload_file(file: UploadFile, bucket: Bucket, folder: str = "") -> str:
    _configure()
    data, content_type = await _validate(file, bucket)

    cloud_folder = f"portfolio/{bucket}/{folder}" if folder else f"portfolio/{bucket}"
    resource_type = "image" if bucket == "images" else "raw"

    try:
        result = cloudinary.uploader.upload(
            BytesIO(data),
            folder=cloud_folder,
            resource_type=resource_type,
            unique_filename=True,
            overwrite=False,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Cloudinary upload error: {str(e)}",
        )

    return result["secure_url"]


async def delete_file(public_url: str) -> None:
    try:
        _configure()
        parts = public_url.split("/upload/")
        if len(parts) != 2:
            return
        path = parts[1]
        if path.startswith("v") and "/" in path:
            path = path.split("/", 1)[1]
        public_id = path.rsplit(".", 1)[0]
        resource_type = "image" if "/image/" in public_url else "raw"
        cloudinary.uploader.destroy(public_id, resource_type=resource_type)
    except Exception:
        pass