export const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function fetchCsrfToken() {
  const response = await fetch(`${API_BASE}/api/csrf/`, { credentials: "include" });
  if (!response.ok) {
    throw new Error(`Could not initialize security token (${response.status}).`);
  }
  const data = await response.json();
  if (!data.csrfToken) throw new Error("The server did not return a CSRF token.");
  return data.csrfToken;
}

// Useful at app startup to establish the session CSRF cookie. Unsafe requests
// also refresh and use the token returned by this endpoint themselves.
export async function initializeCsrf() {
  await fetchCsrfToken();
}

function isCsrfFailure(response) {
  if (response.status !== 403) return false;
  return response.clone().text().then((body) => /csrf/i.test(body));
}

export async function apiRequest(input, options = {}) {
  const method = (options.method || "GET").toUpperCase();
  const unsafe = !["GET", "HEAD", "OPTIONS"].includes(method);
  const headers = new Headers(options.headers || {});
  const body = options.body;
  if (typeof body === "string" && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const request = async (csrfToken) => {
    const requestHeaders = new Headers(headers);
    if (csrfToken) requestHeaders.set("X-CSRFToken", csrfToken);
    return fetch(input, { ...options, method, headers: requestHeaders, credentials: "include" });
  };

  if (!unsafe) return request();

  let response = await request(await fetchCsrfToken());
  if (await isCsrfFailure(response)) {
    response = await request(await fetchCsrfToken());
  }
  return response;
}

export const apiFetch = apiRequest;
