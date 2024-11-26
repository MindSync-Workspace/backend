from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.memberships import Memberships
from tortoise.exceptions import DoesNotExist
import logging

MembershipPydantic = pydantic_model_creator(Memberships, name="Membership")


async def validate_org_access(org_id: str, user_id: str) -> bool:
    try:
        access = await Memberships.filter(org_id=org_id, user_id=user_id).exists()
        return access
    except DoesNotExist:
        return False
    except Exception as e:
        logging.error(f"Error saat memvalidasi akses membership: {e}")
        return False
