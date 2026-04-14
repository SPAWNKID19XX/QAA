import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import client from '../api/client';
import CommentItem from '../components/CommentItem';

const STATUS_OPTIONS = ['open', 'in_progress', 'done', 'closed'];
const PRIORITY_LABELS = { high: 'High', medium: 'Medium', low: 'Low' };
const PRIORITY_COLORS = {
  high: { background: '#fee2e2', color: '#dc2626' },
  medium: { background: '#fef3c7', color: '#d97706' },
  low: { background: '#dcfce7', color: '#15803d' },
};
const STATUS_COLORS = {
  open: { background: '#dbeafe', color: '#1d4ed8' },
  in_progress: { background: '#fef3c7', color: '#d97706' },
  done: { background: '#dcfce7', color: '#15803d' },
  closed: { background: '#f3f4f6', color: '#6b7280' },
};

export default function TaskDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [task, setTask] = useState(null);
  const [comments, setComments] = useState([]);
  const [attachments, setAttachments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Edit
  const [editing, setEditing] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editSaving, setEditSaving] = useState(false);
  const [editError, setEditError] = useState('');

  // Status change
  const [statusChanging, setStatusChanging] = useState(false);

  // Comment
  const [commentText, setCommentText] = useState('');
  const [commentSubmitting, setCommentSubmitting] = useState(false);
  const [commentError, setCommentError] = useState('');

  // File upload
  const [uploadFile, setUploadFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');

  const fetchTask = useCallback(async () => {
    try {
      const res = await client.get(`/api/tasks/${id}/`);
      setTask(res.data);
      setEditTitle(res.data.title || '');
      setEditDescription(res.data.description || '');
    } catch (err) {
      setError('Failed to load task.');
      console.error(err);
    }
  }, [id]);

  const fetchComments = useCallback(async () => {
    try {
      const res = await client.get(`/api/tasks/${id}/comments/`);
      setComments(res.data.results ?? res.data);
    } catch (err) {
      console.error('Failed to load comments', err);
    }
  }, [id]);

  const fetchAttachments = useCallback(async () => {
    try {
      const res = await client.get(`/api/tasks/${id}/attachments/`);
      setAttachments(res.data.results ?? res.data);
    } catch (err) {
      // Silently ignore if endpoint doesn't exist
      console.error('Failed to load attachments', err);
    }
  }, [id]);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError('');
      await Promise.all([fetchTask(), fetchComments(), fetchAttachments()]);
      setLoading(false);
    };
    load();
  }, [fetchTask, fetchComments, fetchAttachments]);

  const isOwner =
    user &&
    task &&
    (user.id === task.assignee ||
      user.id === task.assignee_id ||
      user.username === task.assignee_username ||
      user.id === task.created_by ||
      user.id === task.created_by_id ||
      user.username === task.created_by_username);

  const handleStatusChange = async (e) => {
    const newStatus = e.target.value;
    setStatusChanging(true);
    try {
      await client.patch(`/api/tasks/${id}/`, { status: newStatus });
      await fetchTask();
    } catch (err) {
      console.error('Status change failed', err);
    } finally {
      setStatusChanging(false);
    }
  };

  const handleEditSave = async () => {
    setEditSaving(true);
    setEditError('');
    try {
      await client.patch(`/api/tasks/${id}/`, {
        title: editTitle,
        description: editDescription,
      });
      await fetchTask();
      setEditing(false);
    } catch (err) {
      const data = err.response?.data;
      setEditError(data ? Object.values(data).flat().join(' ') : 'Save failed.');
    } finally {
      setEditSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Delete this task? This cannot be undone.')) return;
    try {
      const projectId = task?.project;
      await client.delete(`/api/tasks/${id}/`);
      if (projectId) {
        navigate(`/projects/${projectId}`);
      } else {
        navigate('/projects');
      }
    } catch (err) {
      setError('Failed to delete task.');
    }
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    if (!commentText.trim()) return;
    setCommentSubmitting(true);
    setCommentError('');
    try {
      await client.post(`/api/tasks/${id}/comments/`, {
        body: commentText.trim(),
        content: commentText.trim(),
        text: commentText.trim(),
      });
      setCommentText('');
      await fetchComments();
    } catch (err) {
      const data = err.response?.data;
      setCommentError(data ? Object.values(data).flat().join(' ') : 'Failed to post comment.');
    } finally {
      setCommentSubmitting(false);
    }
  };

  const handleFileChange = (e) => {
    setUploadFile(e.target.files?.[0] || null);
  };

  const handleUpload = async () => {
    if (!uploadFile) return;
    setUploading(true);
    setUploadError('');
    try {
      const formData = new FormData();
      formData.append('file', uploadFile);
      await client.post(`/api/tasks/${id}/attachments/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setUploadFile(null);
      // Reset file input
      const input = document.getElementById('attachment-upload-input');
      if (input) input.value = '';
      await fetchAttachments();
    } catch (err) {
      const data = err.response?.data;
      setUploadError(data ? Object.values(data).flat().join(' ') : 'Upload failed.');
    } finally {
      setUploading(false);
    }
  };

  if (loading) {
    return (
      <div style={styles.page}>
        <div style={styles.centered}>Loading task...</div>
      </div>
    );
  }

  if (error && !task) {
    return (
      <div style={styles.page}>
        <div style={styles.errorBanner}>{error}</div>
      </div>
    );
  }

  const priorityStyle = PRIORITY_COLORS[task?.priority] || {};
  const statusStyle = STATUS_COLORS[task?.status] || {};

  return (
    <div style={styles.page}>
      {/* Back link */}
      {task?.project && (
        <button
          onClick={() => navigate(`/projects/${task.project}`)}
          style={styles.backBtn}
          data-testid="task-back-btn"
          id="task-back-btn"
          name="task-back"
        >
          &larr; Back to Project
        </button>
      )}

      {/* Task header */}
      <div style={styles.taskHeader}>
        <div style={styles.taskHeaderLeft}>
          {editing ? (
            <input
              style={{ ...styles.input, fontSize: '20px', fontWeight: '700', width: '100%' }}
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              data-testid="edit-task-title-input"
              id="edit-task-title-input"
              name="edit-task-title"
            />
          ) : (
            <h1
              data-testid="task-title"
              id="task-title"
              style={styles.taskTitle}
            >
              {task?.title}
            </h1>
          )}
        </div>
        <div style={styles.taskActions}>
          <button
            data-testid="edit-task-btn"
            id="edit-task-btn"
            name="edit-task"
            onClick={() => setEditing(!editing)}
            style={styles.secondaryBtn}
          >
            {editing ? 'Cancel Edit' : 'Edit'}
          </button>
          <button
            data-testid="delete-task-btn"
            id="delete-task-btn"
            name="delete-task"
            onClick={handleDelete}
            style={styles.dangerBtn}
          >
            Delete
          </button>
        </div>
      </div>

      {editing && (
        <div style={styles.editForm}>
          <div style={styles.field}>
            <label style={styles.label}>Description</label>
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              rows={3}
              style={styles.textarea}
              data-testid="edit-task-description-input"
              id="edit-task-description-input"
              name="edit-task-description"
            />
          </div>
          {editError && <div style={styles.errorSmall}>{editError}</div>}
          <button
            onClick={handleEditSave}
            disabled={editSaving}
            style={{ ...styles.primaryBtn, ...(editSaving ? styles.btnDisabled : {}) }}
            data-testid="edit-task-save-btn"
            id="edit-task-save-btn"
            name="edit-task-save"
          >
            {editSaving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      )}

      {error && <div style={styles.errorBanner}>{error}</div>}

      {/* Task meta */}
      <div style={styles.metaRow}>
        <div style={styles.metaItem}>
          <span style={styles.metaLabel}>Status</span>
          <span
            data-testid="task-status"
            id="task-status"
            style={{ ...styles.badge, ...statusStyle }}
          >
            {(task?.status || 'open').replace('_', ' ')}
          </span>
        </div>

        <div style={styles.metaItem}>
          <span style={styles.metaLabel}>Priority</span>
          <span
            data-testid="task-priority"
            id="task-priority"
            style={{ ...styles.badge, ...priorityStyle }}
          >
            {PRIORITY_LABELS[task?.priority] || task?.priority || 'Medium'}
          </span>
        </div>

        <div style={styles.metaItem}>
          <span style={styles.metaLabel}>Assignee</span>
          <span
            data-testid="task-assignee"
            id="task-assignee"
            style={styles.metaValue}
          >
            {task?.assignee_username || 'Unassigned'}
          </span>
        </div>

        <div style={styles.metaItem}>
          <span style={styles.metaLabel}>Change Status</span>
          <select
            data-testid="task-status-select"
            id="task-status-select"
            name="task-status-select"
            value={task?.status || 'open'}
            onChange={handleStatusChange}
            disabled={statusChanging}
            style={{ ...styles.select, ...(statusChanging ? { opacity: 0.6 } : {}) }}
          >
            {STATUS_OPTIONS.map((s) => (
              <option key={s} value={s}>
                {s.replace('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
              </option>
            ))}
          </select>
        </div>
      </div>

      {task?.description && (
        <div style={styles.descriptionBox}>
          <p style={styles.descriptionText}>{task.description}</p>
        </div>
      )}

      {/* Comments */}
      <div
        data-testid="comments-section"
        id="comments-section"
        style={styles.section}
      >
        <h2 style={styles.sectionTitle}>Comments</h2>

        <div style={styles.commentsList}>
          {comments.length === 0 ? (
            <p style={styles.emptyHint}>No comments yet. Be the first to comment.</p>
          ) : (
            comments.map((c) => (
              <CommentItem key={c.id} comment={c} />
            ))
          )}
        </div>

        {/* Comment form */}
        <form onSubmit={handleCommentSubmit} style={styles.commentForm}>
          <textarea
            data-testid="comment-input"
            id="comment-input"
            name="comment"
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            rows={3}
            style={styles.textarea}
            placeholder="Add a comment..."
          />
          {commentError && <div style={styles.errorSmall}>{commentError}</div>}
          <button
            type="submit"
            data-testid="comment-submit-btn"
            id="comment-submit-btn"
            name="comment-submit"
            disabled={commentSubmitting || !commentText.trim()}
            style={{
              ...styles.primaryBtn,
              ...((commentSubmitting || !commentText.trim()) ? styles.btnDisabled : {}),
            }}
          >
            {commentSubmitting ? 'Posting...' : 'Post Comment'}
          </button>
        </form>
      </div>

      {/* Attachments */}
      <div
        data-testid="attachments-section"
        id="attachments-section"
        style={styles.section}
      >
        <h2 style={styles.sectionTitle}>Attachments</h2>

        {attachments.length > 0 && (
          <div style={styles.attachmentsList}>
            {attachments.map((att, i) => (
              <div key={att.id || i} style={styles.attachmentItem}>
                <a
                  href={att.file || att.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={styles.attachmentLink}
                  data-testid={`attachment-${att.id || i}`}
                >
                  {att.filename || att.name || `Attachment ${i + 1}`}
                </a>
              </div>
            ))}
          </div>
        )}

        {attachments.length === 0 && (
          <p style={styles.emptyHint}>No attachments yet.</p>
        )}

        <div style={styles.uploadRow}>
          <input
            type="file"
            data-testid="attachment-upload-input"
            id="attachment-upload-input"
            name="attachment-file"
            onChange={handleFileChange}
            style={styles.fileInput}
          />
          <button
            data-testid="attachment-upload-btn"
            id="attachment-upload-btn"
            name="attachment-upload"
            onClick={handleUpload}
            disabled={!uploadFile || uploading}
            style={{
              ...styles.secondaryBtn,
              ...((!uploadFile || uploading) ? styles.btnDisabled : {}),
            }}
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
        {uploadError && <div style={{ ...styles.errorSmall, marginTop: '8px' }}>{uploadError}</div>}
      </div>
    </div>
  );
}

const styles = {
  page: {
    maxWidth: '900px',
    margin: '0 auto',
    padding: '32px 24px',
  },
  centered: {
    textAlign: 'center',
    padding: '48px 0',
    color: '#6b7280',
    fontSize: '16px',
  },
  backBtn: {
    background: 'none',
    border: 'none',
    color: '#1d4ed8',
    cursor: 'pointer',
    fontSize: '14px',
    padding: '0 0 16px 0',
    fontWeight: '500',
  },
  taskHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '16px',
    gap: '16px',
  },
  taskHeaderLeft: {
    flex: 1,
  },
  taskTitle: {
    margin: 0,
    fontSize: '24px',
    fontWeight: '700',
    color: '#111827',
  },
  taskActions: {
    display: 'flex',
    gap: '8px',
    flexShrink: 0,
  },
  editForm: {
    backgroundColor: '#f9fafb',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '16px',
    marginBottom: '16px',
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  metaRow: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '20px',
    marginBottom: '20px',
    backgroundColor: '#f9fafb',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '16px',
  },
  metaItem: {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
  },
  metaLabel: {
    fontSize: '12px',
    fontWeight: '500',
    color: '#9ca3af',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
  },
  metaValue: {
    fontSize: '14px',
    color: '#374151',
    fontWeight: '500',
  },
  badge: {
    fontSize: '12px',
    fontWeight: '500',
    padding: '3px 10px',
    borderRadius: '12px',
    textTransform: 'capitalize',
    display: 'inline-block',
  },
  descriptionBox: {
    backgroundColor: '#f9fafb',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '16px',
    marginBottom: '24px',
  },
  descriptionText: {
    margin: 0,
    fontSize: '15px',
    color: '#4b5563',
    lineHeight: '1.6',
  },
  section: {
    backgroundColor: '#ffffff',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '24px',
    marginBottom: '20px',
  },
  sectionTitle: {
    margin: '0 0 16px 0',
    fontSize: '17px',
    fontWeight: '600',
    color: '#111827',
  },
  commentsList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    marginBottom: '16px',
  },
  commentForm: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  attachmentsList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
    marginBottom: '14px',
  },
  attachmentItem: {
    padding: '8px 12px',
    backgroundColor: '#f9fafb',
    border: '1px solid #e5e7eb',
    borderRadius: '6px',
  },
  attachmentLink: {
    color: '#1d4ed8',
    textDecoration: 'none',
    fontSize: '14px',
  },
  uploadRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    marginTop: '12px',
  },
  fileInput: {
    fontSize: '14px',
    color: '#374151',
  },
  field: {
    display: 'flex',
    flexDirection: 'column',
    gap: '5px',
  },
  label: {
    fontSize: '13px',
    fontWeight: '500',
    color: '#374151',
  },
  input: {
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    padding: '8px 12px',
    fontSize: '14px',
    color: '#111827',
    backgroundColor: '#ffffff',
    outline: 'none',
  },
  textarea: {
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    padding: '8px 12px',
    fontSize: '14px',
    color: '#111827',
    backgroundColor: '#ffffff',
    outline: 'none',
    resize: 'vertical',
    fontFamily: 'inherit',
    width: '100%',
    boxSizing: 'border-box',
  },
  select: {
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    padding: '7px 10px',
    fontSize: '14px',
    color: '#111827',
    backgroundColor: '#ffffff',
    outline: 'none',
    cursor: 'pointer',
  },
  errorBanner: {
    backgroundColor: '#fee2e2',
    border: '1px solid #fca5a5',
    borderRadius: '6px',
    padding: '12px 16px',
    fontSize: '14px',
    color: '#dc2626',
    marginBottom: '16px',
  },
  errorSmall: {
    backgroundColor: '#fee2e2',
    border: '1px solid #fca5a5',
    borderRadius: '6px',
    padding: '8px 12px',
    fontSize: '13px',
    color: '#dc2626',
  },
  emptyHint: {
    margin: 0,
    fontSize: '14px',
    color: '#9ca3af',
  },
  primaryBtn: {
    backgroundColor: '#1d4ed8',
    color: '#ffffff',
    border: 'none',
    borderRadius: '6px',
    padding: '8px 16px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    alignSelf: 'flex-start',
  },
  secondaryBtn: {
    backgroundColor: '#ffffff',
    color: '#374151',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    padding: '8px 16px',
    fontSize: '14px',
    fontWeight: '500',
    cursor: 'pointer',
  },
  dangerBtn: {
    backgroundColor: '#dc2626',
    color: '#ffffff',
    border: 'none',
    borderRadius: '6px',
    padding: '8px 16px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
  },
  btnDisabled: {
    backgroundColor: '#93c5fd',
    cursor: 'not-allowed',
    opacity: 0.7,
  },
};
