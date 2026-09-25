import Navbar from "./Navbar";
import Feed from "./Feed";
import {useEffect, useState } from "react";
import CreatePost from "./CreatePost";
import Login from "./Login";

function getCSRFToken() {
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));

  return cookie ? cookie.split("=")[1] : "";
}
function App() {
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState(null)
  const [user, setUser] = useState(null);
  const handlePostCreated = (newPost) => {
    setPosts((currentPosts) => [newPost, ...currentPosts]);
  };
  useEffect(() => {
    fetch("http://localhost:8000/api/me/", {
      credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Not authenticated");
        }

        return response.json();
      })
      .then((data) => {
        setUser(data);
      })
      .catch(() => {
        setUser(null);
      });
  }, []);
  useEffect(() => {
    fetch("http://localhost:8000/api/posts/", {
      credentials: "include",
    })
      .then((response) => {
        console.log("STATUS:", response.status);

        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }

        return response.json();
      })
      .then((data) => {
        console.log("API RESPONSE:", data);
        setPosts(data);
      })
      .catch((error) => {
        console.error("Failed to fetch posts:", error);
        setError("Failed to load posts.");
      });
  }, []);
  if (!user) {
  return <Login onLogin={setUser} />;};

  const handleLogout = () => {
    fetch("http://localhost:8000/api/logout/", {
      method: "POST",
      credentials: "include",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Logout response:", data);
        setUser(null);
      });
  };

  return (
   
    <>
      <Navbar onLogout={handleLogout} /> 
      
      
      <main>
        <h1 className="app-title">ConnectHub</h1>
        {user && <p>Logged in as {user.username}</p>}
        {error && <p>{error}</p>}
        <CreatePost onPostCreated={handlePostCreated} />
        <Feed posts={posts} />
      </main>
    </>
  );
}

export default App;
