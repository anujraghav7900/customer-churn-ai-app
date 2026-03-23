import React, { useState } from "react";

function App() {
  const [result, setResult] = useState(null);

  const handlePredict = async () => {
    try {
      const data = {
        gender: "Male",
        SeniorCitizen: 0,
        Partner: "Yes",
        Dependents: "No",
        tenure: 12,
        PhoneService: "Yes",
        MultipleLines: "No",
        InternetService: "DSL",
        OnlineSecurity: "No",
        OnlineBackup: "Yes",
        DeviceProtection: "No",
        TechSupport: "No",
        StreamingTV: "No",
        StreamingMovies: "No",
        Contract: "Month-to-month",
        PaperlessBilling: "Yes",
        PaymentMethod: "Electronic check",
        MonthlyCharges: 70,
        TotalCharges: 800
      };

      const response = await fetch(
        "https://anuj-raghavx-customer-churn.up.railway.app/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        }
      );

      const result = await response.json();
      setResult(result);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Customer Churn Prediction</h1>

      <button onClick={handlePredict}>Predict</button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h2>Prediction: {result.prediction}</h2>
          <h3>Probability: {result.churn_probability}</h3>
        </div>
      )}
    </div>
  );
}

export default App;