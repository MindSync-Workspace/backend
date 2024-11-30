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

        file_path = os.path.join(os.path.dirname(__file__), '..', 'utils', 'secrets', 'service-account-key.json')
        credentials = service_account.Credentials.from_service_account_file(file_path)

        self.kms_client = kms.KeyManagementServiceClient(credentials=credentials)
        self.key_name = os.getenv('KMS_KEY_NAME')
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
            file_path, encrypted_data = await handle_upload_and_encrypt(file_data, file_name, encryption_key)

            # Encrypt the AES key using KMS
            encrypted_key = self.kms_client.encrypt(name=self.key_name, plaintext=encryption_key).ciphertext

            # Prepare document metadata to store in the database
            doc_dict = document_data.model_dump()
            doc_dict['file_id'] = str(file_path)  # Store the file path
            doc_dict['encryption_key'] = encrypted_key  # Store the encrypted AES key
            doc_dict['file_size'] = len(encrypted_data)  # Store the file size (optional)

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

    async def download_document(self, document_id: int):
        try:
            # Retrieve the document from the database
            doc_obj = await Documents.get(id=document_id)
            file_path = Path(doc_obj.file_id)

            if not file_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Document not found"
                )

            # Retrieve the encrypted AES key from the database
            encrypted_key = doc_obj.encryption_key

            # Decrypt the AES key using KMS
            encryption_key = self.kms_client.decrypt(name=self.key_name, ciphertext=encrypted_key).plaintext

            # Decrypt the document using the AES key
            decrypted_data = decrypt_document_aes(file_path, encryption_key)

            # Save the decrypted file to a temporary location
            decrypted_file_path = file_path.with_suffix('.decrypted')
            with open(decrypted_file_path, 'wb') as f:
                f.write(decrypted_data)

            # Return the decrypted file as a download response
            return FileResponse(decrypted_file_path, media_type="application/octet-stream", filename=file_path.name)

        except Exception as e:
            logging.error(f"Error during document download: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mendownload document", str(e)],
            )
