from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def stats_root():
    return {"message": "Stats router is live"}