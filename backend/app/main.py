"""
Construction
"""

from fastapi import FastAPI

from backend.models.user import UserRegister
from database.tenant_manager import TenantDatabaseManager

app = FastAPI()

manager = TenantDatabaseManager()


@app.post("/register")
async def create_user(user: UserRegister):
    data = user.model_dump()
    manager.create_tenant(data["user"], data["email"])
    return {"message": "User created", "user": data["user"]}
