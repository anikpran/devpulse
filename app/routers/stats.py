from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.github_event import GithubEvent
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.get("/")
def stats_root():
    return {"message": "Stats router is live"}

@router.get("/{username}")
def streaks(username : str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.github_username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    events = db.query(GithubEvent).filter(GithubEvent.user_id == user.id)\
    .filter(GithubEvent.event_type == "PushEvent")\
    .filter(GithubEvent.created_at >= datetime.now(timezone.utc) - timedelta(days=90))\
    .order_by(GithubEvent.created_at).all()
    
    push_dates = set()

    for event in events:
        push_dates.add(event.created_at.date())

    if not push_dates:
        return {"streak": 0}
    
    streak = 1
    sorted_push_dates = sorted(push_dates)
    prev_date = sorted_push_dates[0]

    for date in sorted_push_dates[1:]:
        difference = (date - prev_date).days
        if (date - prev_date).days > 1:
           streak = 1
        else:
            streak += 1
        prev_date = date
        

    today = date.today()
    last_push = sorted_push_dates[-1]
    if (today - last_push).days > 1:
        return {"streak": 0}
    return {"streak": streak}






