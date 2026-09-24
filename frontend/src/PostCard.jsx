import { useState } from "react";
import "./PostCard.css"

function getCSRFToken() {
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));

  return cookie ? cookie.split("=")[1] : "";
}

function PostCard({ postId, username, content, createdAt, likesCount }) {
  const [liked, setLiked] = useState(false);
  const [likeCount, setLikeCount] = useState(likesCount);
  const handleLike = () => {
    fetch(`http://localhost:8000/api/posts/${postId}/like/`, {
      method: "POST",
      credentials: "include",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
    })
      .then((response) => response.json())
      
      .then((data) => {
        setLiked(data.liked)
        setLikeCount(data.likes_count)
        console.log("Like response:", data);
        
      });
  };

  return (
    <div className="post-card">
      <h3>{username}</h3>
      <p className="post-item">{createdAt}</p>
      <p>{content}</p>

      <button onClick={handleLike}>
        {liked ? "Unlike" : "Like"}</button>
        <p>{likeCount} likes</p>
    </div>
  );
}

export default PostCard;
