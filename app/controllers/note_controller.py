from fastapi import HTTPException, status
from app.models.notes import Notes
from app.schemas.notes import NoteCreate, NoteUpdate
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.response import create_response
import logging
from tortoise.transactions import in_transaction
from app.utils.validate_org_access import validate_org_access
from app.utils.embed import generate_embedding
from app.utils.chroma import add_note_to_collection

NotePydantic = pydantic_model_creator(Notes, name="Note")


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

            add_note_to_collection(
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

    async def get_notes_by_user_id(self, user_id: int):
        try:
            notes_query = Notes.filter(user_id=user_id, org_id=None)
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
