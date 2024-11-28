from fastapi import HTTPException, status
from app.models.memberships import Memberships
from app.schemas.memberships import MembershipCreate, MembershipUpdate
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.response import create_response
import logging

MembershipPydantic = pydantic_model_creator(Memberships, name="Membership")


class MembershipController:
    async def create_membership(self, membership_data: MembershipCreate):
        try:
            membership_dict = membership_data.model_dump()
            membership_obj = await Memberships.create(**membership_dict)
            membership_data = await MembershipPydantic.from_tortoise_orm(membership_obj)
            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Membership berhasil dibuat",
                data=membership_data.model_dump(),
            )
        except Exception as e:
            logging.error(f"Error saat membuat membership: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat membuat membership", str(e)],
            )

    async def get_memberships_by_user_id(self, user_id: int):
        try:
            memberships_query = Memberships.filter(user_id=user_id)
            memberships_data = await MembershipPydantic.from_queryset(memberships_query)
            memberships_dict = [
                membership.model_dump() for membership in memberships_data
            ]

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mendapatkan memberships",
                data=memberships_dict,
            )

        except Exception as e:
            logging.error(
                f"Terjadi error saat mengambil data memberships dengan User ID {user_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengambil data memberships", str(e)],
            )

    async def update_membership(
        self, membership_id: int, membership_data: MembershipUpdate
    ):
        try:
            membership = await Memberships.get_or_none(id=membership_id)
            if not membership:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=[
                        f"Membership dengan ID {membership_id} tidak ditemukan",
                        str(e),
                    ],
                )

            await Memberships.filter(id=membership_id).update(
                **membership_data.model_dump()
            )

            updated_membership = await MembershipPydantic.from_tortoise_orm(
                await Memberships.get(id=membership_id)
            )

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Membership berhasil diupdate",
                data=updated_membership.model_dump(),
            )
        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(
                f"Terjadi error saat memperbarui membership dengan ID {membership_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat memperbarui membership", str(e)],
            )

    async def delete_membership(self, membership_id: int):
        try:
            membership = await Memberships.filter(id=membership_id).first()
            if not membership:
                raise HTTPException(
                    status_code=404, detail=["Membership tidak ditemukan"]
                )

            await membership.delete()

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil menghapus membership",
                data={},
            )
        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(
                f"Terjadi error saat menghapus membership dengan ID {membership_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat menghapus membership", str(e)],
            )
