import httpx
from sqlalchemy.orm import Session
from app.models.github_event import GithubEvent
from datetime import datetime

GITHUB_API_URL = "https://api.github.com"

async def fetch_and_store_github_events(
        username: str,
        access_token: str, 
        user_id: int,
        db: Session
):
    #first call github api 
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_URL}/users/{username}/events",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json"
            }
        )

    if response.status_code != 200:
        raise Exception(f"Github API Error: {response.status_code}")
    
    events = response.json()

    #filter and store events of interest 
    stored = 0
    for event in events:
        if event["type"] != "PushEvent":
            continue
        
        #check if we have event
        existing = db.query(GithubEvent).filter(
            GithubEvent.event_id == event["id"]
        ).first()
        if existing:
            continue

        #create and store event

        github_event = GithubEvent(
            user_id=user_id,
            event_type=event["type"],
            repo_name=event["repo"]["name"],
            event_id=event["id"],
            created_at=datetime.strptime(
                event["created_at"], "%Y-%m-%dT%H:%M:%SZ"
            )
        )
        db.add(github_event)
        stored+=1
    
    db.commit()
    return stored

