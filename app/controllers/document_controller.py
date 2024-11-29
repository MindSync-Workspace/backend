from fastapi import HTTPException, status
from app.models.documents import Documents
from app.schemas.documents import DocumentCreate, DocumentUpdate
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.response import create_response
import logging


DocumentPydantic = pydantic_model_creator(Documents, name="Document")


class DocumentController:

    async def upload_document(self, document_data: DocumentCreate):
        try:
            ## TODO: handle FileUpload, handleEncrypt (use cryptography package)
            doc_dict = document_data.model_dump()
            doc_obj = await Documents.create(**doc_dict)
            doc_data = await DocumentPydantic.from_tortoise_orm(doc_obj)
            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Document berhasil diupload",
                data=doc_data.model_dump(),
            )
        except Exception as e:
            logging.error(f"Error saat membuat Document: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat membuat Document", str(e)],
            )
