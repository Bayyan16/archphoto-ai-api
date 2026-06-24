from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.render import router as render_router

app = FastAPI(
    title="ArchPhoto AI API",
    description="Backend API for AI architectural render enhancement.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://archphoto-ai.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/storage", StaticFiles(directory="storage"), name="storage")

app.include_router(render_router, prefix="/api/v1/render", tags=["Render"])


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "ArchPhoto AI API is running",
    }