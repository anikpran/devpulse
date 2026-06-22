from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import github, stats
from app.database import engine, Base
from app.models import user, github_event


Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevPulse", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(github.router, prefix="/github", tags=["github"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])


@app.get("/")
def root():
    return {"message": "DevPulse is running"}
