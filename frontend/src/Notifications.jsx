import { useCallback, useEffect, useState } from "react";
import { API_BASE, csrfToken } from "./api";

function Notifications({ onUnreadCount }) {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState(null);
  const [error, setError] = useState("");
  const loadNotifications = useCallback(async () => {
    setLoading(true); setError("");
    try {
      const response = await fetch(`${API_BASE}/api/notifications/`, { credentials: "include" });
      const data = await response.json(); if (!response.ok) throw new Error(data.detail || `Could not load notifications (${response.status}).`);
      setNotifications(data); onUnreadCount(data.filter((item) => !item.is_read).length);
    } catch (requestError) { setError(requestError.message); }
    finally { setLoading(false); }
  }, [onUnreadCount]);
  useEffect(() => { Promise.resolve().then(loadNotifications); }, [loadNotifications]);
  const markRead = async (item) => {
    setBusyId(item.id); setError("");
    try {
      const response = await fetch(`${API_BASE}/api/notifications/${item.id}/read/`, { method: "POST", credentials: "include", headers: { "X-CSRFToken": csrfToken() } });
      const data = await response.json(); if (!response.ok) throw new Error(data.detail || "Could not mark notification as read.");
      setNotifications((current) => current.map((notification) => notification.id === item.id ? { ...notification, is_read: data.is_read } : notification));
      onUnreadCount((count) => Math.max(0, count - 1));
    } catch (requestError) { setError(requestError.message); }
    finally { setBusyId(null); }
  };
  return <section className="feature-section"><header className="section-heading"><div><p className="eyebrow">YOUR ACTIVITY</p><h1>Notifications</h1></div><button className="secondary-button" onClick={loadNotifications} disabled={loading}>{loading ? "Refreshing…" : "Refresh"}</button></header>
    {error && <p className="form-error" role="alert">{error}</p>}
    {loading ? <p className="state-message">Loading notifications…</p> : notifications.length ? <div className="notification-list">{notifications.map((item) => <article className={item.is_read ? "notification card" : "notification unread card"} key={item.id}><div className="notification-copy"><p><strong>{item.sender}</strong> {item.type === "follow" ? "started following you" : item.type === "like" ? "liked your post" : "commented on your post"}</p><time>{new Date(item.created_at).toLocaleString()}</time></div>{!item.is_read && <button className="secondary-button" disabled={busyId === item.id} onClick={() => markRead(item)}>{busyId === item.id ? "Saving…" : "Mark read"}</button>}</article>)}</div> : <div className="empty-state card"><h2>You’re all caught up</h2><p>New follows, likes and comments will appear here.</p></div>}
  </section>;
}
export default Notifications;
