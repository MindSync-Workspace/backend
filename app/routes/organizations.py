from fastapi import APIRouter, status
from app.controllers.organization_controller import OrganizationController
from app.schemas.organizations import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
    OrganizationsResponse,
)
from typing import List

router = APIRouter(prefix="/organizations", tags=["Organizations"])
organization_controller = OrganizationController()


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new organization",
)
async def create_organization(organization_data: OrganizationCreate):
    """
    Create a new organization in the database.
    - **name**: The name of the organization.
    - **description**: The description of the organization.
    - **start_date**: The start date of the subscription.
    - **end_date**: The end date of the subscription.
    """
    return await organization_controller.create_organization(organization_data)


@router.get(
    "",
    response_model=OrganizationsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all organizations",
)
async def get_organizations():
    """
    Fetch all organizations.
    """
    return await organization_controller.get_organizations()


@router.put(
    "/{organization_id}",
    response_model=OrganizationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an organization",
)
async def update_organization(
    organization_id: int, organization_data: OrganizationUpdate
):
    """
    Update a specific organization by its ID.
    - **organization_id**: The unique ID of the organization to update.
    - **name**: The updated name of the organization.
    - **description**: The updated description of the organization.
    - **start_date**: The updated start date of the subscription.
    - **end_date**: The updated end date of the subscription.
    """
    return await organization_controller.update_organization(
        organization_id, organization_data
    )


@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an organization",
)
async def delete_organization(organization_id: int):
    """
    Delete an organization by its ID.
    - **organization_id**: The unique identifier for the organization.
    """
    return await organization_controller.delete_organization(organization_id)
