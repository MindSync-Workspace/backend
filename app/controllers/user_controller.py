from fastapi import HTTPException, status
from app.models.users import Users
from app.schemas.users import UserCreate, UserUpdate
from passlib.hash import bcrypt
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.response import create_response  # Corrected import path

# Define the Pydantic model for Users
User_Pydantic = pydantic_model_creator(Users, name="User", exclude=("password",))

class UserController:
    async def create_user(self, user_data: UserCreate):
        user = await Users.filter(username=user_data.username).first()
        if user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        user = await Users.filter(email=user_data.email).first()
        if user:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        user_dict = user_data.dict()
        user_dict["password"] = bcrypt.hash(user_dict["password"])
        user_obj = await Users.create(**user_dict)
        user_data = await User_Pydantic.from_tortoise_orm(user_obj)
        
        return create_response(status_code=status.HTTP_201_CREATED, message="User created successfully", data=user_data.dict())

    async def get_users(self):
        users = await User_Pydantic.from_queryset(Users.all())
        users_data = [user.dict() for user in users]
        
        return create_response(status_code=status.HTTP_200_OK, message="Users fetched successfully", data=users_data)

    async def get_user(self, user_id: int):
        user = await Users.filter(id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = await User_Pydantic.from_tortoise_orm(user)
        
        return create_response(status_code=status.HTTP_200_OK, message="User fetched successfully", data=user_data.dict())

    async def update_user(self, user_id: int, user_data: UserUpdate):
        user = await Users.filter(id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        update_data = user_data.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = bcrypt.hash(update_data["password"])
        
        await Users.filter(id=user_id).update(**update_data)
        updated_user = await User_Pydantic.from_tortoise_orm(await Users.get(id=user_id))
        
        return create_response(status_code=status.HTTP_200_OK, message="User updated successfully", data=updated_user.dict())

    async def delete_user(self, user_id: int):
        user = await Users.filter(id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        await user.delete()
        
        return create_response(status_code=status.HTTP_200_OK, message="User deleted successfully", data={})
