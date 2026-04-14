import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import client from '../api/client';
import TaskCard from '../components/TaskCard';

const TASK_STATUSES = ['', 'open', 'in_progress', 'done', 'closed'];
const TASK_PRIORITIES = ['', 'low', 'medium', 'high'];
const PRIORITY_OPTIONS = ['low', 'medium', 'high'];

export default function ProjectDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Filters
  const [statusFilter, setStatusFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');

  // Edit project
  const [editing, setEditing] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editStatus, setEditStatus] = useState('');
  const [editError, setEditError] = useState('');
  const [editSaving, setEditSaving] = useState(false);

  // Add member
  const [memberInput, setMemberInput] = useState('');
  const [memberError, setMemberError] = useState('');
  const [addingMember, setAddingMember] = useState(false);

  // Create task
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [newTask, setNewTask] = useState({ title: '', description: '', priority: 'medium' });
  const [taskError, setTaskError] = useState('');
  const [creatingTask, setCreatingTask] = useState(false);

  const fetchProject = useCallback(async () => {
    try {
      const res = await client.get(`/api/projects/${id}/`);
      setProject(res.data);
      setEditTitle(res.data.title || res.data.name || '');
      setEditDescription(res.data.description || '');
      setEditStatus(res.data.status || 'active');
      setMembers(res.data.members || []);
    } catch (err) {
      setError('Failed to load project.');
      console.error(err);
    }
  }, [id]);

  const fetchTasks = useCallback(async () => {
    try {
      const params = { project: id };
      if (statusFilter) params.status = statusFilter;
      if (priorityFilter) params.priority = priorityFilter;
      const res = await client.get('/api/tasks/', { params });
      setTasks(res.data.results ?? res.data);
    } catch (err) {
      console.error('Failed to load tasks', err);
    }
  }, [id, statusFilter, priorityFilter]);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError('');
      await Promise.all([fetchProject(), fetchTasks()]);
      setLoading(false);
    };
    load();
  }, [fetchProject, fetchTasks]);

  const isOwner =
    user &&
    project &&
    (user.id === project.owner ||
      user.id === project.owner_id ||
      user.username === project.owner_username);

  const handleEditSave = async () => {
    setEditSaving(true);
    setEditError('');
    try {
      await client.patch(`/api/projects/${id}/`, {
        title: editTitle,
        description: editDescription,
        status: editStatus,
      });
      await fetchProject();
      setEditing(false);
    } catch (err) {
      const data = err.response?.data;
      setEditError(data ? Object.values(data).flat().join(' ') : 'Save failed.');
    } finally {
      setEditSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Delete this project? This cannot be undone.')) return;
    try {
      await client.delete(`/api/projects/${id}/`);
      navigate('/projects');
    } catch (err) {
      setError('Failed to delete project.');
    }
  };

  const handleAddMember = async (e) => {
    e.preventDefault();
    if (!memberInput.trim()) return;
    setAddingMember(true);
    setMemberError('');
    try {
      await client.post(`/api/projects/${id}/add_member/`, {
        username: memberInput.trim(),
      });
      setMemberInput('');
      await fetchProject();
    } catch (err) {
      const data = err.response?.data;
      setMemberError(data?.detail || data?.username?.[0] || 'Failed to add member.');
    } finally {
      setAddingMember(false);
    }
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    if (!newTask.title.trim()) return;
    setCreatingTask(true);
    setTaskError('');
    try {
      await client.post('/api/tasks/', {
        title: newTask.title.trim(),
        description: newTask.description.trim(),
        priority: newTask.priority,
        project: id,
      });
      setNewTask({ title: '', description: '', priority: 'medium' });
      setShowTaskForm(false);
      await fetchTasks();
    } catch (err) {
      const data = err.response?.data;
      setTaskError(data ? Object.values(data).flat().join(' ') : 'Failed to create task.');
    } finally {
      setCreatingTask(false);
    }
  };

  if (loading) {
    return (
      <div style={styles.page}>
        <div style={styles.centered}>Loading project...</div>
      </div>
    );
  }

  if (error && !project) {
    return (
      <div style={styles.page}>
        <div style={styles.errorBanner}>{error}</div>
      </div>
    );
  }

  return (
    <div style={styles.page}>
      {/* Project header */}
      <div style={styles.projectHeader}>
        <div style={styles.projectHeaderLeft}>
          {editing ? (
            <input
              style={{ ...styles.input, fontSize: '22px', fontWeight: '700', width: '100%' }}
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              data-testid="edit-project-title-input"
              id="edit-project-title-input"
              name="edit-project-title"
            />
          ) : (
            <h1
              data-testid="project-title"
              id="project-title"
              style={styles.projectTitle}
            >
              {project?.title || project?.name}
            </h1>
          )}
          <span
            data-testid="project-status"
            id="project-status"
            style={{
              ...styles.statusBadge,
              ...(project?.status === 'active' ? styles.statusActive : styles.statusArchived),
            }}
          >
            {project?.status || 'active'}
          </span>
        </div>

        <div style={styles.projectActions}>
          {isOwner && !editing && (
            <>
              <button
                data-testid="edit-project-btn"
                id="edit-project-btn"
                name="edit-project"
                onClick={() => setEditing(true)}
                style={styles.secondaryBtn}
              >
                Edit
              </button>
              <button
                data-testid="delete-project-btn"
                id="delete-project-btn"
                name="delete-project"
                onClick={handleDelete}
                style={styles.dangerBtn}
              >
                Delete
              </button>
            </>
          )}
          {editing && (
            <>
              <button
                onClick={handleEditSave}
                disabled={editSaving}
                style={{ ...styles.primaryBtn, ...(editSaving ? styles.btnDisabled : {}) }}
                data-testid="edit-project-save-btn"
                id="edit-project-save-btn"
                name="edit-project-save"
              >
                {editSaving ? 'Saving...' : 'Save'}
              </button>
              <button
                onClick={() => setEditing(false)}
                style={styles.secondaryBtn}
                data-testid="edit-project-cancel-btn"
                id="edit-project-cancel-btn"
                name="edit-project-cancel"
              >
                Cancel
              </button>
            </>
          )}
        </div>
      </div>

      {/* Edit form extra fields */}
      {editing && (
        <div style={styles.editForm}>
          <div style={styles.field}>
            <label style={styles.label}>Description</label>
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              rows={3}
              style={styles.textarea}
              data-testid="edit-project-description-input"
              id="edit-project-description-input"
              name="edit-project-description"
            />
          </div>
          <div style={styles.field}>
            <label style={styles.label}>Status</label>
            <select
              value={editStatus}
              onChange={(e) => setEditStatus(e.target.value)}
              style={styles.select}
              data-testid="edit-project-status-select"
              id="edit-project-status-select"
              name="edit-project-status"
            >
              <option value="active">Active</option>
              <option value="archived">Archived</option>
            </select>
          </div>
          {editError && <div style={styles.errorSmall}>{editError}</div>}
        </div>
      )}

      {project?.description && !editing && (
        <p style={styles.description}>{project.description}</p>
      )}

      {error && <div style={styles.errorBanner}>{error}</div>}

      <div style={styles.grid}>
        {/* Members section */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Members</h2>
          <div
            data-testid="members-list"
            id="members-list"
            style={styles.memberList}
          >
            {members.length === 0 ? (
              <p style={styles.emptyHint}>No members yet.</p>
            ) : (
              members.map((m, i) => (
                <div key={m.id || i} style={styles.memberItem}>
                  <span style={styles.memberAvatar}>
                    {(m.username || m)[0]?.toUpperCase()}
                  </span>
                  <span style={styles.memberName}>{m.username || m}</span>
                </div>
              ))
            )}
          </div>

          {/* Add member */}
          <form onSubmit={handleAddMember} style={styles.addMemberForm}>
            <input
              data-testid="add-member-input"
              id="add-member-input"
              name="add-member-username"
              type="text"
              value={memberInput}
              onChange={(e) => setMemberInput(e.target.value)}
              placeholder="Username to add"
              style={{ ...styles.input, flex: 1 }}
            />
            <button
              type="submit"
              data-testid="add-member-btn"
              id="add-member-btn"
              name="add-member-submit"
              disabled={addingMember}
              style={{ ...styles.primaryBtn, ...(addingMember ? styles.btnDisabled : {}) }}
            >
              {addingMember ? '...' : 'Add'}
            </button>
          </form>
          {memberError && <div style={styles.errorSmall}>{memberError}</div>}
        </div>

        {/* Tasks section */}
        <div style={{ flex: 2 }}>
          <div style={styles.tasksHeader}>
            <h2 style={styles.sectionTitle}>Tasks</h2>
            <button
              data-testid="create-task-btn"
              id="create-task-btn"
              name="create-task"
              onClick={() => setShowTaskForm(true)}
              style={styles.primaryBtn}
            >
              + New Task
            </button>
          </div>

          {/* Task filters */}
          <div style={styles.taskFilters}>
            <select
              data-testid="task-filter-status"
              id="task-filter-status"
              name="task-filter-status"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              style={styles.select}
            >
              {TASK_STATUSES.map((s) => (
                <option key={s} value={s}>
                  {s ? s.replace('_', ' ') : 'All Statuses'}
                </option>
              ))}
            </select>
            <select
              data-testid="task-filter-priority"
              id="task-filter-priority"
              name="task-filter-priority"
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              style={styles.select}
            >
              {TASK_PRIORITIES.map((p) => (
                <option key={p} value={p}>
                  {p ? p : 'All Priorities'}
                </option>
              ))}
            </select>
          </div>

          {/* Create task form */}
          {showTaskForm && (
            <div style={styles.formCard}>
              <h3 style={styles.formTitle}>New Task</h3>
              <form onSubmit={handleCreateTask} style={styles.form}>
                <div style={styles.field}>
                  <label style={styles.label}>Title *</label>
                  <input
                    data-testid="new-task-title-input"
                    id="new-task-title-input"
                    name="new-task-title"
                    type="text"
                    value={newTask.title}
                    onChange={(e) => setNewTask((p) => ({ ...p, title: e.target.value }))}
                    required
                    style={styles.input}
                    placeholder="Task title"
                  />
                </div>
                <div style={styles.field}>
                  <label style={styles.label}>Description</label>
                  <textarea
                    data-testid="new-task-description-input"
                    id="new-task-description-input"
                    name="new-task-description"
                    value={newTask.description}
                    onChange={(e) => setNewTask((p) => ({ ...p, description: e.target.value }))}
                    rows={2}
                    style={styles.textarea}
                    placeholder="Optional description"
                  />
                </div>
                <div style={styles.field}>
                  <label style={styles.label}>Priority</label>
                  <select
                    data-testid="new-task-priority-select"
                    id="new-task-priority-select"
                    name="new-task-priority"
                    value={newTask.priority}
                    onChange={(e) => setNewTask((p) => ({ ...p, priority: e.target.value }))}
                    style={styles.select}
                  >
                    {PRIORITY_OPTIONS.map((p) => (
                      <option key={p} value={p}>
                        {p.charAt(0).toUpperCase() + p.slice(1)}
                      </option>
                    ))}
                  </select>
                </div>
                {taskError && <div style={styles.errorSmall}>{taskError}</div>}
                <div style={styles.formActions}>
                  <button
                    type="submit"
                    data-testid="new-task-submit-btn"
                    id="new-task-submit-btn"
                    name="new-task-submit"
                    disabled={creatingTask}
                    style={{ ...styles.primaryBtn, ...(creatingTask ? styles.btnDisabled : {}) }}
                  >
                    {creatingTask ? 'Creating...' : 'Create Task'}
                  </button>
                  <button
                    type="button"
                    onClick={() => { setShowTaskForm(false); setTaskError(''); }}
                    style={styles.secondaryBtn}
                    data-testid="new-task-cancel-btn"
                    id="new-task-cancel-btn"
                    name="new-task-cancel"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Tasks list */}
          <div
            data-testid="tasks-list"
            id="tasks-list"
            style={styles.tasksList}
          >
            {tasks.length === 0 ? (
              <p style={styles.emptyHint}>No tasks found.</p>
            ) : (
              tasks.map((task) => (
                <TaskCard key={task.id} task={task} />
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    maxWidth: '1100px',
    margin: '0 auto',
    padding: '32px 24px',
  },
  centered: {
    textAlign: 'center',
    padding: '48px 0',
    color: '#6b7280',
    fontSize: '16px',
  },
  projectHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '12px',
    gap: '16px',
  },
  projectHeaderLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: '14px',
    flex: 1,
  },
  projectTitle: {
    margin: 0,
    fontSize: '26px',
    fontWeight: '700',
    color: '#111827',
  },
  projectActions: {
    display: 'flex',
    gap: '8px',
    flexShrink: 0,
  },
  statusBadge: {
    fontSize: '13px',
    fontWeight: '500',
    padding: '3px 12px',
    borderRadius: '12px',
    textTransform: 'capitalize',
    whiteSpace: 'nowrap',
  },
  statusActive: {
    background: '#dcfce7',
    color: '#15803d',
  },
  statusArchived: {
    background: '#f3f4f6',
    color: '#6b7280',
  },
  description: {
    margin: '0 0 24px 0',
    fontSize: '15px',
    color: '#4b5563',
    lineHeight: '1.6',
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
  grid: {
    display: 'flex',
    gap: '28px',
    alignItems: 'flex-start',
    marginTop: '24px',
  },
  section: {
    flex: 1,
    backgroundColor: '#ffffff',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '20px',
  },
  sectionTitle: {
    margin: '0 0 14px 0',
    fontSize: '17px',
    fontWeight: '600',
    color: '#111827',
  },
  memberList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    marginBottom: '14px',
  },
  memberItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  memberAvatar: {
    width: '28px',
    height: '28px',
    backgroundColor: '#dbeafe',
    color: '#1d4ed8',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: '600',
    fontSize: '13px',
  },
  memberName: {
    fontSize: '14px',
    color: '#374151',
  },
  addMemberForm: {
    display: 'flex',
    gap: '8px',
  },
  tasksHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px',
  },
  taskFilters: {
    display: 'flex',
    gap: '10px',
    marginBottom: '16px',
  },
  tasksList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  formCard: {
    backgroundColor: '#ffffff',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '20px',
    marginBottom: '16px',
  },
  formTitle: {
    margin: '0 0 14px 0',
    fontSize: '16px',
    fontWeight: '600',
    color: '#111827',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
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
  },
  select: {
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    padding: '8px 12px',
    fontSize: '14px',
    color: '#111827',
    backgroundColor: '#ffffff',
    outline: 'none',
    cursor: 'pointer',
  },
  formActions: {
    display: 'flex',
    gap: '8px',
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
  },
};
