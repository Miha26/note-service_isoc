from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
import os
from pymongo import MongoClient

app = FastAPI()

# Conectare la MongoDB local (port diferit pentru container separat în viitor)
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["notes_db"]  # sau tags_db în funcție de serviciu
notes_collection = db["notes"]

class Note(BaseModel):
    title: str
    content: str
    user_id: str  # legătura cu utilizatorul

@app.post("/note")
def create_note(note: Note):
    result = notes_collection.insert_one(note.dict())
    return {"message": "Note created", "note_id": str(result.inserted_id)}

@app.get("/notes/{user_id}")
def get_notes(user_id: str):
    notes = list(notes_collection.find({"user_id": user_id}))
    for note in notes:
        note["_id"] = str(note["_id"])  # convertim ObjectId în string
    return notes

@app.delete("/note/{note_id}")
def delete_note(note_id: str):
    result = notes_collection.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted"}
