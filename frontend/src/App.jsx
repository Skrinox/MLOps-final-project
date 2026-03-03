import { useState } from 'react'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    Open: '', High: '', Low: '', Volume: ''
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const API_URL = "http://127.0.0.1:8000/predict";

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    const payload = {
      Open: parseFloat(formData.Open),
      High: parseFloat(formData.High),
      Low: parseFloat(formData.Low),
      Volume: parseFloat(formData.Volume)
    };

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Backend returned status ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error("Prediction error:", err);
      setError("Failed to connect to the backend API.");
    }
  };

  return (
    <div className="container">
      <h1 style={{ color: '#d71921' }}>Toyota stock predictor 📈</h1>
      <p>Enter trading features to predict the closing price.</p>

      <form onSubmit={handleSubmit} className="form">
        {['Open', 'High', 'Low', 'Volume'].map((field) => (
          <div key={field} className="form-group">
            <label>{field} {field !== 'Volume' && 'Price ($)'}:</label>
            <input
              type="number"
              name={field}
              step="any"
              required
              value={formData[field]}
              onChange={handleChange}
              placeholder={`ex: ${field === 'Volume' ? '1200000' : '150.00'}`}
            />
          </div>
        ))}
        <button type="submit">Predict Close Price</button>
      </form>

      {error && <div className="error-box">{error}</div>}

      {result && (
        <div className="result-box">
          <h3>Prediction</h3>
          <p><strong>Estimated close:</strong> ${result.predicted_close_price.toFixed(2)}</p>
          <p style={{ fontSize: '0.85em', color: '#666' }}>
            Served by registry stage: <strong>{result.model_version_stage}</strong>
          </p>
        </div>
      )}
    </div>
  )
}

export default App