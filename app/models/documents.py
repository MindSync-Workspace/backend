# app/models/documents.py
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Documents(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255, null=True)
    token_identifier = fields.CharField(max_length=255, null=True)
    org_id = fields.CharField(max_length=255, null=True)
    embedding = fields.JSONField(null=True, default=None)
    file_id = fields.CharField(max_length=255)  # Assuming fileId is a string
    user = fields.ForeignKeyField("models.Users", related_name="documents", null=True)  # Relasi ke Users

    class Meta:
        table = "documents"

    def __str__(self):
        return self.title


# Create Pydantic models for API
DocumentPydantic = pydantic_model_creator(Documents, name="Document")