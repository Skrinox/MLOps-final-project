import { useMemo, useState } from "react";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    Open: "",
    High: "",
    Low: "",
    Volume: "",
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const API_URL = `${import.meta.env.VITE_BACKEND_URL}/predict`;

  const fields = [
    { key: "Open", label: "Open", hint: "e.g. 150.00", suffix: "$", step: "any" },
    { key: "High", label: "High", hint: "e.g. 160.00", suffix: "$", step: "any" },
    { key: "Low", label: "Low", hint: "e.g. 145.00", suffix: "$", step: "any" },
    { key: "Volume", label: "Volume", hint: "e.g. 1200000", suffix: "", step: "1" },
  ];

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const fillExample = () => {
    setFormData({ Open: "150", High: "160", Low: "145", Volume: "1200000" });
    setError(null);
    setResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    setIsLoading(true);

    const payload = {
      Open: parseFloat(formData.Open),
      High: parseFloat(formData.High),
      Low: parseFloat(formData.Low),
      Volume: parseFloat(formData.Volume),
    };

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        const msg =
          data?.detail ||
          `Backend returned status ${response.status}. Check the API logs.`;
        throw new Error(msg);
      }

      setResult(data);
    } catch (err) {
      console.error("Prediction error:", err);
      setError(err.message || "Failed to connect to the backend API.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="topbar">
        <div className="brand">
          <div className="logoMark">T</div>
          <div>
            <h1 className="title">Toyota Stock Predictor</h1>
            <p className="subtitle">
              Predict closing price from trading features (Open/High/Low/Volume).
            </p>
          </div>
        </div>

        <div className="badgeRow">
          <span className="badge">MLflow Registry</span>
          <span className="badge badgeMuted">Stage-aware serving</span>
        </div>
      </header>

      <main className="layout">
        <section className="card">
          <div className="cardHeader">
            <h2>Inputs</h2>
            <p>Fill the form and request a prediction from the API.</p>
          </div>

          <form onSubmit={handleSubmit} className="formGrid">
            {fields.map((f) => (
              <div key={f.key} className="field">
                <label htmlFor={f.key}>{f.label}</label>
                <div className="inputWrap">
                  <input
                    id={f.key}
                    type="number"
                    name={f.key}
                    step={f.step}
                    inputMode="decimal"
                    required
                    value={formData[f.key]}
                    onChange={handleChange}
                    placeholder={f.hint}
                    aria-label={f.label}
                  />
                  {f.suffix ? <span className="suffix">{f.suffix}</span> : null}
                </div>
              </div>
            ))}

            <div className="actions">
              <button
                type="button"
                className="btn btnGhost"
                onClick={fillExample}
                disabled={isLoading}
              >
                Fill example
              </button>

              <button type="submit" className="btn btnPrimary" disabled={isLoading}>
                {isLoading ? (
                  <>
                    <span className="spinner" aria-hidden="true" /> Predicting…
                  </>
                ) : (
                  "Predict close price"
                )}
              </button>
            </div>
          </form>

          {error && (
            <div className="alert alertError" role="alert">
              <div className="alertTitle">Prediction failed</div>
              <div className="alertBody">{error}</div>
            </div>
          )}
        </section>

        <section className="card">
          <div className="cardHeader">
            <h2>Result</h2>
            <p>Response returned by the backend.</p>
          </div>

          {!result ? (
            <div className="empty">
              <div className="emptyIcon">📈</div>
              <div className="emptyText">
                No prediction yet. Submit inputs to see the estimated close price.
              </div>
            </div>
          ) : (
            <div className="result">
              <div className="metric">
                <div className="metricLabel">Estimated close</div>
                <div className="metricValue">
                  ${Number(result.predicted_close_price).toFixed(2)}
                </div>
              </div>

              <div className="meta">
                <div className="metaRow">
                  <span className="metaKey">Registry stage</span>
                  <span className="pill">{result.model_version_stage}</span>
                </div>

                {/* Si plus tard vous ajoutez model_version/model_name dans l’API, ça s’affichera */}
                {"model_version" in result && (
                  <div className="metaRow">
                    <span className="metaKey">Model version</span>
                    <span className="pill pillMuted">v{result.model_version}</span>
                  </div>
                )}
              </div>

              <details className="raw">
                <summary>Raw JSON</summary>
                <pre>{JSON.stringify(result, null, 2)}</pre>
              </details>
            </div>
          )}
        </section>
      </main>

      <footer className="footer">
        <span>Local API: {API_URL}</span>
      </footer>
    </div>
  );
}

export default App;