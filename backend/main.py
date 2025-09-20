from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Dict
from agents import TextCorrector, FeedbackGenerator

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# In-memory user storage (replace with DB in production)
users: Dict[str, str] = {}  # username -> hashed_password

class RegisterRequest(BaseModel):
    username: str
    password: str

class CorrectionRequest(BaseModel):
    text: str
    language: str

def fake_hash_password(password: str) -> str:
    # Replace with real hash function!
    return "hashed_" + password

def authenticate_user(username: str, password: str) -> bool:
    hashed = fake_hash_password(password)
    return users.get(username) == hashed

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    # In production, validate JWT. Here, token is username.
    if token in users:
        return token
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.post("/register")
def register(data: RegisterRequest):
    if data.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[data.username] = fake_hash_password(data.password)
    return {"msg": "User registered successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if authenticate_user(form_data.username, form_data.password):
        # Issue JWT in production; here, return username as token
        return {"token": form_data.username}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/correct")
def correct(data: CorrectionRequest, user: str = Depends(get_current_user)):
    corrector = TextCorrector()
    feedbacker = FeedbackGenerator()
    correction = corrector.correct(data.text, data.language)
    tips = feedbacker.generate(data.text, data.language)
    return {
        "correction": correction,
        "tips": tips
    }