from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from agents.langgraph_agent import langgraph_correction_agent
from agents.autogen_agent import autogen_coaching_agent
from stt import transcribe_audio
from tts import synthesize_speech
from avatar import generate_avatar_video
from db import get_db, create_session, get_user_progress
from models import User
from auth import (
    create_access_token, get_password_hash, authenticate_user, get_current_user
)

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/register/")
def register(
    name: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    target_language: str = Form(...), 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(password)
    new_user = User(
        name=name,
        email=email,
        hashed_password=hashed_password,
        target_language=target_language
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}

@app.post("/token")
def login(
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me/")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "target_language": current_user.target_language
    }

@app.get("/protected/")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"msg": f"Hello, {current_user.name}! You are authorized."}

@app.post("/correction/")
def correction(
    input_text: str = Form(...), 
    language: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    return langgraph_correction_agent(input_text, language)

@app.post("/coaching/")
def coaching(
    input_text: str = Form(...), 
    language: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    return autogen_coaching_agent(input_text, language)

@app.post("/stt/")
async def stt(
    audio: UploadFile = File(...), 
    language: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    text = await transcribe_audio(audio, language)
    return {"transcription": text}

@app.post("/tts/")
async def tts(
    text: str = Form(...), 
    language: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    audio_bytes = synthesize_speech(text, language)
    return {"audio": audio_bytes}

@app.post("/avatar/")
async def avatar(
    text: str = Form(...), 
    language: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    video_bytes = generate_avatar_video(text, language)
    return {"video": video_bytes}

@app.post("/session/start/")
def start_session(
    user_id: int = Form(...), 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session_id = create_session(user_id, db)
    return {"session_id": session_id}

@app.get("/progress/")
def progress(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = get_user_progress(user_id, db)
    return data
