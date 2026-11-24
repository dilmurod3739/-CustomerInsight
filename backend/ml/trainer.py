import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
)

CATEGORICAL_FEATURES = [
    "gender", "SeniorCitizen", "Partner", "Dependents",
    "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod"
]

NUMERICAL_FEATURES = ["tenure", "MonthlyCharges", "TotalCharges"]

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Drop customerID if present
    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])
        
    # TotalCharges contains empty strings for tenure == 0
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].astype(str).str.strip(), errors="coerce")
        df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"] * df["tenure"])
        
    if "SeniorCitizen" in df.columns:
        df["SeniorCitizen"] = df["SeniorCitizen"].astype(str)

    # Standardize target
    if "Churn" in df.columns:
        df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
        
    return df

def train_and_evaluate(csv_path: str, model_save_dir: str = "backend/ml_models"):
    os.makedirs(model_save_dir, exist_ok=True)
    
    df = pd.read_csv(csv_path)
    df_cleaned = clean_data(df)
    
    X = df_cleaned.drop(columns=["Churn"])
    y = df_cleaned["Churn"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERICAL_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES)
        ]
    )
    
    # Random Forest Pipeline
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight="balanced"
    )
    
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])
    
    pipeline.fit(X_train, y_train)
    
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    
    # Metrics
    metrics = {
        "model_name": "Random Forest Classifier (Balanced)",
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred)), 4),
        "recall": round(float(recall_score(y_test, y_pred)), 4),
        "f1_score": round(float(f1_score(y_test, y_pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_proba)), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "total_samples": int(len(df)),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test))
    }
    
    # Feature importances
    onehot_cols = list(pipeline.named_steps["preprocessor"].named_transformers_["cat"].get_feature_names_out(CATEGORICAL_FEATURES))
    feature_names = NUMERICAL_FEATURES + onehot_cols
    importances = pipeline.named_steps["classifier"].feature_importances_
    top_importances = sorted(
        [{"feature": f, "importance": round(float(imp), 4)} for f, imp in zip(feature_names, importances)],
        key=lambda x: x["importance"],
        reverse=True
    )[:10]
    
    metrics["top_feature_importances"] = top_importances
    
    # Save model and metadata
    pipeline_path = os.path.join(model_save_dir, "churn_pipeline.joblib")
    metrics_path = os.path.join(model_save_dir, "model_metrics.json")
    
    joblib.dump(pipeline, pipeline_path)
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"Model saved to {pipeline_path}")
    print(f"Metrics: {metrics}")
    return pipeline, metrics

if __name__ == "__main__":
    train_and_evaluate("data/Telco-Customer-Churn.csv")
