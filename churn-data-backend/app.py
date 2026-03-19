from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Load model and threshold
model = joblib.load("churn_model.pkl")
threshold = joblib.load("churn_threshold.pkl")

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development (later restrict)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Define Input Schema
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