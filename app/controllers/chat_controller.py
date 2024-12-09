from fastapi import HTTPException, status
from app.models.chats import Chats
from app.schemas.chats import ChatCreate, ChatUpdate
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.response import create_response
import logging
from app.utils.rag.rag import get_chat_response_from_model

ChatPydantic = pydantic_model_creator(Chats, name="Chat")


class ChatController:
    async def create_chat_and_get_bot_response(self, chat_data: ChatCreate):
        try:
            chat_dict = chat_data.model_dump()
            chat_dict["is_human"] = True
            chat_obj = await Chats.create(**chat_dict)
            chat_data = await ChatPydantic.from_tortoise_orm(chat_obj)

            bot_response_text = get_chat_response_from_model(
                chat_dict["text"], chat_dict["document_id"]
            )

            bot_chat_data = {
                "document_id": chat_dict["document_id"],
                "user_id": chat_dict["user_id"],
                # "org_id": chat_dict.get("org"),
                "is_human": False,
                "text": bot_response_text,
            }

            bot_chat_obj = await Chats.create(**bot_chat_data)
            bot_chat_data = await ChatPydantic.from_tortoise_orm(bot_chat_obj)

            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Berhasil mendapatkan response model",
                data=bot_chat_data.model_dump(),
            )
        except Exception as e:
            logging.error(f"Error saat membuat chat: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat membuat chat", str(e)],
            )

    async def get_chats_by_document_id(self, document_id: int):
        try:
            chats_query = Chats.filter(document_id=document_id).order_by("created_at")
            chats_data = await ChatPydantic.from_queryset(chats_query)
            chats_dict = [chat.model_dump() for chat in chats_data]

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mendapatkan chats",
                data=chats_dict,
            )

        except Exception as e:
            logging.error(
                f"Terjadi error saat mengambil data chats dengan Document ID {document_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengambil data chats", str(e)],
            )

    async def update_chat(self, chat_id: int, chat_data: ChatUpdate):
        try:
            chat = await Chats.get_or_none(id=chat_id)
            if not chat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=[f"Chat dengan ID {chat_id} tidak ditemukan"],
                )

            await Chats.filter(id=chat_id).update(**chat_data.model_dump())

            updated_chat = await ChatPydantic.from_tortoise_orm(
                await Chats.get(id=chat_id)
            )

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Chat berhasil diupdate",
                data=updated_chat.model_dump(),
            )

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(
                f"Terjadi error saat memperbarui chat dengan ID {chat_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat memperbarui chat", str(e)],
            )

    async def delete_chat(self, chat_id: int):
        try:
            chat = await Chats.filter(id=chat_id).first()
            if not chat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=["Chat tidak ditemukan"],
                )

            await chat.delete()

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil menghapus chat",
                data={},
            )

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(f"Terjadi error saat menghapus chat dengan ID {chat_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat menghapus chat", str(e)],
            )
