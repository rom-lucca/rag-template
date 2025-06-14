from fastapi import APIRouter, Header, HTTPException

router = APIRouter()

@router.get("/")
def ask_question(auhtorization: str = Header(...)):
    if not auhtorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization token format.")
    
    token = auhtorization.replace("Bearer ", "")

    from app.auth.token_manager import verify_token
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    
    return {"message": "Token is valid, you can ask your question."}