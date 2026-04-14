export default function CommentItem({ comment }) {
  const date = comment.created_at
    ? new Date(comment.created_at).toLocaleString()
    : '';

  return (
    <div
      data-testid={`comment-${comment.id}`}
      id={`comment-${comment.id}`}
      style={styles.comment}
    >
      <div style={styles.header}>
        <span style={styles.author}>
          {comment.author_username || comment.author || 'Unknown'}
        </span>
        {date && <span style={styles.date}>{date}</span>}
      </div>
      <p style={styles.body}>{comment.body || comment.content || comment.text}</p>
    </div>
  );
}

const styles = {
  comment: {
    backgroundColor: '#f9fafb',
    border: '1px solid #e5e7eb',
    borderRadius: '6px',
    padding: '12px 16px',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '6px',
  },
  author: {
    fontWeight: '600',
    fontSize: '13px',
    color: '#374151',
  },
  date: {
    fontSize: '12px',
    color: '#9ca3af',
  },
  body: {
    margin: 0,
    fontSize: '14px',
    color: '#4b5563',
    lineHeight: '1.5',
  },
};
