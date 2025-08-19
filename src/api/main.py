from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.schemas import ChatRequest, ChatResponse, LoginRequest, LoginResponse
from ..core.database import get_db, Base, engine
from ..core.auth import AuthService
from ..core.retrieval import RAGService

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Fitness Coach", version="1.0.0")
auth_service = AuthService()
rag_service = RAGService()

@app.event("startup")
def startup_event():
    rag_service.setup_vectorstore()

@app.post("/auth/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth_service.generate_token(user)
    return LoginResponse(access_token=token)

@app.post("/chat/ask", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        response = rag_service.query(request.query)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))