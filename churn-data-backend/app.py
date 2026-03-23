from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# -----------------------------
# Load model safely (IMPORTANT)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "churn_model.pkl"))
threshold = joblib.load(os.path.join(BASE_DIR, "churn_threshold.pkl"))

# -----------------------------
# App init (ONLY ONCE)
# -----------------------------
app = FastAPI()

# -----------------------------
# CORS (Frontend access fix)
# -----------------------------
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # (later restrict to Vercel URL)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Input Schema
# -----------------------------
class Customer(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def home():
    return {"message": "Telecom Customer Churn API is running 🚀"}

@app.post("/predict")
def predict_churn(customer: Customer):
    input_df = pd.DataFrame([customer.dict()])

    prob = model.predict_proba(input_df)[0][1]
    prediction = 1 if prob >= threshold else 0

    return {
        "churn_probability": round(float(prob), 4),
        "prediction": prediction
    }