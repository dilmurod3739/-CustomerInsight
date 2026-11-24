from typing import Optional, List, Dict, Any
from pydantic import BaseModel

# Auth Schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Prediction Input & Output Schemas
class CustomerFeatures(BaseModel):
    gender: str = "Female"
    SeniorCitizen: int = 0
    Partner: str = "No"
    Dependents: str = "No"
    tenure: int = 12
    PhoneService: str = "Yes"
    MultipleLines: str = "No"
    InternetService: str = "Fiber optic"
    OnlineSecurity: str = "No"
    OnlineBackup: str = "No"
    DeviceProtection: str = "No"
    TechSupport: str = "No"
    StreamingTV: str = "No"
    StreamingMovies: str = "No"
    Contract: str = "Month-to-month"
    PaperlessBilling: str = "Yes"
    PaymentMethod: str = "Electronic check"
    MonthlyCharges: float = 70.0
    TotalCharges: Optional[float] = None
    customerID: Optional[str] = "NEW-001"

class PredictionResult(BaseModel):
    customerID: str
    churn_probability: float  # e.g. 0.74 (74%)
    churn_prediction: str     # "Yes" or "No"
    risk_level: str           # "High", "Medium", "Low"
    key_factors: List[str]
    retention_recommendations: List[str]

class ModelMetrics(BaseModel):
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    confusion_matrix: List[List[int]]
    feature_importances: Dict[str, float]
    total_samples: int
    train_samples: int
    test_samples: int

class DatasetSummary(BaseModel):
    total_customers: int
    churn_rate: float
    active_customers: int
    churned_customers: int
    avg_monthly_charges: float
    avg_tenure: float
    contract_distribution: Dict[str, int]
    internet_distribution: Dict[str, int]
    payment_distribution: Dict[str, int]
