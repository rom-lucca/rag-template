from fastapi import FastAPI

from app.db.database import Base, engine
from app.models import users
from app.api import routes_ask, routes_auth, routes_result

app = FastAPI(title="RAG Microservice", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(routes_auth.router, prefix="/auth", tags=["Auth"])
app.include_router(routes_ask.router, prefix="/ask", tags=["Ask"])
app.include_router(routes_result.router, prefix="/result", tags=["Result"])

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "RAG Microservice is running."}