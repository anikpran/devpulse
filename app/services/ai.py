from datetime import datetime, timezone
import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def generate_digest(
        username: str,
        streak: int,
        events: list
):
    total_push = len(events)
    unique_dates = set()
    repos = set()
    for event in events:
        unique_dates.add(event.created_at.date())
        repos.add(event.repo_name)

    summary = {
        "username": username, 
        "streak": streak,
        "total_pushes": total_push,
        "active_days": len(unique_dates),
        "repos": list(repos)
    }
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[  
            {
                "role": "user",
                "content": f"""Generate a short, encouraging weekly digest for a software engineer with this activity:
                
                Username: {summary['username']}
                Current streak: {summary['streak']} days
                Total pushes this week: {summary['total_pushes']}
                Active coding days: {summary['active_days']} out of 7
                Repos worked on: {', '.join(summary['repos'])}

                Keep it to 3-4 sentences. Be specific, encouraging, and mention the streak."""
            }
            ]   
        )
        return message.content[0].text
    except Exception:
        return "Digest unavailable - API Credits needed"