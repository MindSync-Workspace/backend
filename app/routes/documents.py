from fastapi import APIRouter, status, UploadFile, Form, File

from app.controllers.document_controller import DocumentController
from app.schemas.documents import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentsResponse,
)

from app.utils.response import create_response
from app.utils.chroma.documents import (
    reset_database,
)


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

    document_data = DocumentCreate(user_id=user_id, title=title)

    return await document_controller.upload_document(document_data, file)


# Get Document By Id
@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a document by its ID",
)
async def get_document(document_id: int):
    """
    Retrieve a document's details by its ID.
    - **document_id**: The ID of the document to retrieve.
    """
    return await document_controller.get_document_by_id(document_id)


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
    document_update.id = document_id

    return await document_controller.update_document(document_update)


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

    return await document_controller.delete_document(document_id)


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

    return await document_controller.get_all_documents_by_user_id(user_id)


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

    return await document_controller.download_document(document_id)


@router.post(
    "/whatsapps/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and encrypt a new document (**BOT**)",
)
async def upload_document_from_whatsapp(
    number: str = Form(...), title: str = Form(...), file: UploadFile = File(...)
):
    """
    Upload a new document, encrypt it, and save its metadata.
    - **number**: The unique whatsapp number.
    - **title**: The title of the document.
    - **file**: The document file to upload.
    """
    print(number, title)

    document_data = DocumentCreate(number=number, title=title, summary="tteeeesssstttt")

    return await document_controller.upload_document_by_whatsapp_number(
        document_data, file
    )


@router.get(
    "/test/test",
    response_model={},
    status_code=status.HTTP_201_CREATED,
    summary="Upload and encrypt a new document (**BOT**)",
)
async def upload_document_from_whatsapp(
    # number: str = Form(...), title: str = Form(...), file: UploadFile = File(...)
):
    """
    Upload a new document, encrypt it, and save its metadata.
    - **number**: The unique whatsapp number.
    - **title**: The title of the document.
    - **file**: The document file to upload.
    """
    try:
        # documents = load_documents("app\\utils\\document.pdf")

        # chunks = split_documents(documents)
        # await add_docs_to_new_collection(chunks, 1)

        #
        reset_database()
        # response = get_chat_response_from_model(
        #     "Maksud penelitian ini,jawab dengan 20 kata maksimal",
        #     1,
        # )
        return create_response(
            status_code=200, message="Berhasil", data={"response": "Berhasil hapus"}
        )
    except Exception as e:
        print(e)
