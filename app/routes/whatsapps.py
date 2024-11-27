from fastapi import APIRouter, status, Header
from app.controllers.whatsapp_controller import WhatsappController
from app.schemas.whatsapps import WhatsappCreate, WhatsappResponse, WhatsappUpdate
from typing import List

router = APIRouter(prefix="/whatsapps", tags=["Whatsapps"])
whatsapp_controller = WhatsappController()


@router.post(
    "",
    response_model=WhatsappResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Connect WhatsApp to user account (**BOT**)",
)
async def connect_whatsapp(whatsapp_data: WhatsappUpdate):
    """
    Endpoint to connect a WhatsApp number to a user account.
    - **number**: The WhatsApp number to be connected to the account.
    - **secret_key**: The secret key for the user to authenticate the connection of the WhatsApp number.
    """
    return await whatsapp_controller.connect_whatsapp_to_account(whatsapp_data)


@router.delete(
    "",
    status_code=status.HTTP_200_OK,
    summary="Disconnect WhatsApp from user account",
)
async def disconnect_whatsapp(whatsapp_data: WhatsappUpdate):
    """
    Endpoint to disconnect a WhatsApp number from a user account and reset the secret key.
    - **number**: The WhatsApp number to be disconnected.
    - **secret_key**: The secret key for the user to authenticate and disconnect their WhatsApp number.
    """
    return await whatsapp_controller.disconnect_whatsapp_from_account(whatsapp_data)
