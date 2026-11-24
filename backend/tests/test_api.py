from backend.main import root
from backend.api.dataset import get_dataset_summary, get_dataset_sample
from backend.api.predict import get_model_metrics, predict_single_customer
from backend.schemas.schemas import CustomerFeatures
from backend.core.database import SessionLocal, Base, engine

def test_all():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Root test
    r = root()
    assert r["status"] == "online"

    # Dataset summary test
    summary = get_dataset_summary()
    assert summary["total_customers"] == 7043
    assert summary["churn_rate"] > 0

    # Dataset sample test
    sample = get_dataset_sample(limit=5)
    assert len(sample["data"]) == 5

    # Metrics test
    metrics = get_model_metrics()
    assert "accuracy" in metrics
    assert metrics["accuracy"] > 0.7

    # Prediction test
    feat = CustomerFeatures(
        customerID="TEST-100",
        tenure=1,
        MonthlyCharges=90.0,
        Contract="Month-to-month",
        InternetService="Fiber optic",
        PaymentMethod="Electronic check"
    )
    result = predict_single_customer(feat, db=db)
    assert result.churn_prediction in ["Yes", "No"]
    assert result.risk_level in ["High", "Medium", "Low"]

    db.close()
    print("Testlar muvaffaqiyatli yakunlandi! (100% PASS)")

if __name__ == "__main__":
    test_all()
