import React, { useState } from "react";

function App() {
  const [tenure, setTenure] = useState("");
  const [monthlyCharges, setMonthlyCharges] = useState("");
  const [totalCharges, setTotalCharges] = useState("");
  const [result, setResult] = useState(null);

  const handlePredict = async () => {
    const data = {
      gender: "Male",
      SeniorCitizen: 0,
      Partner: "Yes",
      Dependents: "No",
      tenure: Number(tenure),
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
      MonthlyCharges: Number(monthlyCharges),
      TotalCharges: Number(totalCharges)
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
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Customer Churn Prediction</h1>

      <input
        placeholder="Tenure"
        value={tenure}
        onChange={(e) => setTenure(e.target.value)}
      /><br /><br />

      <input
        placeholder="Monthly Charges"
        value={monthlyCharges}
        onChange={(e) => setMonthlyCharges(e.target.value)}
      /><br /><br />

      <input
        placeholder="Total Charges"
        value={totalCharges}
        onChange={(e) => setTotalCharges(e.target.value)}
      /><br /><br />

      <button onClick={handlePredict}>Predict</button>

      {result && (
        <div>
          <h2>Prediction: {result.prediction}</h2>
          <h3>Probability: {result.churn_probability}</h3>
        </div>
      )}
    </div>
  );
}

export default App;