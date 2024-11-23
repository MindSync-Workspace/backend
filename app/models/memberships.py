# app/models/memberships.py
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Memberships(models.Model):
    id = fields.IntField(pk=True)
    org_id = fields.ForeignKeyField("models.Organizations", related_name="memberships")
    user_id = fields.ForeignKeyField("models.Users", related_name="memberships")

    class Meta:
        table = "memberships"
        unique_together = (("org_id", "user_id"),)  # Unique constraint for orgId and userId

    def __str__(self):
        return f"{self.user_id} in {self.org_id}"


# Create Pydantic models for API
MembershipPydantic = pydantic_model_creator(Memberships, name="Membership")