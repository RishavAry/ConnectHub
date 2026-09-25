import { useCallback, useEffect, useState } from "react";
import Navbar from "./Navbar";
import Feed from "./Feed";
import CreatePost from "./CreatePost";
import Login from "./Login";
import Register from "./Register";
import { API_BASE } from "./api";
import ProfileView from "./ProfileView";
import PeopleSearch from "./PeopleSearch";
import Notifications from "./Notifications";

function App() {
  const [posts, setPosts] = useState([]);
  const [user, setUser] = useState(null);
  const [view, setView] = useState("feed");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [logoutLoading, setLogoutLoading] = useState(false);
  const [authView, setAuthView] = useState("login");
  const [authNotice, setAuthNotice] = useState("");
  const [selectedProfileId, setSelectedProfileId] = useState(null);
  const [unreadCount, setUnreadCount] = useState(0);

  const loadPosts = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE}/api/posts/`, { credentials: "include" });
      if (!response.ok) throw new Error(response.status === 403 ? "Please log in to view the feed." : `Could not load posts (${response.status}).`);
      setPosts(await response.json());
    } catch (requestError) {
      setError(requestError.message || "Could not load posts.");
    } finally {
      setLoading(false);
    }
  }, []);

  const loadUser = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/api/me/`, { credentials: "include" });
      if (!response.ok) throw new Error("Not authenticated");
      setUser(await response.json());
    } catch {
      setUser(null);
    }
  }, []);

  useEffect(() => {
    Promise.resolve().then(async () => {
      try {
        const response = await fetch(`${API_BASE}/api/csrf/`, { credentials: "include" });
        if (!response.ok) throw new Error(`Could not initialize security cookie (${response.status}).`);
        await loadUser();
      } catch (requestError) {
        setError(requestError.message);
        setUser(null);
      }
    });
  }, [loadUser]);
  useEffect(() => { if (user) Promise.resolve().then(loadPosts); }, [user, loadPosts]);

  const handlePostCreated = (post) => setPosts((current) => [post, ...current]);
  const handleLogout = async () => {
    setLogoutLoading(true);
    setError("");

    try {
      const csrfResponse = await fetch(`${API_BASE}/api/csrf/`, {
        credentials: "include",
      });

      if (!csrfResponse.ok) {
        throw new Error("Could not initialize secure logout.");
      }

      const csrfData = await csrfResponse.json();

      const response = await fetch(`${API_BASE}/api/logout/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "X-CSRFToken": csrfData.csrfToken,
        },
      });

      if (!response.ok) {
        throw new Error(`Logout failed (${response.status}).`);
      }

      setUser(null);
      setPosts([]);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLogoutLoading(false);
    }
  };

  if (!user) return authView === "register"
    ? <Register onSwitchLogin={() => setAuthView("login")} onRegistered={(message) => { setAuthNotice(message); setAuthView("login"); }} />
    : <Login onLogin={loadUser} notice={authNotice} onSwitchRegister={() => { setAuthNotice(""); setAuthView("register"); }} />;

  return <>
    <Navbar user={user} view={view} unreadCount={unreadCount} onNavigate={(nextView) => { setView(nextView); if (nextView === "profile") setSelectedProfileId(user.id); }} onLogout={handleLogout} logoutLoading={logoutLoading} />
    <main className="app-main">
      {view === "feed" ? <>
        <header className="page-heading"><div><p className="eyebrow">YOUR COMMUNITY</p><h1>Home feed</h1></div><span className="welcome">Signed in as <strong>{user.username}</strong></span></header>
        <CreatePost onPostCreated={handlePostCreated} />
        {error && <div className="notice error-notice" role="alert">{error} <button onClick={loadPosts}>Retry</button></div>}
        {loading ? <p className="state-message">Loading your feed…</p> : <Feed posts={posts} onError={setError} />}
      </> : view === "search" ? <PeopleSearch onOpenProfile={(id) => { setSelectedProfileId(id); setView("profile"); }} />
        : view === "notifications" ? <Notifications onUnreadCount={setUnreadCount} />
          : <ProfileView userId={selectedProfileId || user.id} currentUser={user} onError={setError} />}
    </main>
  </>;
}

export default App;
