import { useEffect, useState } from "react";

import "./PostCard.css";

function getCSRFToken() {
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));

  return cookie ? cookie.split("=")[1] : "";
}

function PostCard({ postId, username, content, createdAt, likesCount }) {
  const [liked, setLiked] = useState(false);
  const [likeCount, setLikeCount] = useState(likesCount);
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState([]);
  useEffect(() => {
    fetch(`http://localhost:8000/api/posts/${postId}/comments/`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setComments(data);
      });
  }, [postId]);
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
        setLiked(data.liked);
        setLikeCount(data.likes_count);
        console.log("Like response:", data);
      });
  };
  const handleComment = () => {
    fetch(`http://localhost:8000/api/posts/${postId}/comments/`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({
        content: comment,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Comment response:", data);
        setComments((currentComments) => [...currentComments, data]);
        setComment("");
      });
  };

  return (
    <div className="post-card">
      <h3>{username}</h3>
      <p className="post-item">{createdAt}</p>
      <p>{content}</p>

      <button onClick={handleLike}>{liked ? "Unlike" : "Like"}</button>
      <p>{likeCount} likes</p>
      <textarea
        value={comment}
        onChange={(event) => setComment(event.target.value)}
        placeholder="Write a comment..."
      />

      <button onClick={handleComment}>Comment</button>
      {comments.map((item) => (
        <div key={item.id}>
          <strong>{item.username}</strong>
          <p>{item.content}</p>
        </div>
      ))}
    </div>
  );
}

export default PostCard;
