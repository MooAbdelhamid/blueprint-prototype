from fastapi import FastAPI

app = FastAPI()

users = []


@app.post("/users")
def create_user(name: str):
    users.append(name)
    return {"users": users}


@app.get("/users")
def get_users():
    return {"users": users}
