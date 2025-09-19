from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    target_language = Column(String)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

class ErrorCorrection(Base):
    __tablename__ = "error_corrections"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    error_type = Column(String)
    original_text = Column(String)
    corrected_text = Column(String)

# Pydantic schemas
class CorrectionRequest(BaseModel):
    input_text: str
    language: str

class CoachingRequest(BaseModel):
    input_text: str
    language: str

class STTRequest(BaseModel):
    audio: bytes
    language: str

class TTSRequest(BaseModel):
    text: str
    language: str

class AvatarRequest(BaseModel):
    text: str
    language: str
