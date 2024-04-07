from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient("mongodb://localhost:27017/")
db = client["buildManager"]
sessions_collection = db["session"]
owner_collection = db["Owners"]


def update_user_session(user_id):
    now = datetime.now()
    expires_at = now + timedelta(days=1)  # expiration après 1 jour
    # Mets à jour le document de session
    sessions_collection.update_one(
        {"session_key": "unique_session"},
        {"$set": {
            "session_id": user_id,
            "created_at": now,
            "expires_at": expires_at
        }},
        upsert=True
    )


def get_current_user_id():
    session = sessions_collection.find_one({"session_key": "unique_session"})
    if session and session["expires_at"] > datetime.now():

        return session["session_id"]
    else:
        return None


def get_current_user_building_ids():
    user_id = get_current_user_id()
    if user_id:
        owner = owner_collection.find_one({"_id": user_id})
        if owner and "_buildings" in owner:
            building_ids = [building["_id"] for building in owner["_buildings"] if "_id" in building]
            return building_ids
        else:
            print("Aucun bâtiment associé à cet utilisateur.")
            return []
    else:
        print("Aucun utilisateur connecté ou session expirée.")
        return []
