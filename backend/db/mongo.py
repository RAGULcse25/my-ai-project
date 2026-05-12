import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_db():
    uri = os.getenv("MONGODB_URI")
    if not uri or uri == "your_mongodb_atlas_uri_here":
        print("⚠️  Warning: MONGODB_URI not set or is default.")
        return None
    
    try:
        client = MongoClient(uri)
        # Force a connection check
        client.admin.command('ping')
        return client["seads_db"]
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        return None

# Global DB Instance
db = get_db()