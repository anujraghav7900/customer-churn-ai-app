# 🚀 Customer Churn Prediction (Full Stack AI App)

## 📌 Overview

This project is a full-stack AI application that predicts whether a telecom customer is likely to churn or not. It combines machine learning with a FastAPI backend and a React frontend to provide real-time predictions.

---

## 🎯 Problem Statement

Customer churn is a major problem for telecom companies. Retaining existing customers is more cost-effective than acquiring new ones.
This project helps identify customers who are likely to churn so that businesses can take preventive actions.

---

## 🧠 Features

* Predicts customer churn probability
* Real-time predictions using API
* Full-stack implementation (React + FastAPI)
* Machine learning pipeline with preprocessing
* Threshold tuning for business optimization

---

## 🛠️ Tech Stack

### 🔹 Machine Learning

* Scikit-learn
* Pandas
* NumPy

### 🔹 Backend

* FastAPI
* Uvicorn
* Pydantic

### 🔹 Frontend

* React.js
* Axios

---

## 📊 Dataset

* Telco Customer Churn Dataset
* ~7000 customer records
* Features include:

  * tenure
  * MonthlyCharges
  * Contract
  * InternetService
  * etc.

---

## ⚙️ Machine Learning Workflow

1. Data preprocessing

   * Removed irrelevant columns
   * Handled missing values
   * Encoded categorical variables
2. Feature engineering using ColumnTransformer
3. Pipeline creation for preprocessing + model
4. Model training (Logistic Regression)
5. Model evaluation using ROC-AUC and Cross Validation
6. Threshold tuning (0.5 → 0.4 for better recall)
7. Feature importance analysis

---

## 📈 Model Performance

* ROC-AUC: ~0.84
* Cross Validation Score: ~0.845

---

## 🧠 Key Insights

* Customers with month-to-month contracts are more likely to churn
* High monthly charges increase churn probability
* Longer tenure reduces churn
* Lack of tech support increases churn risk

---

## 🔌 API (FastAPI)

### Endpoint:

POST /predict

### Input:

Customer details in JSON format

### Output:

```json
{
"churn_probability": 0.88,
"prediction": 1
}
```

---

## ⚛️ Frontend (React)

* Simple UI for user input
* Sends request to FastAPI backend
* Displays prediction results in real time

---

## 🔄 System Architecture

User → React Frontend → FastAPI Backend → ML Model → Response → UI

---

## 🚀 How to Run Locally

### Backend:

```bash
cd backend
python -m uvicorn app:app --reload
```

### Frontend:

```bash
cd frontend
npm install
npm start
```

---
---

## 📌 Author

**Anuj Raghav**
