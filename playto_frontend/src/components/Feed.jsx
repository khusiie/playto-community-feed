import React, { useState, useEffect } from 'react';
import { fetchThreads, createThread } from '../services/api';
import Thread from './Thread';

const Feed = () => {
    const [threads, setThreads] = useState([]);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    useEffect(() => {
        loadThreads();
    }, []);

    const loadThreads = async () => {
        try {
            const response = await fetchThreads();
            setThreads(response.data);
        } catch (error) {
            console.error("Error fetching threads", error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await createThread({ title, content });
            setThreads([response.data, ...threads]); // Add to top
            setTitle('');
            setContent('');
        } catch (error) {
            console.error("Error creating thread", error);
        }
    };

    return (
        <div className="feed-container">
            <div className="create-post">
                <h2>Create a Post</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                    <textarea
                        placeholder="Content"
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        required
                    />
                    <button type="submit">Post</button>
                </form>
            </div>

            <div className="thread-list">
                {threads.map(thread => (
                    <Thread key={thread.id} thread={thread} />
                ))}
            </div>
        </div>
    );
};

export default Feed;
