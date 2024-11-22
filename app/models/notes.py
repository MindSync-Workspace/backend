# app/models/users.py
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Notes(models.Model):
    id = fields.IntField(pk=True)
    text = fields.CharField(max_length=255)
    user = fields.ForeignKeyField("models.Users", related_name="notes")
    embedding = fields.JSONField(null=True, default=None)
    tokenIdentifier = fields.CharField(max_length=255, null=True, default=None)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "notes"

    def __str__(self):
        return self.username


# Create Pydantic models for API
NotePydantic = pydantic_model_creator(Notes, name="Note")