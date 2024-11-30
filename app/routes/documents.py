from fastapi import APIRouter, status, UploadFile, File, HTTPException
from app.controllers.document_controller import DocumentController
from app.schemas.documents import DocumentCreate, DocumentResponse
from typing import List
import os

router = APIRouter(prefix="/documents", tags=["Documents"])
document_controller = DocumentController()

@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and encrypt a new document",
)
async def upload_document(document_data: DocumentCreate, file: UploadFile = File(...)):
    """
    Upload a new document, encrypt it, and save its metadata.
    - **document_data**: The metadata for the document (title, description, etc.).
    - **file**: The document file to upload.
    """
    try:
        return await document_controller.upload_document(document_data, file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading document: {str(e)}"
        )

@router.get(
    "/download/{document_id}",
    status_code=status.HTTP_200_OK,
    summary="Download a document",
)
async def download_document(document_id: int):
    """
    Download a document by its ID.
    - **document_id**: The unique ID of the document to download.
    """
    try:
        return await document_controller.download_document(document_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} not found: {str(e)}"
        )
