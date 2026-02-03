import React, { useState } from 'react';
import { likeContent, createComment } from '../services/api';
import { formatDistanceToNow } from 'date-fns';
import CommentTree from './CommentTree';

const Thread = ({ thread }) => {
    const [likes, setLikes] = useState(thread.likes_count || 0);
    const [comments, setComments] = useState(thread.comments || []);
    const [commentsCount, setCommentsCount] = useState(thread.comments_count || 0);
    const [showComments, setShowComments] = useState(false);
    const [replyContent, setReplyContent] = useState('');

    const handleLike = async () => {
        try {
            const response = await likeContent('thread', thread.id);
            if (response.data.status === 'liked') {
                setLikes(likes + 1);
            } else {
                setLikes(likes - 1);
            }
        } catch (error) {
            console.error("Error liking thread", error);
        }
    };

    const handleReply = async (e) => {
        e.preventDefault();
        try {
            const response = await createComment({
                content: replyContent,
                thread: thread.id,
                parent: null
            });
            setComments([response.data, ...comments]);
            setCommentsCount(commentsCount + 1);
            setReplyContent('');
            setShowComments(true);
        } catch (error) {
            console.error("Error replying", error);
        }
    };

    return (
        <div className="thread-card">
            <h3>{thread.title}</h3>
            <p className="thread-content">{thread.content}</p>
            <div className="meta">
                <span>Posted by {thread.author.username} {formatDistanceToNow(new Date(thread.created_at))} ago</span>
                <button onClick={handleLike}>❤️ {likes}</button>
                <button onClick={() => setShowComments(!showComments)}>💬 {commentsCount} Comments</button>
            </div>

            {showComments && (
                <div className="comments-section">
                    <form onSubmit={handleReply}>
                        <input
                            type="text"
                            value={replyContent}
                            onChange={(e) => setReplyContent(e.target.value)}
                            placeholder="Write a comment..."
                        />
                        <button type="submit">Post</button>
                    </form>
                    {comments.map(comment => (
                        <CommentTree key={comment.id} comment={comment} threadId={thread.id} />
                    ))}
                </div>
            )}
        </div>
    );
};

export default Thread;
