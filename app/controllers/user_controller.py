from fastapi import HTTPException, status
from app.models.users import Users
from app.schemas.users import UserCreate, UserUpdate
from passlib.hash import bcrypt
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.response import create_response
import logging

UserPydantic = pydantic_model_creator(Users, name="User", exclude=("password",))


class UserController:
    async def create_user(self, user_data: UserCreate):
        try:
            existing_user = await Users.filter(username=user_data.username).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=["Username sudah ada"],
                )

            existing_email = await Users.filter(email=user_data.email).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=["Email sudah digunakan"],
                )

            user_dict = user_data.model_dump()
            user_dict["password"] = bcrypt.hash(user_dict["password"])
            user_obj = await Users.create(**user_dict)
            user_data = await UserPydantic.from_tortoise_orm(user_obj)

            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="User berhasil dibuat",
                data=user_data.model_dump(),
            )
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            logging.error(f"Error saat membuat user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat membuat user", str(e)],
            )

    async def get_users(self):
        try:
            users_query = Users.all()
            users_data = await UserPydantic.from_queryset(users_query)
            users_dict = [user.model_dump() for user in users_data]

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mendapatkan semua user",
                data=users_dict,
            )
        except Exception as e:
            logging.error(f"Error saat mengambil data user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengambil data user", str(e)],
            )

    async def get_user(self, user_id: int):
        try:
            user = await Users.get_or_none(id=user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=[f"User dengan ID {user_id} tidak ditemukan"],
                )

            user_data = await UserPydantic.from_tortoise_orm(user)

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mendapatkan data user",
                data=user_data.model_dump(),
            )
        except Exception as e:
            logging.error(f"Error saat mengambil data user dengan ID {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengambil data user", str(e)],
            )

    async def update_user(self, user_id: int, user_data: UserUpdate):
        try:
            user = await Users.get_or_none(id=user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=[f"User dengan ID {user_id} tidak ditemukan"],
                )

            update_data = user_data.model_dump(exclude_unset=True)
            if "password" in update_data:
                update_data["password"] = bcrypt.hash(update_data["password"])

            await Users.filter(id=user_id).update(**update_data)
            updated_user = await UserPydantic.from_tortoise_orm(
                await Users.get(id=user_id)
            )

            return create_response(
                status_code=status.HTTP_200_OK,
                message="User berhasil diperbarui",
                data=updated_user.model_dump(),
            )
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            logging.error(f"Error saat memperbarui user dengan ID {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat memperbarui user", str(e)],
            )

    async def delete_user(self, user_id: int):
        try:
            user = await Users.get_or_none(id=user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=[f"User dengan ID {user_id} tidak ditemukan"],
                )

            await user.delete()

            return create_response(
                status_code=status.HTTP_200_OK,
                message="User berhasil dihapus",
                data={},
            )
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            logging.error(f"Error saat menghapus user dengan ID {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat menghapus user", str(e)],
            )
