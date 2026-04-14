import { useNavigate } from 'react-router-dom';

const PRIORITY_COLORS = {
  high: { background: '#fee2e2', color: '#dc2626' },
  medium: { background: '#fef3c7', color: '#d97706' },
  low: { background: '#dcfce7', color: '#15803d' },
  default: { background: '#f3f4f6', color: '#6b7280' },
};

const STATUS_COLORS = {
  open: { background: '#dbeafe', color: '#1d4ed8' },
  in_progress: { background: '#fef3c7', color: '#d97706' },
  done: { background: '#dcfce7', color: '#15803d' },
  closed: { background: '#f3f4f6', color: '#6b7280' },
  default: { background: '#f3f4f6', color: '#6b7280' },
};

export default function TaskCard({ task }) {
  const navigate = useNavigate();
  const priorityStyle = PRIORITY_COLORS[task.priority] || PRIORITY_COLORS.default;
  const statusStyle = STATUS_COLORS[task.status] || STATUS_COLORS.default;

  return (
    <div
      data-testid={`task-card-${task.id}`}
      id={`task-card-${task.id}`}
      onClick={() => navigate(`/tasks/${task.id}`)}
      style={styles.card}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && navigate(`/tasks/${task.id}`)}
    >
      <div style={styles.header}>
        <h4 style={styles.title}>{task.title}</h4>
        <div style={styles.badges}>
          <span style={{ ...styles.badge, ...priorityStyle }}>
            {task.priority || 'medium'}
          </span>
          <span style={{ ...styles.badge, ...statusStyle }}>
            {(task.status || 'open').replace('_', ' ')}
          </span>
        </div>
      </div>
      {task.description && (
        <p style={styles.description}>{task.description}</p>
      )}
      {task.assignee_username && (
        <p style={styles.assignee}>Assigned to: {task.assignee_username}</p>
      )}
    </div>
  );
}

const styles = {
  card: {
    backgroundColor: '#ffffff',
    border: '1px solid #e5e7eb',
    borderRadius: '6px',
    padding: '14px 16px',
    cursor: 'pointer',
    boxShadow: '0 1px 2px rgba(0,0,0,0.04)',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '6px',
  },
  title: {
    margin: 0,
    fontSize: '14px',
    fontWeight: '600',
    color: '#111827',
  },
  badges: {
    display: 'flex',
    gap: '6px',
  },
  badge: {
    fontSize: '11px',
    fontWeight: '500',
    padding: '2px 8px',
    borderRadius: '10px',
    textTransform: 'capitalize',
    whiteSpace: 'nowrap',
  },
  description: {
    margin: '0 0 6px 0',
    fontSize: '13px',
    color: '#6b7280',
    lineHeight: '1.4',
  },
  assignee: {
    margin: 0,
    fontSize: '12px',
    color: '#9ca3af',
  },
};
