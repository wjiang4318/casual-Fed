from app.ingestion.fetch import fetch_statement
from app.llm.extract import extract_meeting
from app.ingestion.diff import get_prior_statement, diff_statements
from app.db.database import SessionLocal # only need this because this is the actual object in the file that we call tog et a session
from app.db.models import Meeting # we don't need Base (don't need to create a table) so we import meetings to create a new row
from datetime import datetime

def get_current_utc_time():
    return datetime.utcnow()

def ingest_meeting(date: str):
    date_obj = datetime.strptime(date, "%Y%m%d") 
    session = SessionLocal()
    existing = session.query(Meeting).filter_by(date=date_obj).first()
    if existing:
        session.close()
        return(f'Fed fomc for {date_obj} already exist')
    else: 
        statement = fetch_statement(date)
        extracted_info = extract_meeting(statement)
        prior_statement = get_prior_statement(date)
        
        if prior_statement:
            diff_result= diff_statements(prior_statement, statement)
        else:
            diff_result = None
        try:
            meeting = Meeting( 
            date=date_obj, 
            decision=extracted_info.decision,
            magnitude_bps=extracted_info.magnitude_bps,
            tone=extracted_info.tone,
            tone_confidence=extracted_info.tone_confidence,
            statement_text=statement,
            created_at=get_current_utc_time(),
            statement_diff_json = diff_result
        )
            session.add(meeting) # knows to add to meeting because Meeting class has __tablename__ = "meetings" defined in the model:
            session.commit()
            session.refresh(meeting)
            return(f'Fed fomc for {date_obj} created')
        except Exception as e:
            session.rollback()     # undo if something breaks
            raise e
        finally:
            session.close()

if __name__ == "__main__":
    print(ingest_meeting("20260617"))