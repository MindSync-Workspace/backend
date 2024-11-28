from fastapi import APIRouter, status
from app.controllers.membership_controller import MembershipController
from app.schemas.memberships import (
    MembershipCreate,
    MembershipResponse,
    MembershipUpdate,
    MembershipsResponse,
)
from typing import List

router = APIRouter(prefix="/memberships", tags=["Memberships"])
membership_controller = MembershipController()


@router.post(
    "",
    response_model=MembershipResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new membership",
)
async def create_membership(membership_data: MembershipCreate):
    """
    Create a new membership in the database.
    - **user_id**: The unique user ID.
    - **membership_type**: The type of membership.
    - **start_date**: The start date of the membership.
    - **end_date**: The end date of the membership.
    """
    return await membership_controller.create_membership(membership_data)


@router.get(
    "/users/{user_id}",
    response_model=MembershipsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all memberships by user ID",
)
async def get_memberships_by_user_id(user_id: int):
    """
    Fetch all memberships for a given user ID.
    - **user_id**: The unique user ID.
    """
    return await membership_controller.get_memberships_by_user_id(user_id)


@router.put(
    "/{membership_id}",
    response_model=MembershipResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a membership",
)
async def update_membership(membership_id: int, membership_data: MembershipUpdate):
    """
    Update a specific membership by its ID.
    - **membership_id**: The unique ID of the membership to update.
    - **membership_type**: The updated type of membership.
    - **start_date**: The updated start date of the membership.
    - **end_date**: The updated end date of the membership.
    """
    return await membership_controller.update_membership(membership_id, membership_data)


@router.delete(
    "/{membership_id}", status_code=status.HTTP_200_OK, summary="Delete a membership"
)
async def delete_membership(membership_id: int):
    """
    Delete a membership by its ID.
    - **membership_id**: The unique identifier for the membership.
    """
    return await membership_controller.delete_membership(membership_id)
