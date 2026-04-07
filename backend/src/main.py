from fastapi import FastAPI, Request
from src.app.adapters.inbound.rest.routers.auth_router import router as auth_router
from src.app.adapters.inbound.rest.routers.ideas_router import router as ideas_router
from src.app.adapters.inbound.rest.routers.logs_router import router as logs_router
from src.app.adapters.inbound.rest.routers.ratings_router import router as ratings_router
from slowapi.middleware import SlowAPIMiddleware
from src.app.adapters.inbound.rest.rate_limiter import limiter

app = FastAPI(title="Ideas Tracker API")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


app.include_router(ideas_router)
app.include_router(logs_router)
app.include_router(ratings_router)
app.include_router(auth_router)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}