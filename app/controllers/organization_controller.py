from fastapi import HTTPException, status
from app.models.organizations import Organizations
from app.schemas.organizations import OrganizationCreate, OrganizationUpdate
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.response import create_response
import logging
import datetime


OrganizationPydantic = pydantic_model_creator(Organizations, name="Organization")


class OrganizationController:
    async def create_organization(self, organization_data: OrganizationCreate):
        try:
            organization_dict = organization_data.model_dump()
            now = datetime.datetime.utcnow()
            organization_dict['start_date'] = now
            organization_dict['end_date'] = now + datetime.timedelta(days=30)
            organization_obj = await Organizations.create(**organization_dict)
            organization_data = await OrganizationPydantic.from_tortoise_orm(organization_obj)
            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Organization berhasil dibuat",
                data=organization_data.model_dump(),
            )
        except Exception as e:
            logging.error(f"Error saat membuat organization: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat membuat organization", str(e)],
            )

    async def get_organizations(self):
        try:
            organizations_query = Organizations.all()
            organizations_data = await OrganizationPydantic.from_queryset(organizations_query)
            organizations_dict = [organization.model_dump() for organization in organizations_data]

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mendapatkan organizations",
                data=organizations_dict,
            )
        except Exception as e:
            logging.error(f"Terjadi error saat mengambil data organizations: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengambil data organizations", str(e)],
            )

    async def update_organization(self, organization_id: int, organization_data: OrganizationUpdate):
        try:
            organization = await Organizations.get_or_none(id=organization_id)
            if not organization:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=[f"Organization dengan ID {organization_id} tidak ditemukan", str(e)],
                )

            await Organizations.filter(id=organization_id).update(**organization_data.model_dump())

            updated_organization = await OrganizationPydantic.from_tortoise_orm(
                await Organizations.get(id=organization_id)
            )

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Organization berhasil diupdate",
                data=updated_organization.model_dump(),
            )
        
        except HTTPException as http_exc:
            raise http_exc
        
        except Exception as e:
            logging.error(f"Terjadi error saat memperbarui organization dengan ID {organization_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat memperbarui organization", str(e)],
            )

    async def delete_organization(self, organization_id: int):
        try:
            organization = await Organizations.filter(id=organization_id).first()
            if not organization:
                raise HTTPException(status_code=404, detail=["Organization tidak ditemukan"])

            await organization.delete()

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil menghapus organization",
                data={},
            )
        except HTTPException as http_exc:
            raise http_exc
        
        except Exception as e:
            logging.error(f"Terjadi error saat menghapus organization dengan ID {organization_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat menghapus organization", str(e)],
            )
