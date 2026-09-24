import PostCard from "./PostCard";
import "./Feed.css";

function Feed({ posts }) {
  return (
    <div className="feed">
      {posts.map((post) => (
        <PostCard
          key={post.id}
          postId={post.id}
          username={post.username}
          content={post.content}
          createdAt={post.createdAt}
          likesCount={post.likes_count}
        />
      ))}
    </div>
  );
}

export default Feed;
