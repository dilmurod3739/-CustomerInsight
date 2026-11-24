import json
import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.core.database import get_db
from backend.models.models import PredictionRecord, User
from backend.schemas.schemas import CustomerFeatures, PredictionResult, ModelMetrics
from backend.ml.predictor import predictor, METRICS_PATH
from backend.api.auth import get_current_user

router = APIRouter(prefix="/predict", tags=["Predictions & ML"])

@router.post("/single", response_model=PredictionResult)
def predict_single_customer(
    features: CustomerFeatures,
    db: Session = Depends(get_db),
    # Optional auth: allow guest testing or logged-in users
):
    try:
        result = predictor.predict(features)
        
        # Save to DB history
        record = PredictionRecord(
            customer_id=result.customerID,
            tenure=features.tenure,
            monthly_charges=features.MonthlyCharges,
            total_charges=features.TotalCharges or (features.MonthlyCharges * max(1, features.tenure)),
            contract=features.Contract,
            internet_service=features.InternetService,
            tech_support=features.TechSupport,
            online_security=features.OnlineSecurity,
            payment_method=features.PaymentMethod,
            churn_risk_score=result.churn_probability,
            churn_prediction=result.churn_prediction,
            risk_level=result.risk_level,
            key_factors=json.dumps(result.key_factors, ensure_ascii=False)
        )
        db.add(record)
        db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bashorat qilishda xatolik: {str(e)}")

@router.get("/metrics")
def get_model_metrics():
    if not os.path.exists(METRICS_PATH):
        raise HTTPException(status_code=404, detail="Model metrikalari topilmadi. Avval modelni o'qiting.")
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    return metrics

@router.get("/history")
def get_prediction_history(limit: int = 50, db: Session = Depends(get_db)):
    records = db.query(PredictionRecord).order_by(desc(PredictionRecord.created_at)).limit(limit).all()
    out = []
    for r in records:
        factors = []
        try:
            if r.key_factors:
                factors = json.loads(r.key_factors)
        except Exception:
            factors = [r.key_factors]
        out.append({
            "id": r.id,
            "customer_id": r.customer_id,
            "tenure": r.tenure,
            "monthly_charges": r.monthly_charges,
            "contract": r.contract,
            "internet_service": r.internet_service,
            "churn_risk_score": r.churn_risk_score,
            "churn_prediction": r.churn_prediction,
            "risk_level": r.risk_level,
            "key_factors": factors,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })
    return out
