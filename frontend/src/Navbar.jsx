import "./Navbar.css";

function Navbar({ user, view, unreadCount, onNavigate, onLogout, logoutLoading }) {
  const items = [["feed", "Feed"], ["profile", "Profile"], ["search", "People"], ["notifications", "Notifications"]];
  return <nav className="top-nav">
    <a className="brand" href="#feed" onClick={(event) => { event.preventDefault(); onNavigate("feed"); }}>ConnectHub</a>
    <div className="nav-links" aria-label="Main navigation">
      {items.map(([key, label]) => <button className={view === key ? "nav-link active" : "nav-link"} key={key} onClick={() => onNavigate(key)}>{label}{key === "notifications" && unreadCount > 0 ? <span className="notification-badge">{unreadCount}</span> : null}</button>)}
    </div>
    <div className="nav-user"><span>{user?.username}</span><button className="logout-button" disabled={logoutLoading} onClick={onLogout}>{logoutLoading ? "Signing out…" : "Logout"}</button></div>
  </nav>;
}
export default Navbar;
