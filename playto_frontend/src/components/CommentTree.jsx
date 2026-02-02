import React, { useState } from 'react';
import { likeContent, createComment } from '../services/api';
import { formatDistanceToNow } from 'date-fns';

const CommentTree = ({ comment, threadId }) => {
    const [likes, setLikes] = useState(comment.likes_count || 0);
    const [showReply, setShowReply] = useState(false);
    const [replyContent, setReplyContent] = useState('');
    const [replies, setReplies] = useState(comment.replies || []);

    const handleLike = async () => {
        try {
            const response = await likeContent('comment', comment.id);
            if (response.data.status === 'liked') {
                setLikes(likes + 1);
            } else {
                setLikes(likes - 1);
            }
        } catch (error) {
            console.error("Error liking comment", error);
        }
    };

    const handleReply = async (e) => {
        e.preventDefault();
        try {
            const response = await createComment({
                content: replyContent,
                thread: threadId,
                parent: comment.id
            });
            setReplies([...replies, response.data]);
            setReplyContent('');
            setShowReply(false);
        } catch (error) {
            console.error("Error replying to comment", error);
        }
    };

    return (
        <div className="comment-node" style={{ marginLeft: '20px', borderLeft: '1px solid #444', paddingLeft: '10px' }}>
            <p><strong>{comment.author.username}</strong>: {comment.content}</p>
            <div className="meta-compact">
                <span>{formatDistanceToNow(new Date(comment.created_at))} ago</span>
                <button className="text-btn" onClick={handleLike}>❤️ {likes}</button>
                <button className="text-btn" onClick={() => setShowReply(!showReply)}>
                    Reply {replies.length > 0 ? `(${replies.length})` : ''}
                </button>
            </div>

            {showReply && (
                <form onSubmit={handleReply}>
                    <input
                        type="text"
                        value={replyContent}
                        onChange={(e) => setReplyContent(e.target.value)}
                        placeholder="Reply..."
                    />
                    <button type="submit">Post</button>
                </form>
            )}

            {replies.map(reply => (
                <CommentTree key={reply.id} comment={reply} threadId={threadId} />
            ))}
        </div>
    );
};

export default CommentTree;
