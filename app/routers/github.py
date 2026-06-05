from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.github import UserResponse, UserCreate
from typing import List
import httpx
import os

router = APIRouter()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/login")
def github_login():
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&scope=read:user,repo"
    )
    return RedirectResponse(github_auth_url)

@router.get("/callback")
async def github_callback(code: str, db: Session = Depends(get_db)):
    # exchange code for access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code
            }
        )

    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to get access token")

    # get github user info
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )

    github_user = user_response.json()

    # find or create user and save token
    user = db.query(User).filter(
        User.github_username == github_user["login"]
    ).first()

    if not user:
        user = User(
            username=github_user["login"],
            github_username=github_user["login"],
            email=github_user.get("email"),
            github_access_token=access_token
        )
        db.add(user)
    else:
        user.github_access_token = access_token
        db.add(user)

    db.commit()
    db.refresh(user)

    return {
        "message": "Github connected successfully",
        "username": user.username,
        "github_username": user.github_username,
        "access_token": access_token
    }