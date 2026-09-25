import { useState } from "react";
import { API_BASE, apiRequest } from "./api";

function Login({ onLogin, onSwitchRegister, notice }) {
  const [username, setUsername] = useState(""); const [password, setPassword] = useState(""); const [busy, setBusy] = useState(false); const [error, setError] = useState("");
  const handleSubmit = async (event) => {
    event.preventDefault(); setBusy(true); setError("");
    try {
      const response = await apiRequest(`${API_BASE}/api/login/`, { method: "POST", body: JSON.stringify({ username, password }) });
      const data = await response.json(); if (!response.ok) throw new Error(data.error || data.detail || "Login failed.");
      await onLogin();
    } catch (requestError) { setError(requestError.message); }
    finally { setBusy(false); }
  };
  return <main className="login-shell"><form className="login-card card" onSubmit={handleSubmit}><p className="eyebrow">WELCOME TO</p><h1>ConnectHub</h1><p className="muted">Sign in to catch up with your community.</p>
    {notice && <p className="success-notice" role="status">{notice}</p>}
    <label>Username<input autoComplete="username" required value={username} onChange={(event) => setUsername(event.target.value)} /></label>
    <label>Password<input type="password" autoComplete="current-password" required value={password} onChange={(event) => setPassword(event.target.value)} /></label>
    {error && <p className="form-error" role="alert">{error}</p>}<button className="primary-button" disabled={busy}>{busy ? "Signing in…" : "Sign in"}</button>
    <p className="auth-switch">New to ConnectHub? <button type="button" onClick={onSwitchRegister}>Create an account</button></p>
  </form></main>;
}
export default Login;
