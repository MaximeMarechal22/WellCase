import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import './index.css';
import HomePage from './pages/HomePage';
import CasesPage from './pages/CasesPage';
import CaseDetailPage from './pages/CaseDetailPage';
import InventoryPage from './pages/InventoryPage';
import UpgradePage from './pages/UpgradePage';
import HistoryPage from './pages/HistoryPage';
import ProfilePage from './pages/ProfilePage';
import AdminPage from './pages/AdminPage';
import MissionsPage from './pages/MissionsPage';
import LeaderboardPage from './pages/LeaderboardPage';
import GuidePage from './pages/GuidePage';
import BattlePassPage from './pages/BattlePassPage';
import MarketPage from './pages/MarketPage';
import CollectionsPage from './pages/CollectionsPage';
import './pages/CollectionsPage.css';
import './pages/MarketPage.css';
import Navbar from './components/Navbar';
import { AuthProvider, useAuth } from './context/AuthContext';

const AdminRoute = ({ children }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="app-loading" role="status" aria-live="polite">
        <div className="spinner-border text-primary" aria-hidden="true"></div>
        <span>Loading...</span>
      </div>
    );
  }

  if (!user) return <Navigate to="/login" replace state={{ from: location }} />;
  if (!user.is_admin) return <Navigate to="/" replace />;
  return children;
};

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="app-loading" role="status" aria-live="polite">
        <div className="spinner-border text-primary" aria-hidden="true"></div>
        <span>Loading your CaseForge account...</span>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return children;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Navbar />
          <main className="app-main">
            <Routes>
              <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
              <Route path="/cases" element={<ProtectedRoute><CasesPage /></ProtectedRoute>} />
              <Route path="/cases/:caseId" element={<ProtectedRoute><CaseDetailPage /></ProtectedRoute>} />
              <Route path="/inventory" element={<ProtectedRoute><InventoryPage /></ProtectedRoute>} />
              <Route path="/upgrade" element={<ProtectedRoute><UpgradePage /></ProtectedRoute>} />
              <Route path="/history" element={<ProtectedRoute><HistoryPage /></ProtectedRoute>} />
              <Route path="/leaderboard" element={<ProtectedRoute><LeaderboardPage /></ProtectedRoute>} />
              <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
              <Route path="/admin" element={<AdminRoute><AdminPage /></AdminRoute>} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/missions" element={<ProtectedRoute><MissionsPage /></ProtectedRoute>} />
              <Route path="/battle-pass" element={<ProtectedRoute><BattlePassPage /></ProtectedRoute>} />
              <Route path="/guide" element={<ProtectedRoute><GuidePage /></ProtectedRoute>} />
              <Route path="/market" element={<ProtectedRoute><MarketPage /></ProtectedRoute>} />
              <Route path="/collections" element={<ProtectedRoute><CollectionsPage /></ProtectedRoute>} />
              <Route path="/register" element={<RegisterPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

// Login Page
const LoginPage = () => {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const result = await login(username, password);
      if (result.success) {
        window.location.href = '/';
      } else {
        setError(result.error || 'Login failed');
      }
    } catch (err) {
      setError('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6 col-lg-4">
          <div className="card shadow-lg">
            <div className="card-body p-5">
              <h2 className="text-center mb-4">Welcome Back</h2>
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Username</label>
                  <input
                    type="text"
                    className="form-control"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="btn btn-primary w-100"
                  disabled={loading}
                >
                  {loading ? 'Logging in...' : 'Login'}
                </button>
              </form>
              {error && (
                <div className="alert alert-danger mt-3">
                  {error}
                </div>
              )}
              <div className="text-center mt-4">
                <p>Don't have an account?</p>
                <Link to="/register" className="text-decoration-none">Register</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Register Page
const RegisterPage = () => {
  const { register, login } = useAuth();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    try {
      const result = await register({
        username,
        email,
        password
      });

      if (result.success) {
        setSuccess(true);
        // Auto-login after registration
        const loginResult = await login(username, password);
        if (loginResult.success) {
          setTimeout(() => {
            window.location.href = '/';
          }, 1500);
        }
      } else {
        setError(result.error || 'Registration failed');
      }
    } catch (err) {
      setError('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="container mt-5">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-4">
            <div className="card shadow-lg">
              <div className="card-body p-5 text-center">
                <div className="mb-4">
                  <i className="bi bi-check-circle display-1 text-success"></i>
                </div>
                <h2>Account Created!</h2>
                <p className="text-muted">Redirecting to login...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6 col-lg-4">
          <div className="card shadow-lg">
            <div className="card-body p-5">
              <h2 className="text-center mb-4">Create Account</h2>
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Username</label>
                  <input
                    type="text"
                    className="form-control"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Email</label>
                  <input
                    type="email"
                    className="form-control"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    minLength="6"
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Confirm Password</label>
                  <input
                    type="password"
                    className="form-control"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    minLength="6"
                  />
                </div>
                <button
                  type="submit"
                  className="btn btn-primary w-100"
                  disabled={loading}
                >
                  {loading ? 'Creating account...' : 'Register'}
                </button>
              </form>
              {error && (
                <div className="alert alert-danger mt-3">
                  {error}
                </div>
              )}
              {success && (
                <div className="alert alert-success mt-3">
                  Account created successfully!
                </div>
              )}
              <div className="text-center mt-4">
                <p>Already have an account?</p>
                <Link to="/login" className="text-decoration-none">Login</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;