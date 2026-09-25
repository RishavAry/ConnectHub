import { useEffect, useState } from "react";
import Feed from "./Feed";
import { API_BASE, csrfToken } from "./api";

function ProfileView({ userId, currentUser, onError }) {
  const ownProfile = userId === currentUser.id;
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [followingBusy, setFollowingBusy] = useState(false);
  const [draft, setDraft] = useState({ bio: "", location: "" });
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  useEffect(() => {
    let active = true;
    Promise.resolve().then(() => {
      if (active) { setLoading(true); setError(""); }
      return fetch(`${API_BASE}/api/users/${userId}/profile/`, { credentials: "include" });
    }).then(async (response) => {
      const data = await response.json(); if (!response.ok) throw new Error(data.detail || `Could not load profile (${response.status}).`); return data;
    }).then((data) => { if (active) { setProfile(data); setDraft({ bio: data.bio || "", location: data.location || "" }); } }).catch((requestError) => { if (active) setError(requestError.message); }).finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [userId]);
  const saveProfile = async (event) => {
    event.preventDefault(); setSaving(true); setError(""); setNotice("");
    try {
      const response = await fetch(`${API_BASE}/api/profile/`, { method: "PATCH", credentials: "include", headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken() }, body: JSON.stringify(draft) });
      const data = await response.json(); if (!response.ok) throw new Error(Object.values(data.errors || {}).flat().join(" ") || data.detail || "Could not save profile.");
      setProfile((current) => ({ ...current, ...data })); setNotice("Profile saved.");
    } catch (requestError) { setError(requestError.message); }
    finally { setSaving(false); }
  };
  const follow = async () => {
    setFollowingBusy(true); setError("");
    try {
      const response = await fetch(`${API_BASE}/api/users/${userId}/follow/`, { method: profile.is_following ? "DELETE" : "POST", credentials: "include", headers: { "X-CSRFToken": csrfToken() } });
      const data = await response.json(); if (!response.ok) throw new Error(data.detail || "Could not update follow status.");
      setProfile((current) => ({ ...current, is_following: data.following, followers_count: data.followers_count }));
    } catch (requestError) { setError(requestError.message); }
    finally { setFollowingBusy(false); }
  };
  if (loading) return <p className="state-message">Loading profile…</p>;
  if (error && !profile) return <p className="form-error" role="alert">{error}</p>;
  if (!profile) return null;
  return <section className="feature-section"><article className="profile-card card"><header className="profile-heading"><div className="avatar profile-avatar">{profile.username[0]?.toUpperCase()}</div><div><p className="eyebrow">PROFILE</p><h1>{profile.username}</h1><p className="muted">{[profile.first_name, profile.last_name].filter(Boolean).join(" ")}</p></div>{!ownProfile && <button className={profile.is_following ? "secondary-button" : "primary-button"} disabled={followingBusy} onClick={follow}>{followingBusy ? "Saving…" : profile.is_following ? "Unfollow" : "Follow"}</button>}</header>
    <div className="profile-counts"><span><strong>{profile.posts_count}</strong> posts</span><span><strong>{profile.followers_count}</strong> followers</span><span><strong>{profile.following_count}</strong> following</span></div>
    {(profile.bio || profile.location) && <div className="profile-bio">{profile.bio && <p>{profile.bio}</p>}{profile.location && <p className="muted">{profile.location}</p>}</div>}
    {ownProfile && <form className="profile-form" onSubmit={saveProfile}><h2>Edit your profile</h2><label>Bio<textarea maxLength="5000" rows="3" value={draft.bio} onChange={(event) => setDraft((value) => ({ ...value, bio: event.target.value }))} /></label><label>Location<input maxLength="30" value={draft.location} onChange={(event) => setDraft((value) => ({ ...value, location: event.target.value }))} /></label><button className="primary-button" disabled={saving}>{saving ? "Saving…" : "Save profile"}</button>{notice && <p className="success-notice" role="status">{notice}</p>}</form>}
    {error && <p className="form-error" role="alert">{error}</p>}</article>
    <h2 className="profile-posts-title">Posts</h2><Feed posts={profile.posts || []} onError={onError} />
  </section>;
}
export default ProfileView;
