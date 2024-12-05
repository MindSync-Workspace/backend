# app/models/notes.py
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Notes(models.Model):
    id = fields.IntField(pk=True)
    text = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyField("models.Users", related_name="notes")
    org = fields.ForeignKeyField(
        "models.Organizations", related_name="notes", null=True, default=None
    )

    class Meta:
        table = "notes"

    def __str__(self):
        return self.text


# Create Pydantic models for API
NotePydantic = pydantic_model_creator(Notes, name="Note")
