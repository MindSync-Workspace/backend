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
            user = await Users.filter(username=user_data.username).first()
            if user:
                raise HTTPException(status_code=400, detail="Username sudah ada")

            user = await Users.filter(email=user_data.email).first()
            if user:
                raise HTTPException(status_code=400, detail=["Akun sudah ada"])

            user_dict = user_data.model_dump()
            user_dict["password"] = bcrypt.hash(user_dict["password"])
            user_obj = await Users.create(**user_dict)
            user_data = await UserPydantic.from_tortoise_orm(user_obj)

            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Berhasil membuat user",
                data=user_data.model_dump(),
            )
        except Exception as e:
            logging.error(f"Terjadi error saat membuat user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat membuat user", str(e)],
            )

    async def get_users(self):
        try:
            users = await UserPydantic.from_queryset(Users.all())
            users_data = [user.model_dump() for user in users]

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mengambil data semua user",
                data=users_data,
            )
        except Exception as e:
            logging.error(f"Terjadi error saat mengambil data user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat membuat data user", str(e)],
            )

    async def get_user(self, user_id: int):
        try:
            user = await Users.filter(id=user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User tidak ditemukan")

            user_data = await UserPydantic.from_tortoise_orm(user)

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mengambil data user",
                data=user_data.model_dump(),
            )
        except Exception as e:
            logging.error(
                f"Terjadi error saat mengambil data user dengan User ID {user_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengambil data user", str(e)],
            )

    async def update_user(self, user_id: int, user_data: UserUpdate):
        try:
            user = await Users.filter(id=user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User tidak ditemukan")

            update_data = user_data.model_dump(exclude_unset=True)
            if "password" in update_data:
                update_data["password"] = bcrypt.hash(update_data["password"])

            await Users.filter(id=user_id).update(**update_data)
            updated_user = await UserPydantic.from_tortoise_orm(
                await Users.get(id=user_id)
            )

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mengupdate data user",
                data=updated_user.model_dump(),
            )
        except Exception as e:
            logging.error(
                f"Terjadi error saat mengupdate user dengan User ID {user_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat mengupdate user", str(e)],
            )

    async def delete_user(self, user_id: int):
        try:
            user = await Users.filter(id=user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User tidak ditemukan")

            await user.delete()

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil menghapus user",
                data={},
            )
        except Exception as e:
            logging.error(
                f"Terjadi error saat menghapus user dengan User ID {user_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat menghapus user", str(e)],
            )
