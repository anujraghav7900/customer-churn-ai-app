import pandas as pd

# Load dataset
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Basic inspection
print("Shape:", df.shape)
print("\nFirst 5 rows:\n", df.head())
print("\nInfo:\n")
print(df.info())
print("\nChurn Distribution:\n", df["Churn"].value_counts())

# ==============================
# Data Cleaning & Preparation
# ==============================

# Drop customerID (not useful for ML)
df.drop("customerID", axis=1, inplace=True)

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# Drop missing rows
df.dropna(inplace=True)

print("\nShape after cleaning:", df.shape)

# Convert target to numeric
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# ==============================
from sklearn.model_selection import train_test_split

X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Separate numeric and categorical columns
num_cols = X.select_dtypes(include=["int64", "float64"]).columns
cat_cols = X.select_dtypes(include=["object"]).columns

# Numeric pipeline
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Categorical pipeline
categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

# Combine both
preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, num_cols),
    ("cat", categorical_pipeline, cat_cols)
])

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

model = Pipeline([
    ("preprocessing", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

print("ROC-AUC:", roc_auc_score(y_test, y_prob))

# =============================
# Feature Importance (Logistic Regression)
# =============================

import numpy as np
import pandas as pd

# Get feature names after preprocessing
feature_names = model.named_steps["preprocessing"].get_feature_names_out()

# Get coefficients
coefficients = model.named_steps["classifier"].coef_[0]

# Create DataFrame
feature_importance = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": coefficients
})

# Remove pipeline prefixes for cleaner names
feature_importance["Feature"] = feature_importance["Feature"].str.replace("num__", "")
feature_importance["Feature"] = feature_importance["Feature"].str.replace("cat__", "")

# Sort by absolute coefficient
feature_importance["Abs_Coefficient"] = np.abs(feature_importance["Coefficient"])
feature_importance = feature_importance.sort_values(
    by="Abs_Coefficient",
    ascending=False
)

print("\nTop 15 Important Features:\n")
print(feature_importance.head(15))

import matplotlib.pyplot as plt

top_features = feature_importance.head(10)

plt.figure(figsize=(8,6))
plt.barh(top_features["Feature"], top_features["Coefficient"])
plt.gca().invert_yaxis()
plt.title("Top 10 Feature Importance (Logistic Regression)")
plt.show()

# =============================
# Random Forest Model
# =============================

from sklearn.ensemble import RandomForestClassifier

rf_model = Pipeline([
    ("preprocessing", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        random_state=42,
        class_weight="balanced"
    ))
])

rf_model.fit(X_train, y_train)

y_prob_rf = rf_model.predict_proba(X_test)[:, 1]

print("Random Forest ROC-AUC:",
      roc_auc_score(y_test, y_prob_rf))

from xgboost import XGBClassifier

xgb_model = Pipeline([
    ("preprocessing", preprocessor),
    ("classifier", XGBClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        random_state=42,
        eval_metric="logloss"
    ))
])

xgb_model.fit(X_train, y_train)

y_prob_xgb = xgb_model.predict_proba(X_test)[:, 1]

print("XGBoost ROC-AUC:",
      roc_auc_score(y_test, y_prob_xgb))

from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(
    model,
    X,
    y,
    cv=5,
    scoring="roc_auc"
)

print("Cross Validation ROC-AUC:", cv_scores.mean())

import numpy as np

y_prob = model.predict_proba(X_test)[:, 1]

# Custom threshold
threshold = 0.4
y_custom = (y_prob >= threshold).astype(int)

from sklearn.metrics import classification_report

print("Classification Report (Threshold = 0.4)\n")
print(classification_report(y_test, y_custom))

# =============================
# Save Final Production Model
# =============================

import joblib

# Save full pipeline
joblib.dump(model, "churn_model.pkl")

print("Model saved successfully as churn_model.pkl")

# Save threshold separately
threshold = 0.4
joblib.dump(threshold, "churn_threshold.pkl")

print("Threshold saved successfully.")

