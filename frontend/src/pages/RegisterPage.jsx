import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (form.password !== form.password_confirm) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      await register(form.username, form.email, form.password);
      setSuccess('Account created successfully! Redirecting to login...');
      setTimeout(() => navigate('/login'), 1500);
    } catch (err) {
      const data = err.response?.data;
      if (data) {
        const messages = Object.values(data).flat().join(' ');
        setError(messages || 'Registration failed.');
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.heading}>Create Account</h1>
        <p style={styles.sub}>QAA Training App</p>

        <form onSubmit={handleSubmit} style={styles.form} noValidate>
          <div style={styles.field}>
            <label htmlFor="username" style={styles.label}>
              Username
            </label>
            <input
              id="username"
              name="username"
              data-testid="register-username-input"
              type="text"
              value={form.username}
              onChange={handleChange}
              required
              autoComplete="username"
              style={styles.input}
              placeholder="Choose a username"
            />
          </div>

          <div style={styles.field}>
            <label htmlFor="email" style={styles.label}>
              Email
            </label>
            <input
              id="email"
              name="email"
              data-testid="register-email-input"
              type="email"
              value={form.email}
              onChange={handleChange}
              required
              autoComplete="email"
              style={styles.input}
              placeholder="Enter your email"
            />
          </div>

          <div style={styles.field}>
            <label htmlFor="password" style={styles.label}>
              Password
            </label>
            <input
              id="password"
              name="password"
              data-testid="register-password-input"
              type="password"
              value={form.password}
              onChange={handleChange}
              required
              autoComplete="new-password"
              style={styles.input}
              placeholder="Choose a password"
            />
          </div>

          <div style={styles.field}>
            <label htmlFor="password_confirm" style={styles.label}>
              Confirm Password
            </label>
            <input
              id="password_confirm"
              name="password_confirm"
              data-testid="register-password-confirm-input"
              type="password"
              value={form.password_confirm}
              onChange={handleChange}
              required
              autoComplete="new-password"
              style={styles.input}
              placeholder="Repeat your password"
            />
          </div>

          {error && (
            <div
              data-testid="register-error-msg"
              id="register-error-msg"
              role="alert"
              style={styles.error}
            >
              {error}
            </div>
          )}

          {success && (
            <div
              data-testid="register-success-msg"
              id="register-success-msg"
              role="status"
              style={styles.success}
            >
              {success}
            </div>
          )}

          <button
            type="submit"
            data-testid="register-submit-btn"
            id="register-submit-btn"
            name="register-submit"
            disabled={loading}
            style={{ ...styles.btn, ...(loading ? styles.btnDisabled : {}) }}
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>

        <p style={styles.footer}>
          Already have an account?{' '}
          <Link
            to="/login"
            data-testid="login-link"
            id="login-link"
            style={styles.link}
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f3f4f6',
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: '10px',
    padding: '40px',
    width: '100%',
    maxWidth: '420px',
    boxShadow: '0 4px 16px rgba(0,0,0,0.08)',
  },
  heading: {
    margin: '0 0 4px 0',
    fontSize: '24px',
    fontWeight: '700',
    color: '#111827',
    textAlign: 'center',
  },
  sub: {
    margin: '0 0 28px 0',
    fontSize: '14px',
    color: '#6b7280',
    textAlign: 'center',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
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
    padding: '10px 12px',
    fontSize: '14px',
    outline: 'none',
    color: '#111827',
    backgroundColor: '#ffffff',
  },
  error: {
    backgroundColor: '#fee2e2',
    border: '1px solid #fca5a5',
    borderRadius: '6px',
    padding: '10px 12px',
    fontSize: '14px',
    color: '#dc2626',
  },
  success: {
    backgroundColor: '#dcfce7',
    border: '1px solid #86efac',
    borderRadius: '6px',
    padding: '10px 12px',
    fontSize: '14px',
    color: '#15803d',
  },
  btn: {
    backgroundColor: '#1d4ed8',
    color: '#ffffff',
    border: 'none',
    borderRadius: '6px',
    padding: '11px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
    marginTop: '4px',
  },
  btnDisabled: {
    backgroundColor: '#93c5fd',
    cursor: 'not-allowed',
  },
  footer: {
    marginTop: '20px',
    textAlign: 'center',
    fontSize: '14px',
    color: '#6b7280',
  },
  link: {
    color: '#1d4ed8',
    fontWeight: '500',
    textDecoration: 'none',
  },
};
