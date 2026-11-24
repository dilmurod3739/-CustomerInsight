import os
import shutil
import pandas as pd
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.models.models import DatasetRecord
from backend.ml.trainer import clean_data, train_and_evaluate
from backend.schemas.schemas import DatasetSummary

router = APIRouter(prefix="/dataset", tags=["Dataset Operations"])
DEFAULT_DATA_PATH = "data/Telco-Customer-Churn.csv"

@router.get("/summary")
def get_dataset_summary():
    if not os.path.exists(DEFAULT_DATA_PATH):
        raise HTTPException(status_code=404, detail="Dataset fayli topilmadi.")

    df = pd.read_csv(DEFAULT_DATA_PATH)
    total_customers = len(df)
    
    # Calculate key EDA metrics
    churn_counts = df["Churn"].value_counts().to_dict()
    churned = churn_counts.get("Yes", 0)
    active = churn_counts.get("No", 0)
    churn_rate = round((churned / total_customers) * 100, 2) if total_customers > 0 else 0.0

    avg_monthly = round(float(df["MonthlyCharges"].mean()), 2)
    avg_tenure = round(float(df["tenure"].mean()), 1)

    contract_dist = df["Contract"].value_counts().to_dict()
    internet_dist = df["InternetService"].value_counts().to_dict()
    payment_dist = df["PaymentMethod"].value_counts().to_dict()

    # Churn rates by segment
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

@router.post("/upload")
async def upload_custom_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Faqat CSV formatidagi fayllar qabul qilinadi.")

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    save_path = os.path.join(upload_dir, file.filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        df = pd.read_csv(save_path)
        required_cols = {"tenure", "MonthlyCharges", "Contract", "Churn"}
        if not required_cols.issubset(set(df.columns)):
            os.remove(save_path)
            raise HTTPException(
                status_code=400,
                detail=f"Fayl strukturasi mos emas. Kamida quyidagi ustunlar bo'lishi shart: {required_cols}"
            )

        # Log to DB
        record = DatasetRecord(
            filename=file.filename,
            file_path=save_path,
            row_count=len(df),
            col_count=len(df.columns)
        )
        db.add(record)
        db.commit()

        # Re-train model with new dataset
        train_and_evaluate(save_path)

        return {
            "message": "Dataset muvaffaqiyatli yuklandi va yangi model o'qitildi!",
            "rows": len(df),
            "columns": len(df.columns),
            "filename": file.filename
        }
    except Exception as e:
        if os.path.exists(save_path):
            os.remove(save_path)
        raise HTTPException(status_code=500, detail=f"Faylni qayta ishlashda xatolik: {str(e)}")
