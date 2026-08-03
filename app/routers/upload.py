from fastapi import APIRouter, UploadFile, File, Query
from typing import Literal
from app.core.dependencies import AdminDep
from app.services.storage import upload_file, delete_file, Bucket
from pydantic import BaseModel

router = APIRouter(prefix="/upload", tags=["upload"])


class UploadResponse(BaseModel):
    url: str
    filename: str
    bucket: str


class DeleteRequest(BaseModel):
    url: str


@router.post("", response_model=UploadResponse, dependencies=[AdminDep])
async def upload(
    file: UploadFile = File(...),
    bucket: Bucket = Query("images", description="'images' or 'documents'"),
    folder: str = Query("", description="Sub-folder, e.g. 'projects' or 'posts'"),
):
    url = await upload_file(file, bucket, folder)
    return UploadResponse(url=url, filename=file.filename or "", bucket=bucket)


@router.delete("", status_code=204, dependencies=[AdminDep])
async def remove(body: DeleteRequest):
    await delete_file(body.url)