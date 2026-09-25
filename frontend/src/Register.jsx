import { useState } from "react";
import { API_BASE, csrfToken } from "./api";

function Register({ onSwitchLogin, onRegistered }) {
  const [values, setValues] = useState({ username: "", email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [busy, setBusy] = useState(false);
  const update = (field) => (event) => setValues((current) => ({ ...current, [field]: event.target.value }));
  const handleSubmit = async (event) => {
    event.preventDefault(); setErrors({}); setBusy(true);
    try {
      const csrfResponse = await fetch(`${API_BASE}/api/csrf/`, { credentials: "include" });
      if (!csrfResponse.ok) throw new Error("Could not initialize secure registration. Please retry.");
      const response = await fetch(`${API_BASE}/api/register/`, {
        method: "POST", credentials: "include",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken() },
        body: JSON.stringify(values),
      });
      const data = await response.json();
      if (!response.ok) { setErrors(data.errors || { form: [data.detail || "Registration failed."] }); return; }
      onRegistered(data.message || "Registration successful. Please sign in.");
    } catch (error) { setErrors({ form: [error.message || "Registration failed. Please retry."] }); }
    finally { setBusy(false); }
  };
  return <main className="login-shell"><form className="login-card card" onSubmit={handleSubmit}>
    <p className="eyebrow">JOIN THE COMMUNITY</p><h1>Create your account</h1><p className="muted">Register to start sharing with ConnectHub.</p>
    <label>Username<input autoComplete="username" required maxLength="150" value={values.username} onChange={update("username")} /></label>
    <label>Email<input type="email" autoComplete="email" required value={values.email} onChange={update("email")} /></label>
    <label>Password<input type="password" autoComplete="new-password" required value={values.password} onChange={update("password")} /></label>
    {Object.entries(errors).map(([field, messages]) => <p className="form-error" role="alert" key={field}>{field !== "__all__" && field !== "form" ? `${field}: ` : ""}{messages.join(" ")}</p>)}
    <button className="primary-button" disabled={busy}>{busy ? "Creating account…" : "Create account"}</button>
    <p className="auth-switch">Already registered? <button type="button" onClick={onSwitchLogin}>Sign in</button></p>
  </form></main>;
}
export default Register;
