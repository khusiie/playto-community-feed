import React, { useState, useEffect } from 'react';
import { fetchLeaderboard } from '../services/api';

const Leaderboard = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        const load = async () => {
            try {
                const res = await fetchLeaderboard();
                setUsers(res.data);
            } catch (error) {
                console.error("Error fetching leaderboard", error);
            }
        };
        load();
        const interval = setInterval(load, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="leaderboard">
            <h2>🏆 Leaderboard (24h)</h2>
            <ul>
                {users.map((entry, index) => (
                    <li key={index} className="leaderboard-entry">
                        <span className="rank">#{index + 1}</span>
                        <span className="username">{entry.user__username}</span>
                        <span className="karma">{entry.total_karma} pts</span>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Leaderboard;
