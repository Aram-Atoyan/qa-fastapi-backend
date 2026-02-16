from fastapi import FastAPI
from routes import router

app = FastAPI(title="Q&A Backend API")

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(router)