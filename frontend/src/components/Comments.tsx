import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { Comment } from '../types';

interface CommentsProps {
  showId: number;
  episodeId?: number;
}

export function Comments({ showId, episodeId }: CommentsProps) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isEpisode = episodeId !== undefined;

  useEffect(() => {
    fetchComments();
  }, [showId, episodeId]);

  const fetchComments = async () => {
    setLoading(true);
    try {
      const data = isEpisode
        ? await api.getEpisodeComments(episodeId!)
        : await api.getShowComments(showId);
      setComments(data);
    } catch (err) {
      setError('Failed to load comments');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newComment.trim() || submitting) return;

    setSubmitting(true);
    setError(null);
    try {
      const comment = isEpisode
        ? await api.addEpisodeComment(showId, episodeId!, newComment)
        : await api.addShowComment(showId, newComment);
      setComments([comment, ...comments]);
      setNewComment('');
    } catch (err) {
      setError('Failed to add comment');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (commentId: number) => {
    try {
      await api.deleteComment(commentId);
      setComments(comments.filter(c => c.id !== commentId));
    } catch (err) {
      setError('Failed to delete comment');
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="comments-section">
      <h3>{isEpisode ? 'Episode Comments' : 'Show Comments'}</h3>
      
      <form onSubmit={handleSubmit} className="comment-form">
        <textarea
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Write a comment..."
          rows={3}
          disabled={submitting}
        />
        <button type="submit" disabled={submitting || !newComment.trim()}>
          {submitting ? 'Posting...' : 'Post Comment'}
        </button>
      </form>

      {error && <div className="comment-error">{error}</div>}

      {loading ? (
        <div className="comments-loading">Loading comments...</div>
      ) : comments.length === 0 ? (
        <div className="no-comments">No comments yet. Be the first!</div>
      ) : (
        <ul className="comments-list">
          {comments.map(comment => (
            <li key={comment.id} className="comment-item">
              <p className="comment-text">{comment.text}</p>
              <div className="comment-meta">
                <span className="comment-date">{formatDate(comment.created_at)}</span>
                <button 
                  className="comment-delete"
                  onClick={() => handleDelete(comment.id)}
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}