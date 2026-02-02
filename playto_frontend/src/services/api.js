import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/',
    timeout: 5000,
    withCredentials: true,
});

// Since we are using session authentication (or none for read-only), 
// we might need to handle CSRF token if we do POST requests with session.
// For now, let's assume loose cookies or basic auth if needed.
// Actually, with Django Session Auth, we need X-CSRFToken.

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

api.interceptors.request.use((config) => {
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
});

export default api;

export const fetchThreads = () => api.get('threads/');
export const createThread = (data) => api.post('threads/', data);
export const fetchLeaderboard = () => api.get('leaderboard/');
export const likeContent = (contentType, objectId) => api.post('likes/', { content_type: contentType, object_id: objectId });
export const createComment = (data) => api.post('comments/', data);
