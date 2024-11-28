from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist
from app.models.notes import Notes
from app.models.whatsapps import Whatsapps
from app.schemas.notes import NoteCreate, NoteUpdate, NoteSearch, NoteData
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.response import create_response
import logging
import datetime
from app.utils.validate_org_access import validate_org_access
from app.utils.chroma import (
    add_note_to_collection,
    get_notes_on_vector_db,
    process_note,
    query_note_similar,
)
from app.utils.get_user_id import get_user_id_by_whatsapp_number
import asyncio

NotePydantic = pydantic_model_creator(Notes, name="Note")
WhatsappPydantic = pydantic_model_creator(Whatsapps, name="Whatsapp")


class NoteController:

    async def create_note(self, note_data: NoteCreate):
        try:
            note_dict = note_data.model_dump()

            metadata = {
                "user_id": note_dict["user_id"],
            }

            if "org_id" in note_dict and note_dict["org_id"] is not None:
                metadata["org_id"] = note_dict["org_id"]
                has_access = await validate_org_access(
                    note_data.org_id, note_data.user_id
                )
                if not has_access:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=[
                            "Anda tidak memiliki akses untuk membuat note di organisasi ini."
                        ],
                    )

            note_obj = await Notes.create(**note_dict)
            logging.info(f"Note dibuat dengan ID: {note_obj.id}")

            await add_note_to_collection(
                note_id=str(note_obj.id), text=note_obj.text, metadata=metadata
            )

            note_data = await NotePydantic.from_tortoise_orm(note_obj)

            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Note berhasil dibuat",
                data=note_data.model_dump(),
            )
        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(f"Error saat membuat note: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat membuat notes", str(e)],
            )

    async def get_note(self, note_id: int):
        try:
            note = await Notes.get_or_none(id=note_id)

            if not note:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=[f"Note dengan ID {note_id} tidak ditemukan"],
                )
            # notes_query = notes_query.prefetch_related("user")
            note_data = await NotePydantic.from_tortoise_orm(note)

            ## Validate user_id must same with request / middleware

            await get_notes_on_vector_db(note_id)

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mendapatkan note",
                data=note_data.model_dump(),
            )

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(
                f"Terjadi error saat mengambil data note dengan ID {note_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengambi data note", str(e)],
            )

    async def get_notes(self, user_id: int):
        try:
            notes_query = Notes.filter(user_id=user_id, org_id=None)
            # notes_query = notes_query.prefetch_related("user")
            notes_data = await NotePydantic.from_queryset(notes_query)
            notes_dict = [note.model_dump() for note in notes_data]

            tasks = [process_note(note, user_id) for note in notes_dict]

            ## Validate user_id same with who that request
            await asyncio.gather(*tasks)

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mendapatkan notes",
                data=notes_dict,
            )

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(
                f"Terjadi error saat mengambil data notes dengan User ID {user_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengambi data notes", str(e)],
            )

    async def get_notes_by_org_id(self, org_id: int):
        try:
            notes_query = Notes.filter(org_id=org_id)
            # notes_query = notes_query.prefetch_related("user")
            notes_data = await NotePydantic.from_queryset(notes_query)
            notes_dict = [note.model_dump() for note in notes_data]

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mendapatkan notes",
                data=notes_dict,
            )
        except Exception as e:
            logging.error(
                f"Terjadi error saat mengambil data notes dengan Organization ID {org_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengambi data notes", str(e)],
            )

    async def get_notes_by_user_id_and_org_id(self, user_id: int, org_id: int):
        try:
            notes_query = Notes.filter(user_id=user_id, org_id=org_id)
            # notes_query = notes_query.prefetch_related("user")
            notes_data = await NotePydantic.from_queryset(notes_query)
            notes_dict = [note.model_dump() for note in notes_data]

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mendapatkan notes",
                data=notes_dict,
            )
        except Exception as e:
            logging.error(
                f"Terjadi error saat mengambil data notes dengan User ID {user_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengambi data notes", str(e)],
            )

    async def update_note(self, note_id: int, note_data: NoteUpdate):
        try:
            note = await Notes.get_or_none(id=note_id)
            if not note:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=[f"Note dengan ID {note_id} tidak ditemukan"],
                )

            if note_data.user_id != note.user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=["Anda tidak memiliki akses untuk mengupdate note ini"],
                )

            await Notes.filter(id=note_id).update(**note_data.model_dump())

            updated_note = await NotePydantic.from_tortoise_orm(
                await Notes.get(id=note_id)
            )

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Note berhasil diupdate",
                data=updated_note.model_dump(),
            )

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(
                f"Terjadi error saat memperbarui note dengan ID {note_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat memperbarui note", str(e)],
            )

    async def delete_note(self, note_id: int):
        try:
            note = await Notes.filter(id=note_id).first()

            if not note:
                raise HTTPException(status_code=404, detail=["Note tidak ditemukan"])

            await note.delete()

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil menghapus note",
                data={},
            )
        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(f"Terjadi error saat menghapus note dengan ID {note_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat menghapus note", str(e)],
            )

    async def get_notes_by_whatsapp_number(self, whatsapp_number: str):

        try:
            user_id = await get_user_id_by_whatsapp_number(whatsapp_number)
            return await self.get_notes(user_id=user_id)

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(
                f"Terjadi error saat mengambil notes untuk nomor WhatsApp {whatsapp_number}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengambil notes", str(e)],
            )

    async def create_note_whatsapp(self, note_data: NoteCreate):
        try:
            user_id = await get_user_id_by_whatsapp_number(note_data.number)
            note_data.user_id = user_id

            return await self.create_note(note_data)

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(f"Error saat membuat note: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat membuat notes", str(e)],
            )

    async def query_similar_notes(self, user_id: int, note_data: NoteSearch):
        try:
            similar_notes = await query_note_similar(
                note_data.text, user_id, note_data.n_items
            )

            async def transform_note(i: int):
                return NoteData(
                    id=int(similar_notes["ids"][0][i]),
                    text=similar_notes["documents"][0][i],
                    user_id=similar_notes["metadatas"][0][i]["user_id"],
                    org_id=None,  # Bisa ditambahkan jika ada
                    embedding=None,  # Bisa diambil jika ada
                    token_identifier=None,  # Bisa diambil jika ada
                    created_at=datetime.datetime.now(),  # Mock, ganti dengan data sebenarnya
                    modified_at=datetime.datetime.now(),  # Mock, ganti dengan data sebenarnya
                ).model_dump()

            transformed_notes = await asyncio.gather(
                *(transform_note(i) for i in range(len(similar_notes["ids"][0])))
            )

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mencari similar note",
                data=transformed_notes,
            )
        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(f"Error saat membuat note: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat membuat notes", str(e)],
            )
