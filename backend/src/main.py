from fastapi import FastAPI
from src.app.adapters.inbound.rest.routers.ideas_router import router as ideas_router

app = FastAPI(title="Ideas Tracker API")
app.include_router(ideas_router)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}