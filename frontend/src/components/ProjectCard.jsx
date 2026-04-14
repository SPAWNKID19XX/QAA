import { useNavigate } from 'react-router-dom';

const STATUS_COLORS = {
  active: { background: '#dcfce7', color: '#15803d' },
  archived: { background: '#f3f4f6', color: '#6b7280' },
  default: { background: '#dbeafe', color: '#1d4ed8' },
};

export default function ProjectCard({ project }) {
  const navigate = useNavigate();
  const statusStyle = STATUS_COLORS[project.status] || STATUS_COLORS.default;

  return (
    <div
      data-testid={`project-card-${project.id}`}
      id={`project-card-${project.id}`}
      onClick={() => navigate(`/projects/${project.id}`)}
      style={styles.card}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && navigate(`/projects/${project.id}`)}
    >
      <div style={styles.header}>
        <h3 style={styles.title}>{project.title || project.name}</h3>
        <span
          style={{ ...styles.badge, ...statusStyle }}
        >
          {project.status || 'active'}
        </span>
      </div>
      {project.description && (
        <p style={styles.description}>{project.description}</p>
      )}
      <div style={styles.footer}>
        <span style={styles.meta}>
          Tasks: {project.task_count ?? project.tasks?.length ?? 0}
        </span>
        {project.owner_username && (
          <span style={styles.meta}>Owner: {project.owner_username}</span>
        )}
      </div>
    </div>
  );
}

const styles = {
  card: {
    backgroundColor: '#ffffff',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '20px',
    cursor: 'pointer',
    transition: 'box-shadow 0.15s ease',
    boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '8px',
  },
  title: {
    margin: 0,
    fontSize: '16px',
    fontWeight: '600',
    color: '#111827',
  },
  badge: {
    fontSize: '12px',
    fontWeight: '500',
    padding: '2px 10px',
    borderRadius: '12px',
    textTransform: 'capitalize',
  },
  description: {
    margin: '0 0 12px 0',
    fontSize: '14px',
    color: '#6b7280',
    lineHeight: '1.5',
  },
  footer: {
    display: 'flex',
    gap: '16px',
  },
  meta: {
    fontSize: '12px',
    color: '#9ca3af',
  },
};
