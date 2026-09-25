import PostCard from "./PostCard";
import "./Feed.css";

function Feed({ posts, onError }) {
  if (!posts.length) return <div className="empty-state card"><h2>Your feed is quiet</h2><p>There are no posts to show yet. Be the first to share an update.</p></div>;
  return <div className="feed">{posts.map((post) => <PostCard key={post.id} post={post} onError={onError} />)}</div>;
}
export default Feed;
