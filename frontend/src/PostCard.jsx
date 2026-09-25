import { useEffect, useState } from "react";
import { API_BASE, csrfToken } from "./api";
import "./PostCard.css";

function PostCard({ post, onError }) {
  const [liked, setLiked] = useState(false);
  const [likeCount, setLikeCount] = useState(post.likes_count || 0);
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState([]);
  const [commentsLoading, setCommentsLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [localError, setLocalError] = useState("");
  useEffect(() => {
    let active = true;
    fetch(`${API_BASE}/api/posts/${post.id}/comments/`, { credentials: "include" }).then(async (response) => {
      if (!response.ok) throw new Error(`Could not load comments (${response.status}).`);
      return response.json();
    }).then((data) => { if (active) setComments(data); }).catch((error) => { if (active) setLocalError(error.message); }).finally(() => { if (active) setCommentsLoading(false); });
    return () => { active = false; };
  }, [post.id]);
  const handleLike = async () => {
    setBusy(true); setLocalError("");
    try {
      const response = await fetch(`${API_BASE}/api/posts/${post.id}/like/`, { method: "POST", credentials: "include", headers: { "X-CSRFToken": csrfToken() } });
      const data = await response.json(); if (!response.ok) throw new Error(data.detail || `Like failed (${response.status}).`);
      setLiked(data.liked); setLikeCount(data.likes_count);
    } catch (error) { setLocalError(error.message); onError?.(error.message); }
    finally { setBusy(false); }
  };
  const handleComment = async (event) => {
    event.preventDefault(); if (!comment.trim()) return;
    setBusy(true); setLocalError("");
    try {
      const response = await fetch(`${API_BASE}/api/posts/${post.id}/comments/`, { method: "POST", credentials: "include", headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken() }, body: JSON.stringify({ content: comment.trim() }) });
      const data = await response.json(); if (!response.ok) throw new Error(data.error || data.detail || "Could not add comment.");
      setComments((current) => [...current, data]); setComment("");
    } catch (error) { setLocalError(error.message); onError?.(error.message); }
    finally { setBusy(false); }
  };
  return <article className="post-card card">
    <header className="post-header"><div className="avatar" aria-hidden="true">{post.author?.charAt(0)?.toUpperCase() || "U"}</div><div><h3>{post.author || "ConnectHub member"}</h3><time>{post.created_at ? new Date(post.created_at).toLocaleString() : ""}</time></div></header>
    <p className="post-content">{post.content}</p>
    {post.image && <img className="post-image" src={post.image.startsWith("http") ? post.image : `${API_BASE}${post.image}`} alt={`Post by ${post.author || "user"}`} loading="lazy" />}
    <div className="post-actions"><button className={liked ? "like-button liked" : "like-button"} disabled={busy} onClick={handleLike}>{liked ? "♥ Liked" : "♡ Like"}</button><span className="muted">{likeCount} {likeCount === 1 ? "like" : "likes"}</span></div>
    <section className="comments"><h4>Comments</h4>{commentsLoading ? <p className="muted">Loading comments…</p> : comments.length ? comments.map((item) => <div className="comment" key={item.id}><strong>{item.username}</strong><p>{item.content}</p></div>) : <p className="muted">No comments yet.</p>}
      <form className="comment-form" onSubmit={handleComment}><input value={comment} onChange={(event) => setComment(event.target.value)} placeholder="Write a comment…" aria-label="Write a comment" /><button disabled={busy || !comment.trim()}>{busy ? "Sending…" : "Comment"}</button></form>
    </section>
    {localError && <p className="form-error" role="alert">{localError}</p>}
  </article>;
}
export default PostCard;
