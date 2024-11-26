# app/models/chats.py
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Chats(models.Model):
    id = fields.IntField(pk=True)
    document = fields.ForeignKeyField("models.Documents", related_name="chats")
    user = fields.ForeignKeyField("models.Users", related_name="chats")
    org = fields.ForeignKeyField("models.Organizations", related_name="chats")
    token_identifier = fields.CharField(max_length=255)
    is_human = fields.BooleanField()
    text = fields.CharField(max_length=255)

    class Meta:
        table = "chats"
        unique_together = (("org", "user", "document"),)

    def __str__(self):
        return f"Chat {self.id} for Document {self.document_id}"


# Create Pydantic models for API
ChatPydantic = pydantic_model_creator(Chats, name="Chat")
