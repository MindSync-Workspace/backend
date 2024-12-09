from fastapi import HTTPException, status
from app.models.whatsapps import Whatsapps
from app.schemas.whatsapps import WhatsappCreate, WhatsappUpdate
from tortoise.contrib.pydantic import pydantic_model_creator
import logging
import cuid
from app.utils.response import create_response
from tortoise.exceptions import DoesNotExist

WhatsappPydantic = pydantic_model_creator(Whatsapps, name="Whatsapp")


class WhatsappController:

    async def create_whatsapp(self, whatsapp_data: WhatsappCreate):
        try:
            whatsapp_dict = whatsapp_data

            secret_key = cuid.cuid()
            whatsapp_dict["secret_key"] = secret_key

            whatsapp_obj = await Whatsapps.create(**whatsapp_dict)

            whatsapp_data = await WhatsappPydantic.from_tortoise_orm(whatsapp_obj)

        except Exception as e:
            logging.error(f"Error saat membuat whatsapp: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat membuat whatsapp", str(e)],
            )

    async def get_secret_key_by_user_id(self, user_id: int):
        try:
            whatsapp = await Whatsapps.filter(user_id=user_id).first()

            if not whatsapp:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=[f"Akun dengan ID {user_id} tidak ditemukan"],
                )
            whatsapp_data = await WhatsappPydantic.from_tortoise_orm(whatsapp)
            # whatsapp_dict = whatsapp_data.model_dump()

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Berhasil mendapatkan secret key",
                data=whatsapp_data.model_dump(),
            )

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(f"Error saat mengambil secret key: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Error saat mengambil secret key", str(e)],
            )

    async def connect_whatsapp_to_account(self, whatsapp_data: WhatsappUpdate):
        try:

            if not whatsapp_data.secret_key:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=["Secret key diperlukan untuk menghubungkan WhatsApp"],
                )

            whatsapp_obj = await Whatsapps.get_or_none(number=whatsapp_data.number)

            if whatsapp_obj:
                if whatsapp_obj.user_id != whatsapp_data.user_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=["Nomor WhatsApp sudah terhubung dengan pengguna lain"],
                    )

            else:
                whatsapp_obj = await Whatsapps.get(secret_key=whatsapp_data.secret_key)
                await whatsapp_obj.save()

            whatsapp_obj.number = whatsapp_data.number
            await whatsapp_obj.save()

            updated_whatsapp_data = await WhatsappPydantic.from_tortoise_orm(
                whatsapp_obj
            )

            return create_response(
                status_code=status.HTTP_200_OK,
                message="WhatsApp berhasil terhubung ke akun pengguna",
                data=updated_whatsapp_data.model_dump(),
            )
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=["Secret key tidak ditemukan atau tidak valid"],
            )

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(f"Error saat menghubungkan WhatsApp: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat menghubungkan WhatsApp", str(e)],
            )

    async def disconnect_whatsapp_from_account(self, whatsapp_data: WhatsappUpdate):
        try:
            if not whatsapp_data.number or not whatsapp_data.secret_key:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=[
                        "Nomor WhatsApp dan secret key diperlukan untuk menghapus koneksi"
                    ],
                )

            whatsapp_obj = await Whatsapps.get_or_none(number=whatsapp_data.number)

            if not whatsapp_obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Nomor WhatsApp tidak ditemukan",
                )

            if whatsapp_obj.secret_key != whatsapp_data.secret_key:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Secret key tidak valid, akses ditolak",
                )

            await whatsapp_obj.delete()

            # 5. Reset secret key (opsional) atau update status lain jika diperlukan
            # Dalam kasus ini, kita menghapus koneksi WhatsApp, jadi kita tidak perlu mereset secret_key di tempat lain.

            return create_response(
                status_code=status.HTTP_200_OK,
                message="Koneksi WhatsApp berhasil dihapus dan secret key telah direset",
                data={},
            )

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logging.error(f"Error saat menghapus koneksi WhatsApp: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Terjadi error saat menghapus koneksi WhatsApp", str(e)],
            )
