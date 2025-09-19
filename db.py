from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Session, ErrorCorrection
from datetime import datetime, timedelta
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_session(user_id, db):
    new_session = Session(user_id=user_id, start_time=datetime.utcnow())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session.id

def get_user_progress(user_id, db):
    # Example: return total sessions, errors, speaking time
    total_sessions = db.query(Session).filter(Session.user_id == user_id).count()
    total_errors = db.query(ErrorCorrection).join(Session).filter(Session.user_id == user_id).count()
    total_time = timedelta()
    sessions = db.query(Session).filter(Session.user_id == user_id).all()
    for s in sessions:
        if s.end_time and s.start_time:
            total_time += s.end_time - s.start_time
    return {
        "user_id": user_id,
        "total_sessions": total_sessions,
        "total_errors": total_errors,
        "total_speaking_time_seconds": int(total_time.total_seconds())
    }
