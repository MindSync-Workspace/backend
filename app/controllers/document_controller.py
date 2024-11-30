from fastapi import HTTPException, status, UploadFile
from app.models.documents import Documents
from fastapi.responses import FileResponse
from app.schemas.documents import DocumentCreate, DocumentUpdate
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.response import create_response
import logging
from pathlib import Path
from app.utils.response import create_response  
from app.utils.encrypt import handle_upload_and_encrypt, decrypt_document_aes
import os


DocumentPydantic = pydantic_model_creator(Documents, name="Document")


class DocumentController:

    async def upload_document(self, document_data: DocumentCreate, file: UploadFile):
        try:
            encryption_key = os.urandom(32) 

            file_data = await file.read()  
            file_name = file.filename  

            file_path, encrypted_data = await handle_upload_and_encrypt(file_data, file_name, encryption_key)

            doc_dict = document_data.model_dump()
            doc_dict['file_id'] = str(file_path)  

            doc_obj = await Documents.create(**doc_dict)
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
            doc_obj = await Documents.get(id=document_id)
            file_path = Path(doc_obj.file_id)  

            if not file_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Document not found"
                )
            
            encryption_key = os.urandom(32)  

            decrypted_data = decrypt_document_aes(file_path, encryption_key)

            decrypted_file_path = file_path.with_suffix('.decrypted')
            with open(decrypted_file_path, 'wb') as f:
                f.write(decrypted_data)

            return FileResponse(decrypted_file_path, media_type="application/octet-stream", filename=file_path.name)

        except Exception as e:
            logging.error(f"Error during document download: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mendownload document", str(e)],
            )