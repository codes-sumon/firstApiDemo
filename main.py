from fastapi import FastAPI
from database import Base, engine
from routers import auth_router, userProfile, workStation_router
from models import user

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI JWT Auth Example")

# Include authentication router
app.include_router(auth_router.router)
app.include_router(userProfile.router)
app.include_router(workStation_router.router)


@app.get("/")
def home():
    return {"message": "Welcome to FastAPI JWT Authentication API"}

