from fastapi import APIRouter, HTTPException, status, UploadFile, Form, File
from fastapi.responses import FileResponse
from app.controllers.document_controller import DocumentController
from app.schemas.documents import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentsResponse,
)
from typing import Optional
from app.utils.response import create_response

router = APIRouter(prefix="/documents", tags=["Documents"])
document_controller = DocumentController()


# Upload Document
@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and encrypt a new document",
)
async def upload_document(
    user_id: int = Form(...), title: str = Form(...), file: UploadFile = File(...)
):
    """
    Upload a new document, encrypt it, and save its metadata.
    - **user_id**: The ID of the user uploading the document.
    - **title**: The title of the document.
    - **file**: The document file to upload.
    """
    try:
        document_data = DocumentCreate(
            user_id=user_id, title=title, summary="tteeeesssstttt"
        )
        return await document_controller.upload_document(document_data, file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading document: {str(e)}",
        )


# Update Document
@router.put(
    "/{document_id}",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing document",
)
async def update_document(document_id: int, document_update: DocumentUpdate):
    """
    Update an existing document by its ID.
    - **document_id**: The ID of the document to update.
    - **document_update**: The fields to update (title, summary, etc.).
    """
    try:
        document_update.id = (
            document_id  # Ensure the ID is included in the update request
        )
        return await document_controller.update_document(document_update)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating document: {str(e)}",
        )


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a document",
)
async def delete_document(document_id: int):
    """
    Delete a document by its ID.
    - **document_id**: The ID of the document to delete.
    """
    try:
        # Call delete_document method in the controller
        response = await document_controller.delete_document(document_id)

        # Return successful response with message
        return response  # The response will contain a status_code, message, and data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting document: {str(e)}",
        )


# List Documents by User
@router.get(
    "/",
    response_model=DocumentsResponse,
    status_code=status.HTTP_200_OK,
    summary="List all documents for a user",
)
async def list_documents(user_id: int):
    """
    List all documents uploaded by a user.
    - **user_id**: The ID of the user whose documents to list.
    """
    try:
        return await document_controller.list_documents(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving documents: {str(e)}",
        )


@router.get(
    "/download/{document_id}",
    status_code=status.HTTP_200_OK,
    summary="Download an encrypted document",
)
async def download_document(document_id: int):
    """
    Download a document by its ID.
    - **document_id**: The ID of the document to download.
    """
    try:
        return await document_controller.download_document(document_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error downloading document: {str(e)}",
        )
