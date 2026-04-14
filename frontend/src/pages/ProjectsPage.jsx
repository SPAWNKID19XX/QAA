import { useState, useEffect, useCallback } from 'react';
import client from '../api/client';
import ProjectCard from '../components/ProjectCard';

const FILTERS = ['all', 'active', 'archived'];

export default function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Create form state
  const [showForm, setShowForm] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState('');

  const fetchProjects = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params = filter !== 'all' ? { status: filter === 'archived' ? 'archive' : filter } : {};
      const res = await client.get('/api/projects/', { params });
      setProjects(res.data.results ?? res.data);
    } catch (err) {
      setError('Failed to load projects.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    setCreating(true);
    setCreateError('');
    try {
      await client.post('/api/projects/', {
        title: newTitle.trim(),
        description: newDescription.trim(),
      });
      setNewTitle('');
      setNewDescription('');
      setShowForm(false);
      fetchProjects();
    } catch (err) {
      const data = err.response?.data;
      const msg = data
        ? Object.values(data).flat().join(' ')
        : 'Failed to create project.';
      setCreateError(msg);
    } finally {
      setCreating(false);
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setNewTitle('');
    setNewDescription('');
    setCreateError('');
  };

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <h1
          data-testid="projects-page-title"
          id="projects-page-title"
          style={styles.title}
        >
          Projects
        </h1>
        <button
          data-testid="create-project-btn"
          id="create-project-btn"
          name="create-project"
          onClick={() => setShowForm(true)}
          style={styles.primaryBtn}
        >
          + New Project
        </button>
      </div>

      {/* Filter buttons */}
      <div style={styles.filters}>
        {FILTERS.map((f) => (
          <button
            key={f}
            data-testid={`filter-${f}`}
            id={`filter-${f}`}
            name={`filter-${f}`}
            onClick={() => setFilter(f)}
            style={{
              ...styles.filterBtn,
              ...(filter === f ? styles.filterBtnActive : {}),
            }}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Create project form */}
      {showForm && (
        <div style={styles.formCard}>
          <h2 style={styles.formTitle}>New Project</h2>
          <form onSubmit={handleCreate} style={styles.form}>
            <div style={styles.field}>
              <label htmlFor="new-project-title" style={styles.label}>
                Title <span style={{ color: '#dc2626' }}>*</span>
              </label>
              <input
                id="new-project-title"
                name="new-project-title"
                data-testid="new-project-title-input"
                type="text"
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                required
                style={styles.input}
                placeholder="Project title"
              />
            </div>
            <div style={styles.field}>
              <label htmlFor="new-project-description" style={styles.label}>
                Description
              </label>
              <textarea
                id="new-project-description"
                name="new-project-description"
                data-testid="new-project-description-input"
                value={newDescription}
                onChange={(e) => setNewDescription(e.target.value)}
                rows={3}
                style={styles.textarea}
                placeholder="Optional description"
              />
            </div>
            {createError && (
              <div style={styles.error}>{createError}</div>
            )}
            <div style={styles.formActions}>
              <button
                type="submit"
                data-testid="new-project-submit-btn"
                id="new-project-submit-btn"
                name="new-project-submit"
                disabled={creating}
                style={{
                  ...styles.primaryBtn,
                  ...(creating ? styles.btnDisabled : {}),
                }}
              >
                {creating ? 'Creating...' : 'Create Project'}
              </button>
              <button
                type="button"
                data-testid="new-project-cancel-btn"
                id="new-project-cancel-btn"
                name="new-project-cancel"
                onClick={handleCancel}
                style={styles.secondaryBtn}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Content */}
      {loading ? (
        <div
          data-testid="projects-loading"
          id="projects-loading"
          style={styles.centered}
        >
          Loading projects...
        </div>
      ) : error ? (
        <div style={styles.errorBanner}>{error}</div>
      ) : projects.length === 0 ? (
        <div
          data-testid="projects-empty"
          id="projects-empty"
          style={styles.empty}
        >
          <p style={styles.emptyText}>No projects found.</p>
          <p style={styles.emptyHint}>
            {filter !== 'all'
              ? `No ${filter} projects. Try a different filter.`
              : 'Create your first project to get started.'}
          </p>
        </div>
      ) : (
        <div
          data-testid="projects-list"
          id="projects-list"
          style={styles.list}
        >
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  page: {
    maxWidth: '900px',
    margin: '0 auto',
    padding: '32px 24px',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
  },
  title: {
    margin: 0,
    fontSize: '28px',
    fontWeight: '700',
    color: '#111827',
  },
  filters: {
    display: 'flex',
    gap: '8px',
    marginBottom: '24px',
  },
  filterBtn: {
    backgroundColor: '#ffffff',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    padding: '7px 16px',
    fontSize: '14px',
    cursor: 'pointer',
    color: '#374151',
  },
  filterBtnActive: {
    backgroundColor: '#1d4ed8',
    border: '1px solid #1d4ed8',
    color: '#ffffff',
  },
  primaryBtn: {
    backgroundColor: '#1d4ed8',
    color: '#ffffff',
    border: 'none',
    borderRadius: '6px',
    padding: '9px 18px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
  },
  secondaryBtn: {
    backgroundColor: '#ffffff',
    color: '#374151',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    padding: '9px 18px',
    fontSize: '14px',
    fontWeight: '500',
    cursor: 'pointer',
  },
  btnDisabled: {
    backgroundColor: '#93c5fd',
    cursor: 'not-allowed',
  },
  formCard: {
    backgroundColor: '#ffffff',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '24px',
    marginBottom: '24px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
  },
  formTitle: {
    margin: '0 0 16px 0',
    fontSize: '18px',
    fontWeight: '600',
    color: '#111827',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '14px',
  },
  field: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
  },
  label: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#374151',
  },
  input: {
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    padding: '9px 12px',
    fontSize: '14px',
    color: '#111827',
    backgroundColor: '#ffffff',
    outline: 'none',
  },
  textarea: {
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    padding: '9px 12px',
    fontSize: '14px',
    color: '#111827',
    backgroundColor: '#ffffff',
    outline: 'none',
    resize: 'vertical',
    fontFamily: 'inherit',
  },
  formActions: {
    display: 'flex',
    gap: '10px',
  },
  error: {
    backgroundColor: '#fee2e2',
    border: '1px solid #fca5a5',
    borderRadius: '6px',
    padding: '10px 12px',
    fontSize: '14px',
    color: '#dc2626',
  },
  errorBanner: {
    backgroundColor: '#fee2e2',
    border: '1px solid #fca5a5',
    borderRadius: '6px',
    padding: '14px 16px',
    fontSize: '14px',
    color: '#dc2626',
  },
  centered: {
    textAlign: 'center',
    padding: '48px 0',
    color: '#6b7280',
    fontSize: '16px',
  },
  empty: {
    textAlign: 'center',
    padding: '48px 0',
  },
  emptyText: {
    margin: '0 0 8px 0',
    fontSize: '18px',
    fontWeight: '600',
    color: '#374151',
  },
  emptyHint: {
    margin: 0,
    fontSize: '14px',
    color: '#9ca3af',
  },
  list: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
};
