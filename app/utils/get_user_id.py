from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.whatsapps import Whatsapps
from fastapi import HTTPException, status

WhatsappPydantic = pydantic_model_creator(Whatsapps, name="Whatsapp")


async def get_user_id_by_whatsapp_number(number: str):

    whatsapp = await Whatsapps.get_or_none(number=number)

    if not whatsapp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=["Tolong login terlebih dahulu"],
        )

    user_id = whatsapp.user_id

    return user_id
