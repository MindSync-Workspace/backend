# app/models/organizations.py
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Organizations(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    description = fields.TextField(null=True)  # Deskripsi organisasi
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    start_date = fields.DatetimeField(null=True)
    end_date = fields.DatetimeField(null=True)
    class Meta:
        table = "organizations"

    def __str__(self):
        return self.name


# Create Pydantic models for API
OrganizationPydantic = pydantic_model_creator(Organizations, name="Organization")
OrganizationInPydantic = pydantic_model_creator(
    Organizations, name="OrganizationIn", exclude_readonly=True
)
OrganizationOutPydantic = pydantic_model_creator(Organizations, name="OrganizationOut")
