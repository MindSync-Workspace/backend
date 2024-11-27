# app/models/notes.py
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Whatsapps(models.Model):
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=20, unique=True, null=True, default=None)
    secret_key = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyField(
        "models.Users", related_name="whatsapps", null=True, default=None
    )
    org = fields.ForeignKeyField(
        "models.Organizations", related_name="whatsapps", null=True, default=None
    )

    class Meta:
        table = "whatsapps"

    def __str__(self):
        return self.text


# Create Pydantic models for API
WhatsappPydantic = pydantic_model_creator(Whatsapps, name="Whatsapp")
