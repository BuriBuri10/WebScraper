from fastapi import FastAPI
from api.routes import persona, downloader

app = FastAPI()
app.include_router(persona.router, prefix="/api", tags=["Persona"])
app.include_router(downloader.router, prefix="/api", tags=["Download"])

@app.get("/")
def root():
    return {"message": "API is working!"}
