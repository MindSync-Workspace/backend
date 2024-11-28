from fastapi import APIRouter, status, Header
from app.controllers.note_controller import NoteController
from app.schemas.notes import NoteCreate, NoteResponse, NoteUpdate, NotesResponse
from typing import List

router = APIRouter(prefix="/notes", tags=["Notes"])
note_controller = NoteController()


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
)
async def create_note(note_data: NoteCreate):
    """
    Create a new note in the database.
    - **user_id**: The unique userid of each user.
    - **org_id** (optional): The unique organization ID.
    - **text**: The note's text.
    """
    return await note_controller.create_note(note_data)


@router.get(
    "/users/{user_id}",
    response_model=List[NotesResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all notes by user ID",
)
async def get_notes_by_user_id(user_id: int):
    """
    Fetch all notes for a given user ID.
    - **user_id**: The unique user ID.
    """
    return await note_controller.get_notes(user_id)


@router.get(
    "/users/{user_id}/organizations/{organizations_id}",
    response_model=NotesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all notes by user ID and organization ID",
)
async def get_notes_by_user_id_and_org_id(user_id: int, organizations_id: int):
    """
    Fetch all notes for a given user ID and organization ID.
    - **user_id**: The unique user ID.
    - **org_id**: The unique organization ID.
    """
    return await note_controller.get_notes_by_user_id_and_org_id(
        user_id, organizations_id
    )


@router.put(
    "/{note_id}",
    response_model=NoteResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a note",
)
async def update_note(note_id: int, note_data: NoteUpdate):
    """
    Update a specific note by its ID.
    - **user_id**: The unique user ID.
    - **org_id** (optional): The unique organization ID.
    - **note_id**: The unique ID of the note to update.
    - **text**: The updated note's text.
    """
    return await note_controller.update_note(note_id, note_data)


@router.delete("/{note_id}", status_code=status.HTTP_200_OK, summary="Delete a note")
async def delete_user(note_id: int):
    """
    Delete a note by their ID.
    - **note_id**: The unique identifier for the note_id.
    """
    return await note_controller.delete_note(note_id)


@router.post(
    "/whatsapps",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note on Whatsapp (**BOT**)",
)
async def create_note_whatsapp(note_data: NoteCreate):
    """
    Create a new note in the database.
    - **number**: The unique whatsapp number.
    - **text**: The note's text.
    """
    return await note_controller.create_note_whatsapp(note_data)


@router.get(
    "/whatsapps/{whatsapp_number}",
    response_model=NotesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all notes by Whatsapp number (**BOT**)",
)
async def get_notes_by_whatsapp_number(whatsapp_number: str):
    """
    Fetch all notes for a given user ID and organization ID.
    - **number**: The unique whatsapp number.
    """

    return await note_controller.get_notes_by_whatsapp_number(whatsapp_number)
