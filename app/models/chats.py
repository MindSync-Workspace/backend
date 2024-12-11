# app/models/chats.py
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Chats(models.Model):
    id = fields.IntField(pk=True)
    document = fields.ForeignKeyField("models.Documents", related_name="chats")
    text = fields.TextField()
    is_human = fields.BooleanField()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyField("models.Users", related_name="chats")
    org = fields.ForeignKeyField(
        "models.Organizations", related_name="chats", null=True, default=None
    )

    class Meta:
        table = "chats"

    def __str__(self):
        return f"Chat {self.id} for Document {self.document_id}"


# Create Pydantic models for API
ChatPydantic = pydantic_model_creator(Chats, name="Chat")
