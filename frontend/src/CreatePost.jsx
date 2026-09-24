import { useState } from "react";

function getCSRFToken() {
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));

  return cookie ? cookie.split("=")[1] : "";
}
function CreatePost({ onPostCreated }) {
    const [content, setContent] = useState("");
    const handleSubmit = (event) => {
      event.preventDefault();

      fetch("http://localhost:8000/api/posts/", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
          content: content,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Created post:", data);
          onPostCreated(data);
          setContent("");
        });
    };
  return (
    <div>
      <h2>Create a post</h2>

      <textarea
        value={content}
        onChange={(event) => setContent(event.target.value)}
        placeholder="What's happening?"
      />
      <button onClick={handleSubmit}>Post</button>
    </div>
  );
}

export default CreatePost;
