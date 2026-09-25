import { useState } from "react";
import { API_BASE, csrfToken } from "./api";

function PeopleSearch({ onOpenProfile }) {
  const [query, setQuery] = useState("");
  const [users, setUsers] = useState([]);
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);
  const [busyId, setBusyId] = useState(null);
  const [error, setError] = useState("");
  const search = async (event) => {
    event.preventDefault(); setLoading(true); setError(""); setSearched(true);
    try {
      const response = await fetch(`${API_BASE}/api/users/search/?q=${encodeURIComponent(query.trim())}`, { credentials: "include" });
      const data = await response.json(); if (!response.ok) throw new Error(data.detail || `Search failed (${response.status}).`);
      setUsers(data);
    } catch (requestError) { setError(requestError.message); }
    finally { setLoading(false); }
  };
  const toggleFollow = async (person) => {
    setBusyId(person.id); setError("");
    try {
      const response = await fetch(`${API_BASE}/api/users/${person.id}/follow/`, { method: person.is_following ? "DELETE" : "POST", credentials: "include", headers: { "X-CSRFToken": csrfToken() } });
      const data = await response.json(); if (!response.ok) throw new Error(data.detail || "Could not update follow status.");
      setUsers((current) => current.map((item) => item.id === person.id ? { ...item, is_following: data.following } : item));
    } catch (requestError) { setError(requestError.message); }
    finally { setBusyId(null); }
  };
  return <section className="feature-section"><header className="section-heading"><div><p className="eyebrow">CONNECT</p><h1>Find people</h1></div></header>
    <form className="search-form card" onSubmit={search}><label htmlFor="people-query">Search by name, username or email</label><div><input id="people-query" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Try a username or name" /><button className="primary-button" disabled={loading}>{loading ? "Searching…" : "Search"}</button></div></form>
    {error && <p className="form-error" role="alert">{error}</p>}
    {loading ? <p className="state-message">Searching…</p> : searched && (users.length ? <div className="people-list">{users.map((person) => <article className="person-card card" key={person.id}><button className="person-name" onClick={() => onOpenProfile(person.id)}><span className="avatar">{person.username[0]?.toUpperCase()}</span><span><strong>{person.username}</strong><small>{[person.first_name, person.last_name].filter(Boolean).join(" ")}</small></span></button><button className={person.is_following ? "secondary-button" : "primary-button"} disabled={busyId === person.id} onClick={() => toggleFollow(person)}>{busyId === person.id ? "Saving…" : person.is_following ? "Following" : "Follow"}</button></article>)}</div> : <div className="empty-state card"><h2>No people found</h2><p>Try another name or username.</p></div>)}
  </section>;
}
export default PeopleSearch;
