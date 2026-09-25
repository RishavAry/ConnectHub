export const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
export function csrfToken() {
  return document.cookie.split("; ").find((cookie) => cookie.startsWith("csrftoken="))?.split("=").slice(1).join("=") || "";
}
