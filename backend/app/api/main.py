from fastapi import FastAPI, HTTPException
from datetime import datetime
from app.db.database import SessionLocal 
from app.db.models import Meeting
from app.schemas.meeting import MeetingResponse
from pathlib import Path
import json

app = FastAPI()

@app.get("/")
def root():
    return {"Hello: World"}

@app.get("/meetings/{date}")
def get_meeting(date:str):
    try:
        date_obj = datetime.strptime(date, "%Y%m%d")
    except ValueError:
        raise HTTPException(status_code=400, detail = "Invalid Date")
    session = SessionLocal()
    existing = session.query(Meeting).filter_by(date=date_obj).first() # search for the date
    if existing: # if existing, means we have already processed and ingested the fomc
        # we want to load each element in postgres into our MeetingResponse class. model_config in the class
        # does that for us. Pydantic can build the whole object directly
        response = MeetingResponse.model_validate(existing)
        # model_validate() look at each field declared on MeetingResponse (id, date, decision, ...) and — because 
        # from_attributes=True — tries getattr(existing, "id"), getattr(existing, "date"), etc., 
        # validating each one against the type/constraints you declared (
        session.close()
        return response
    else:
        session.close()
        raise HTTPException(status_code=404, detail = "No meetings found")


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DAG_DIR = BASE_DIR /"data"/"dag.json"
print(DAG_DIR)
@app.get("/dag")
def get_dag():
    with open(DAG_DIR, encoding = "utf-8") as f:
        dag = json.load(f)
    return dag