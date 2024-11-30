from fastapi import HTTPException, status, UploadFile
from app.models.documents import Documents
from fastapi.responses import FileResponse
from app.schemas.documents import DocumentCreate, DocumentUpdate
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.response import create_response
from google.oauth2 import service_account
import logging
from google.cloud import kms
from pathlib import Path
import os
from app.utils.encrypt import handle_upload_and_encrypt, decrypt_document_aes
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
            encryption_key = os.urandom(32)

            # Read file data
            file_data = await file.read()
            file_name = file.filename

            # Encrypt the file and save it
            file_path, encrypted_data = await handle_upload_and_encrypt(
                file_data, file_name, encryption_key
            )

            # Prepare document metadata to store in the database
            doc_dict = document_data.model_dump()
            doc_dict["file_id"] = str(file_path)
            doc_dict["file_size"] = len(encrypted_data)

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
