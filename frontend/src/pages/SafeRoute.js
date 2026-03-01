import { useState } from "react";
import { service } from "../services/api";

export default function SafeRoute() {
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [route, setRoute] = useState(null);

  const onFindRoute = async () => {
    if (!source.trim() || !destination.trim()) {
      setError("Enter both source and destination.");
      return;
    }

    setLoading(true);
    setError("");
    setRoute(null);

    try {
      const data = await service.getSafeRoute(source.trim(), destination.trim(), {
        userPreference: "safety-first",
      });
      setRoute(data);
    } catch (_err) {
      setError("Could not fetch route right now.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container page">
      <section className="panel">
      <h2>Safe Route Navigation</h2>
        <p className="muted">
          Smart route recommendation using risk, crowd density, and lighting
          conditions.
        </p>

        <div className="form-grid">
          <input
            placeholder="Source"
            value={source}
            onChange={(e) => setSource(e.target.value)}
          />
          <input
            placeholder="Destination"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
          />
        </div>

        <button className="btn btn-primary" onClick={onFindRoute} disabled={loading}>
          {loading ? "Calculating..." : "Find Safest Route"}
        </button>

        {error && <p className="error">{error}</p>}

        {route && (
          <div className="result-card">
            <h3>Safest Path Found</h3>
            <p>
              Route: <strong>{route.source}</strong> to{" "}
              <strong>{route.destination}</strong>
            </p>
            <p>
              Risk Score:
            <span
            style={{
                color:
                route.overallRiskScore > 6
                    ? "red"
                    : route.overallRiskScore > 4
                    ? "orange"
                    : "green",
                fontWeight: "bold",
                marginLeft: "6px",
            }}
            >
            {route.overallRiskScore}/10
            </span>
              <strong>{route.eta}</strong>
            </p>
            <p>Path: {route.safestPath?.join(" -> ")}</p>
            <p>Avoid Zones: {route.avoidZones?.join(", ")}</p>
            <p>
              Lighting: {route.lightingScore} | Crowd: {route.crowdScore} |
              Incident Density: {route.incidentDensityScore}
            </p>
            <p className="muted">Live Share URL: {route.liveShareUrl}</p>
            <p className="muted">
              SOS-ready contacts linked: {route.sosContactsNotified}
            </p>
          </div>
        )}
      </section>
    </main>
  );
}
