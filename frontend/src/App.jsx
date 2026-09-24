import Navbar from "./Navbar";
import Feed from "./Feed";
import {useEffect, useState } from "react";
import CreatePost from "./CreatePost";


function App() {
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState(null)
  const handlePostCreated = (newPost) => {
    setPosts((currentPosts) => [newPost, ...currentPosts]);
  };
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
  return (
    <>
      <Navbar />

      <main>
        <h1 className="app-title">ConnectHub</h1>
        {error && <p>{error}</p>}
        <CreatePost onPostCreated={handlePostCreated} />
        <Feed posts={posts} />
      </main>
    </>
  );
}

export default App;
