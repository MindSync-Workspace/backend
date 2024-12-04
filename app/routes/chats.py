from fastapi import APIRouter, status
from app.controllers.chat_controller import ChatController
from app.schemas.chats import ChatCreate, ChatResponse, ChatUpdate, ChatsResponse
from typing import List

router = APIRouter(prefix="/chats", tags=["Chats"])
chat_controller = ChatController()


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new chat",
)
async def create_chat(chat_data: ChatCreate):
    """
    Create a new chat and get bot response.
    - **document_id**: The unique ID of the document.
    - **is_human**: Indicates if the message is from a human.
    - **text**: The content of the chat message.
    """
    return await chat_controller.create_chat_and_get_bot_response(chat_data)


@router.get(
    "/documents/{document_id}",
    response_model=ChatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all chats by document ID",
)
async def get_chats_by_document_id(document_id: int):
    """
    Fetch all chats for a given document ID.
    - **document_id**: The unique ID of the document.
    """
    return await chat_controller.get_chats_by_document_id(document_id)


@router.put(
    "/{chat_id}",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a chat",
)
async def update_chat(chat_id: int, chat_data: ChatUpdate):
    """
    Update a specific chat by its ID.
    - **chat_id**: The unique ID of the chat to update.

    - **is_human**: Updated human flag (optional).
    - **text**: Updated text of the chat (optional).
    """
    return await chat_controller.update_chat(chat_id, chat_data)


@router.delete("/{chat_id}", status_code=status.HTTP_200_OK, summary="Delete a chat")
async def delete_chat(chat_id: int):
    """
    Delete a chat by its ID.
    - **chat_id**: The unique identifier for the chat.
    """
    return await chat_controller.delete_chat(chat_id)
