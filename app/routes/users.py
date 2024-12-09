from fastapi import APIRouter, status, Header
from app.controllers.user_controller import UserController
from app.schemas.users import UserCreate, UserUpdate, UserResponse
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])
user_controller = UserController()


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
async def create_user(user_data: UserCreate, content_type: str = Header(None)):
    """
    Create a new user in the database.
    - **username**: The unique username for the user.
    - **email**: The user's email address.
    - **password**: The user's password (hashed and stored securely).
    """
    print(content_type)
    return await user_controller.create_user(user_data)


@router.get("", response_model=List[UserResponse], summary="Get list of all users")
async def get_users():
    """Fetch all users from the database."""
    return await user_controller.get_users()


@router.get(
    "/{email}", response_model=UserResponse, summary="Retrieve a single user by ID"
)
async def get_user(email: str):
    """
    Get a user's details by their Email.
    - **email**: The unique identifier for the user.
    """
    return await user_controller.get_user(email)


@router.put(
    "/{user_id}", response_model=UserResponse, summary="Update a user's details"
)
async def update_user(user_id: int, user_data: UserUpdate):
    """
    Update a user's details.
    - **user_id**: The unique identifier for the user.
    - **user_data**: Fields to update (optional fields are allowed).
    """
    return await user_controller.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, summary="Delete a user")
async def delete_user(user_id: int):
    """
    Delete a user by their ID.
    - **user_id**: The unique identifier for the user.
    """
    return await user_controller.delete_user(user_id)
