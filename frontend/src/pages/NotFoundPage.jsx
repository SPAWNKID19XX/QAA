import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <div style={styles.page}>
      <h1 style={styles.code}>404</h1>
      <h2 style={styles.title}>Page Not Found</h2>
      <p style={styles.text}>
        The page you are looking for doesn&apos;t exist or has been moved.
      </p>
      <Link to="/projects" style={styles.link} data-testid="not-found-home-link">
        Go to Projects
      </Link>
    </div>
  );
}

const styles = {
  page: {
    minHeight: '60vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '48px 24px',
    textAlign: 'center',
  },
  code: {
    fontSize: '80px',
    fontWeight: '800',
    color: '#1d4ed8',
    margin: '0 0 8px 0',
    lineHeight: 1,
  },
  title: {
    fontSize: '24px',
    fontWeight: '700',
    color: '#111827',
    margin: '0 0 12px 0',
  },
  text: {
    fontSize: '16px',
    color: '#6b7280',
    margin: '0 0 28px 0',
  },
  link: {
    backgroundColor: '#1d4ed8',
    color: '#ffffff',
    textDecoration: 'none',
    borderRadius: '6px',
    padding: '10px 22px',
    fontSize: '15px',
    fontWeight: '600',
  },
};
