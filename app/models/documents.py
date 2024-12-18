from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import os


class Documents(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    summary = fields.TextField(null=True)
    org_id = fields.CharField(max_length=255, null=True)
    file_path = fields.CharField(max_length=255)
    encryption_key = fields.CharField(max_length=500, null=True)
    file_size = fields.IntField(null=True)
    extension_type = fields.CharField(max_length=10, null=True)
    user = fields.ForeignKeyField("models.Users", related_name="documents", null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "documents"

    def __str__(self):
        return self.title


DocumentPydantic = pydantic_model_creator(Documents, name="Document")
