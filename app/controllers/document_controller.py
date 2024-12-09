from fastapi import HTTPException, status, UploadFile
from app.models.documents import Documents
from io import BytesIO
from fastapi.responses import StreamingResponse
from app.schemas.documents import (
    DocumentUpdate,
    DocumentResponse,
    DocumentsResponse,
    DocumentCreate,
)
from tortoise.exceptions import DoesNotExist
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.response import create_response
import base64
from google.oauth2 import service_account
from google.cloud import kms
from pathlib import Path
import os
import logging
from app.utils.encrypt import encrypt_document_aes, decrypt_document_aes
from app.utils.get_user_id import get_user_id_by_whatsapp_number
from dotenv import load_dotenv

load_dotenv()


DocumentPydantic = pydantic_model_creator(Documents, name="Document")


class DocumentController:

    def __init__(self):
        file_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "utils",
            "secrets",
            "service-account-key.json",
        )
        credentials = service_account.Credentials.from_service_account_file(file_path)

        self.kms_client = kms.KeyManagementServiceClient(credentials=credentials)
        self.key_name = os.getenv("KMS_KEY_NAME")
        if not self.key_name:
            raise Exception("KMS_KEY_NAME environment variable is not set.")

    async def upload_document(self, document_data: DocumentCreate, file: UploadFile):
        try:
            # Generate a random encryption key (AES-256)
            # encryption_key = os.urandom(32)

            # # Encode the encryption key to base64
            # encryption_key_base64 = base64.b64encode(encryption_key).decode("utf-8")

            # Read file data
            file_data = await file.read()
            file_name = file.filename

            # Encrypt the file
            # encrypted_data = encrypt_document_aes(file_data, encryption_key)

            # Save only the encrypted file
            encrypted_file_path = Path("media") / (
                file_name
            )  # Store encrypted version with '.enc' extension
            with open(encrypted_file_path, "wb") as f:
                f.write(file_data)

            # Prepare document metadata to store in the database
            doc_dict = document_data.model_dump()
            doc_dict["file_path"] = str(encrypted_file_path)  # Path to encrypted file
            doc_dict["file_size"] = len(file_data)  # Size of the encrypted file
            doc_dict["encryption_key"] = (
                "Asasa"  # Store the base64-encoded encryption key
            )

            # doc_dict["encryption_key"] = (
            #     encryption_key_base64  # Store the base64-encoded encryption key
            # )

            # Create the document entry in the database
            doc_obj = await Documents.create(**doc_dict)

            # Serialize the document data to return in the response
            doc_data = await DocumentPydantic.from_tortoise_orm(doc_obj)
            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Document berhasil diupload",
                data=doc_data.model_dump(),
            )

        except Exception as e:

            logging.error(f"Error saat mengupload document: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengupload document", str(e)],
            )

    async def get_document_by_id(self, document_id: int) -> DocumentResponse:
        try:
            # Fetch the document metadata from the database
            doc = await Documents.get(id=document_id)

            if not doc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=["Document not found"],
                )

            # Serialize the document data to return in the response
            doc_data = await DocumentPydantic.from_tortoise_orm(doc)

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Document retrieved successfully",
                data=doc_data.model_dump(),
            )

        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=["Document not found"],
            )
        except Exception as e:
            logging.error(f"Error fetching document: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Error fetching document", str(e)],
            )

    async def update_document(
        self, document_update: DocumentUpdate
    ) -> DocumentResponse:
        try:
            doc = await Documents.get(id=document_update.id)

            # Dynamically update provided fields
            update_data = document_update.model_dump(
                exclude_unset=True
            )  # Get only fields that were set
            for field, value in update_data.items():
                setattr(doc, field, value)

            # Save the updated document
            await doc.save()

            doc_data = await DocumentPydantic.from_tortoise_orm(doc)

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Document updated successfully",
                data=doc_data.model_dump(),
            )

        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=["Document not found"],
            )

    async def delete_document(self, document_id: int):
        try:
            # Retrieve the document by its ID
            doc = await Documents.get(id=document_id)

            # Get the file path from the document
            file_path = Path(doc.file_path)  # The file_path is stored in the database

            # Ensure the file exists before attempting to delete
            if file_path.exists():
                os.remove(file_path)  # Delete the file from the media directory

            # Delete the document from the database
            await doc.delete()

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Document deleted successfully",
                data={},
            )

        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=["Document not found"],
            )
        except Exception as e:
            logging.error(f"Error deleting document: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Error deleting document", f"{str(e)}"],
            )

    # List all Documents
    async def get_all_documents_by_user_id(self, user_id: int) -> DocumentsResponse:
        try:
            docs = Documents.filter(user_id=user_id)
            docs_data = await DocumentPydantic.from_queryset(docs)

            docs_dict = [
                {
                    key: value
                    for key, value in doc.model_dump().items()
                    if key != "encryption_key"
                }
                for doc in docs_data
            ]
            return create_response(
                status_code=status.HTTP_200_OK,
                message="Documents retrieved successfully",
                data=docs_dict,
            )
        except Exception as e:
            logging.exception("Error retrieving documents")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Error retrieving documents", str(e)],
            )

    async def download_document(self, document_id: int) -> StreamingResponse:
        try:
            # Fetch the document metadata from the database
            doc = await Documents.get(id=document_id)

            if not doc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=["Document not found"],
                )

            # Get the encrypted file path, encryption key, and the original file extension from the database
            encrypted_file_path = Path(doc.file_path)
            encryption_key = doc.encryption_key

            # Ensure the encryption key is in bytes format (if it's a string, convert it to bytes)
            if isinstance(encryption_key, str):
                encryption_key = encryption_key.encode("utf-8")  # Convert to bytes

            # Ensure the encrypted file exists
            if not encrypted_file_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=["Encrypted file not found"],
                )

            # Read the encrypted file data
            with open(encrypted_file_path, "rb") as f:
                encrypted_data = f.read()

            # Decrypt the document
            decrypted_data = decrypt_document_aes(encrypted_data, encryption_key)

            decrypted_file = BytesIO(decrypted_data)
            decrypted_file.seek(0)

            # Prepare headers for Content-Disposition with filename
            headers = {
                "Content-Disposition": f"attachment; filename=document_{document_id}.pdf"
            }

            # Return the decrypted file for download with the correct MIME type
            return StreamingResponse(
                decrypted_file, media_type="application/octet-stream", headers=headers
            )

        except Exception as e:
            logging.error(f"Error during document download: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Error during document download", f"{str(e)}"],
            )

    async def upload_document_by_whatsapp_number(
        self, document_data: DocumentCreate, file: UploadFile
    ):
        try:
            user_id = await get_user_id_by_whatsapp_number(document_data.number)
            document_data.user_id = user_id

            return await self.upload_document(document_data, file)

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(f"Error saat mengupload document: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengupload document", str(e)],
            )
