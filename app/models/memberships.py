# app/models/memberships.py
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Memberships(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyField("models.Users", related_name="memberships")
    org = fields.ForeignKeyField("models.Organizations", related_name="memberships")

    class Meta:
        table = "memberships"
        unique_together = (("org", "user"),)  # Unique constraint for orgId and userId

    def __str__(self):
        return f"{self.user} in {self.org}"


# Create Pydantic models for API
MembershipPydantic = pydantic_model_creator(Memberships, name="Membership")
