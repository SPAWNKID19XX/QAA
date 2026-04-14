import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav style={styles.nav}>
      <div style={styles.left}>
        <Link
          to="/projects"
          style={styles.brand}
          data-testid="navbar-title"
        >
          QAA Training App
        </Link>
        {user && (
          <Link
            to="/projects"
            style={styles.link}
            data-testid="navbar-projects-link"
          >
            Projects
          </Link>
        )}
      </div>
      {user && (
        <div style={styles.right}>
          <span
            data-testid="navbar-username"
            style={styles.username}
          >
            {user.username}
          </span>
          <button
            data-testid="navbar-logout-btn"
            id="navbar-logout-btn"
            name="logout"
            onClick={handleLogout}
            style={styles.logoutBtn}
          >
            Logout
          </button>
        </div>
      )}
    </nav>
  );
}

const styles = {
  nav: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#1d4ed8',
    padding: '0 24px',
    height: '56px',
  },
  left: {
    display: 'flex',
    alignItems: 'center',
    gap: '24px',
  },
  brand: {
    color: '#ffffff',
    fontWeight: '700',
    fontSize: '18px',
    textDecoration: 'none',
  },
  link: {
    color: '#bfdbfe',
    textDecoration: 'none',
    fontSize: '14px',
  },
  right: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
  },
  username: {
    color: '#bfdbfe',
    fontSize: '14px',
  },
  logoutBtn: {
    backgroundColor: 'transparent',
    border: '1px solid #bfdbfe',
    color: '#bfdbfe',
    padding: '6px 14px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
};
