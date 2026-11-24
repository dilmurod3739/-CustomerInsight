from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="analyst")  # admin, analyst, viewer
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    datasets = relationship("DatasetRecord", back_populates="owner")
    predictions = relationship("PredictionRecord", back_populates="user")
    bot_links = relationship("BotLink", back_populates="user")

class DatasetRecord(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    row_count = Column(Integer, default=0)
    col_count = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    owner = relationship("User", back_populates="datasets")

class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(100), index=True, nullable=True)
    tenure = Column(Integer, nullable=False)
    monthly_charges = Column(Float, nullable=False)
    total_charges = Column(Float, nullable=False)
    contract = Column(String(50), nullable=False)
    internet_service = Column(String(50), nullable=False)
    tech_support = Column(String(50), nullable=False)
    online_security = Column(String(50), nullable=False)
    payment_method = Column(String(100), nullable=False)
    churn_risk_score = Column(Float, nullable=False)  # 0.0 to 1.0 (probability)
    churn_prediction = Column(String(10), nullable=False)  # "Yes" or "No"
    risk_level = Column(String(20), nullable=False)  # "Low", "Medium", "High"
    key_factors = Column(Text, nullable=True)  # JSON or comma-separated string
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="predictions")

class BotLink(Base):
    __tablename__ = "bot_links"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    telegram_chat_id = Column(String(100), unique=True, index=True, nullable=False)
    link_code = Column(String(50), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="bot_links")
