import "./Navbar.css"

function Navbar({ onLogout}) {
    return (
      <nav>
        <h2>ConnectHub</h2>
        <button>Profile</button>
        <button onClick={onLogout}>Logout</button>
      </nav>
    );
}
export default Navbar