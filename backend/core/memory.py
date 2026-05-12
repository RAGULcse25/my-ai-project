from db.mongo import get_db
from datetime import datetime

def save_plan(project_idea: str, plan: dict):
    db = get_db()
    if db is None:
        print("💾 DB not connected. Plan not saved to MongoDB.")
        return None
        
    doc = {
        "idea": project_idea,
        "plan": plan,
        "status": "planned",
        "created_at": datetime.utcnow()
    }
    result = db["projects"].insert_one(doc)
    print(f"💾 Plan saved to MongoDB: {result.inserted_id}")
    return str(result.inserted_id)

def get_all_projects():
    db = get_db()
    if db is None:
        return []
    return list(db["projects"].find({}, {"_id": 0}))
