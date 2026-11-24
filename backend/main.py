import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.core.database import Base, engine
from backend.models import models
from backend.api import auth, predict, dataset, bot_api
from backend.ml.trainer import train_and_evaluate
from backend.ml.predictor import predictor

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Database Tables
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized.")

    # Check if model is trained, else train it
    model_path = "backend/ml_models/churn_pipeline.joblib"
    dataset_path = "data/Telco-Customer-Churn.csv"
    if not os.path.exists(model_path) and os.path.exists(dataset_path):
        print("Model mavjud emas. Dastlabki model o'qitilmoqda...")
        train_and_evaluate(dataset_path)
        predictor.load_model()
        print("Model muvaffaqiyatli o'qitildi va yuklandi.")
    else:
        predictor.load_model()
        print("Mavjud model yuklandi.")

    yield
    print("Application shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="CustomerInsight — Mijozlar xatti-harakati va ketish xavfini (Customer Churn) tahlil qilish platformasi API",
    lifespan=lifespan
)

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routerlar
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(dataset.router, prefix=settings.API_V1_STR)
app.include_router(predict.router, prefix=settings.API_V1_STR)
app.include_router(bot_api.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
