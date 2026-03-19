import React, { useState } from "react";
import axios from "axios";

function App() {
  const [tenure, setTenure] = useState(5);
  const [monthlyCharges, setMonthlyCharges] = useState(90.5);
  const [result, setResult] = useState(null);

  const handlePredict = async () => {
    const data = {
      gender: "Female",
      SeniorCitizen: 0,
      Partner: "Yes",
      Dependents: "No",
      tenure: tenure,
      PhoneService: "Yes",
      MultipleLines: "No",
      InternetService: "Fiber optic",
      OnlineSecurity: "No",
      OnlineBackup: "No",
      DeviceProtection: "No",
      TechSupport: "No",
      StreamingTV: "Yes",
      StreamingMovies: "Yes",
      Contract: "Month-to-month",
      PaperlessBilling: "Yes",
      PaymentMethod: "Electronic check",
      MonthlyCharges: monthlyCharges,
      TotalCharges: tenure * monthlyCharges
    };

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        data
      );
      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Error connecting to API");
    }
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>Telecom Churn Prediction</h1>

      <div>
        <label>Tenure: </label>
        <input
          type="number"
          value={tenure}
          onChange={(e) => setTenure(Number(e.target.value))}
        />
      </div>

      <div>
        <label>Monthly Charges: </label>
        <input
          type="number"
          value={monthlyCharges}
          onChange={(e) => setMonthlyCharges(Number(e.target.value))}
        />
      </div>

      <button onClick={handlePredict}>Predict</button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Churn Probability: {result.churn_probability}</h3>
          <h3>
            Prediction: {result.prediction === 1 ? "Will Churn" : "Will Stay"}
          </h3>
        </div>
      )}
    </div>
  );
}

export default App;