from fastapi import APIRouter, status, UploadFile, File, HTTPException, Form
from app.controllers.document_controller import DocumentController
from app.schemas.documents import DocumentCreate, DocumentResponse
from typing import List
import os
from typing import Optional


router = APIRouter(prefix="/documents", tags=["Documents"])
document_controller = DocumentController()

@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and encrypt a new document",
)
async def upload_document(
    user_id: int = Form(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    """
    Upload a new document, encrypt it, and save its metadata.
    - **user_id**: The ID of the user uploading the document.
    - **title**: The title of the document.
    - **description**: A description of the document.
    - **file**: The document file to upload.
    """
    try:
        # Reconstruct the `DocumentCreate` object from the form data
        document_data = DocumentCreate(user_id=user_id, title=title, description=description)
        return await document_controller.upload_document(document_data, file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading document: {str(e)}",
        )

