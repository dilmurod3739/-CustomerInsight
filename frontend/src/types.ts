export interface DatasetSummary {
  total_customers: number;
  churn_rate: number;
  active_customers: number;
  churned_customers: number;
  avg_monthly_charges: number;
  avg_tenure: number;
  contract_distribution: Record<string, number>;
  internet_distribution: Record<string, number>;
  payment_distribution: Record<string, number>;
  churn_by_contract: Record<string, number>;
  churn_by_internet: Record<string, number>;
  churn_by_senior: Record<string, number>;
}

export interface CustomerFeatures {
  customerID?: string;
  gender: string;
  SeniorCitizen: number;
  Partner: string;
  Dependents: string;
  tenure: number;
  PhoneService: string;
  MultipleLines: string;
  InternetService: string;
  OnlineSecurity: string;
  OnlineBackup: string;
  DeviceProtection: string;
  TechSupport: string;
  StreamingTV: string;
  StreamingMovies: string;
  Contract: string;
  PaperlessBilling: string;
  PaymentMethod: string;
  MonthlyCharges: number;
  TotalCharges?: number;
}

export interface PredictionResult {
  customerID: string;
  churn_probability: number;
  churn_prediction: 'Yes' | 'No';
  risk_level: 'High' | 'Medium' | 'Low';
  key_factors: string[];
  retention_recommendations: string[];
}

export interface ModelMetrics {
  model_name: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  roc_auc: number;
  confusion_matrix: number[][];
  total_samples: number;
  train_samples: number;
  test_samples: number;
  top_feature_importances: { feature: string; importance: number }[];
}

export interface PredictionHistoryItem {
  id: number;
  customer_id: string;
  tenure: number;
  monthly_charges: number;
  contract: string;
  internet_service: string;
  churn_risk_score: number;
  churn_prediction: string;
  risk_level: string;
  key_factors: string[];
  created_at: string;
}
