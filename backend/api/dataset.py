import os
import shutil
import pandas as pd
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.models.models import DatasetRecord
from backend.ml.trainer import clean_data, train_and_evaluate
from backend.schemas.schemas import DatasetSummary, CustomerFeatures
from backend.ml.predictor import predictor

router = APIRouter(prefix="/dataset", tags=["Dataset Operations"])
DEFAULT_DATA_PATH = "data/Telco-Customer-Churn.csv"

@router.get("/summary")
def get_dataset_summary():
    if not os.path.exists(DEFAULT_DATA_PATH):
        raise HTTPException(status_code=404, detail="Dataset fayli topilmadi.")

    df = pd.read_csv(DEFAULT_DATA_PATH)
    total_customers = len(df)
    
    churn_counts = df["Churn"].value_counts().to_dict()
    churned = churn_counts.get("Yes", 0)
    active = churn_counts.get("No", 0)
    churn_rate = round((churned / total_customers) * 100, 2) if total_customers > 0 else 0.0

    avg_monthly = round(float(df["MonthlyCharges"].mean()), 2)
    avg_tenure = round(float(df["tenure"].mean()), 1)

    contract_dist = df["Contract"].value_counts().to_dict()
    internet_dist = df["InternetService"].value_counts().to_dict()
    payment_dist = df["PaymentMethod"].value_counts().to_dict()

    churn_by_contract = df.groupby("Contract")["Churn"].apply(lambda s: round((s == "Yes").mean() * 100, 1)).to_dict()
    churn_by_internet = df.groupby("InternetService")["Churn"].apply(lambda s: round((s == "Yes").mean() * 100, 1)).to_dict()
    churn_by_senior = df.groupby("SeniorCitizen")["Churn"].apply(lambda s: round((s == "Yes").mean() * 100, 1)).to_dict()

    return {
        "total_customers": total_customers,
        "churn_rate": churn_rate,
        "active_customers": active,
        "churned_customers": churned,
        "avg_monthly_charges": avg_monthly,
        "avg_tenure": avg_tenure,
        "contract_distribution": contract_dist,
        "internet_distribution": internet_dist,
        "payment_distribution": payment_dist,
        "churn_by_contract": churn_by_contract,
        "churn_by_internet": churn_by_internet,
        "churn_by_senior": churn_by_senior
    }

@router.get("/customer/{customer_id}")
def get_customer_by_id(customer_id: str):
    """Mijoz identifikatori bo'yicha tahlil natijasini olish"""
    if not os.path.exists(DEFAULT_DATA_PATH):
        raise HTTPException(status_code=404, detail="Dataset topilmadi.")

    df = pd.read_csv(DEFAULT_DATA_PATH)
    match = df[df["customerID"].astype(str).str.upper() == customer_id.strip().upper()]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"Mijoz topilmadi: {customer_id}")

    row = match.iloc[0].fillna("").to_dict()

    try:
        total_charges = float(str(row.get("TotalCharges", 0)).strip() or 0)
    except:
        total_charges = float(row.get("MonthlyCharges", 50.0)) * max(1, int(row.get("tenure", 1)))

    features = CustomerFeatures(
        customerID=str(row.get("customerID")),
        gender=str(row.get("gender", "Female")),
        SeniorCitizen=int(row.get("SeniorCitizen", 0)),
        Partner=str(row.get("Partner", "No")),
        Dependents=str(row.get("Dependents", "No")),
        tenure=int(row.get("tenure", 1)),
        PhoneService=str(row.get("PhoneService", "Yes")),
        MultipleLines=str(row.get("MultipleLines", "No")),
        InternetService=str(row.get("InternetService", "DSL")),
        OnlineSecurity=str(row.get("OnlineSecurity", "No")),
        OnlineBackup=str(row.get("OnlineBackup", "No")),
        DeviceProtection=str(row.get("DeviceProtection", "No")),
        TechSupport=str(row.get("TechSupport", "No")),
        StreamingTV=str(row.get("StreamingTV", "No")),
        StreamingMovies=str(row.get("StreamingMovies", "No")),
        Contract=str(row.get("Contract", "Month-to-month")),
        PaperlessBilling=str(row.get("PaperlessBilling", "Yes")),
        PaymentMethod=str(row.get("PaymentMethod", "Electronic check")),
        MonthlyCharges=float(row.get("MonthlyCharges", 50.0)),
        TotalCharges=total_charges
    )

    pred = predictor.predict(features)
    return {
        "found": True,
        "customer": row,
        "analysis": pred.model_dump()
    }

@router.get("/weekly-report")
def get_weekly_segmentation_report():
    """Haftalik mijozlar segmentatsiyasi hisoboti"""
    if not os.path.exists(DEFAULT_DATA_PATH):
        raise HTTPException(status_code=404, detail="Dataset topilmadi.")

    df = pd.read_csv(DEFAULT_DATA_PATH)
    total = len(df)
    churn_rate = round((df["Churn"] == "Yes").mean() * 100, 1)

    # Segments
    m2m = df[df["Contract"] == "Month-to-month"]
    m2m_churn = round((m2m["Churn"] == "Yes").mean() * 100, 1)

    fiber = df[df["InternetService"] == "Fiber optic"]
    fiber_churn = round((fiber["Churn"] == "Yes").mean() * 100, 1)

    seniors = df[df["SeniorCitizen"] == 1]
    seniors_churn = round((seniors["Churn"] == "Yes").mean() * 100, 1)

    two_yr = df[df["Contract"] == "Two year"]
    two_yr_churn = round((two_yr["Churn"] == "Yes").mean() * 100, 1)

    return {
        "period": "Haftalik yakuniy hisobot",
        "total_customers": total,
        "overall_churn_rate": churn_rate,
        "critical_segments": [
          {
            "segment": "Month-to-month shartnomalari",
            "customers": len(m2m),
            "churn_rate": m2m_churn,
            "risk_level": "Yuqori (Kritik)",
            "priority_action": "1 yillik shartnomaga o'tish uchun 15% chegirma va bonus taqdim etish"
          },
          {
            "segment": "Fiber optic foydalanuvchilari",
            "customers": len(fiber),
            "churn_rate": fiber_churn,
            "risk_level": "Yuqori",
            "priority_action": "Texnik yordam (TechSupport) xizmatini bepul 1 oy sinovga berish"
          },
          {
            "segment": "Katta yoshli fuqarolar (Senior Citizen)",
            "customers": len(seniors),
            "churn_rate": seniors_churn,
            "risk_level": "O'rta-Yuqori",
            "priority_action": "Soddalashtirilgan to'lov va maxsus qo'llab-quvvatlash liniyasini ulash"
          },
          {
            "segment": "2 yillik shartnomalar (Sodiq mijozlar)",
            "customers": len(two_yr),
            "churn_rate": two_yr_churn,
            "risk_level": "Juda past (Benchmark)",
            "priority_action": "Sodiqlik ballari va minnatdorchilik dasturini faollashtirish"
          }
        ]
    }

@router.get("/sample")
def get_dataset_sample(limit: int = 50, offset: int = 0, churn: Optional[str] = None):
    if not os.path.exists(DEFAULT_DATA_PATH):
        raise HTTPException(status_code=404, detail="Dataset topilmadi.")

    df = pd.read_csv(DEFAULT_DATA_PATH)
    if churn and churn in ["Yes", "No"]:
        df = df[df["Churn"] == churn]

    total = len(df)
    sample_df = df.iloc[offset:offset + limit].fillna("")
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "columns": list(df.columns),
        "data": sample_df.to_dict(orient="records")
    }
