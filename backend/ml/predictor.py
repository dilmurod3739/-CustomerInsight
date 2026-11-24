import os
import json
import joblib
import pandas as pd
from typing import Dict, Any, List
from backend.ml.trainer import clean_data, NUMERICAL_FEATURES, CATEGORICAL_FEATURES
from backend.schemas.schemas import CustomerFeatures, PredictionResult

MODEL_PATH = "backend/ml_models/churn_pipeline.joblib"
METRICS_PATH = "backend/ml_models/model_metrics.json"

class ChurnPredictor:
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.pipeline = None
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
        else:
            self.pipeline = None

    def predict(self, customer: CustomerFeatures) -> PredictionResult:
        if self.pipeline is None:
            self.load_model()
            if self.pipeline is None:
                raise RuntimeError("Model hali o'qitilmagan. Avval modelni train qiling.")

        data_dict = customer.model_dump(exclude={"customerID"}) if hasattr(customer, "model_dump") else customer.dict(exclude={"customerID"})
        if data_dict.get("TotalCharges") is None:
            data_dict["TotalCharges"] = data_dict["MonthlyCharges"] * max(1, data_dict["tenure"])

        df = pd.DataFrame([data_dict])
        df_cleaned = clean_data(df)

        proba = float(self.pipeline.predict_proba(df_cleaned)[0][1])
        prediction = "Yes" if proba >= 0.5 else "No"
        
        # Risk level
        if proba >= 0.65:
            risk_level = "High"
        elif proba >= 0.35:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # Explain key risk factors
        key_factors = []
        recommendations = []

        if customer.Contract == "Month-to-month":
            key_factors.append("Oylik qisqa muddatli shartnoma (Month-to-month)")
            recommendations.append("Uzoq muddatli (1 yoki 2 yillik) shartnomaga o'tish uchun chegirma yoki bonus taklif qilish")

        if customer.tenure < 6:
            key_factors.append(f"Mijozlik tajribasi kam (atigi {customer.tenure} oy)")
            recommendations.append("Dastlabki 6 oyda faol onboarding va xizmat sifatini monitoring qilish")

        if customer.InternetService == "Fiber optic" and customer.TechSupport == "No":
            key_factors.append("Yuqori narxli optik tolali internet bor, lekin texnik yordam olinmagan")
            recommendations.append("Bepul 1 oylik Premium TechSupport va xavfsizlik paketini taqdim etish")

        if customer.PaymentMethod == "Electronic check":
            key_factors.append("Elektron chek orqali to'lov (ushbu toifada ketish xavfi yuqori)")
            recommendations.append("Avtomatik bank yoki karta to'lov tizimiga ulash va 5% keshbek berish")

        if customer.MonthlyCharges > 80:
            key_factors.append(f"Oylik to'lov yuqori (${customer.MonthlyCharges:.2f})")
            recommendations.append("Xizmat tarifini optimallashtirish yoki chegirmali oilaviy paket taklif etish")

        if not key_factors:
            key_factors.append("Muntazam to'lovchi, barqaror mijoz profiliga ega")
            recommendations.append("Muntazam sodiqlik dasturi (loyalty points) orqali rag'batlantirish")

        return PredictionResult(
            customerID=customer.customerID or "UNKNOWN",
            churn_probability=round(proba, 4),
            churn_prediction=prediction,
            risk_level=risk_level,
            key_factors=key_factors,
            retention_recommendations=recommendations
        )

predictor = ChurnPredictor()
