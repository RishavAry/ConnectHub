import { useState } from "react";
import { API_BASE, apiRequest } from "./api";

function CreatePost({ onPostCreated }) {
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!content.trim()) { setError("Write something before posting."); return; }
    setBusy(true); setError("");
    try {
      const body = new FormData(); body.append("content", content.trim()); if (image) body.append("image", image);
      const response = await apiRequest(`${API_BASE}/api/posts/`, { method: "POST", body });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || data.detail || "Could not create your post.");
      onPostCreated(data); setContent(""); setImage(null); event.target.reset();
    } catch (requestError) { setError(requestError.message); }
    finally { setBusy(false); }
  };
  return <form className="create-post card" onSubmit={handleSubmit}>
    <h2>Share an update</h2>
    <textarea value={content} onChange={(event) => setContent(event.target.value)} placeholder="What’s happening?" rows="3" maxLength="5000" />
    <div className="composer-actions"><label className="file-label">Add an image<input type="file" accept="image/*" onChange={(event) => setImage(event.target.files[0] || null)} /></label><span className="muted">{image?.name || "Images up to 5 MB"}</span><button className="primary-button" disabled={busy}>{busy ? "Posting…" : "Post"}</button></div>
    {error && <p className="form-error" role="alert">{error}</p>}
  </form>;
}
export default CreatePost;
