from fastapi import APIRouter, Depends
from utils.dependencies import get_current_user
from schemas.user import UserResponse

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/me", response_model=UserResponse)
def read_profile(current_user = Depends(get_current_user)):
    # current_user is already validated and retrieved from DB
    return current_user
