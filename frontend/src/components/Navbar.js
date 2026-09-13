import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ImageWithFallback from './ImageWithFallback';
import logo from '../assets/branding/wellcase-wordmark.png';

const Navbar = () => {
  const location = useLocation();
  const { user, balance, logout } = useAuth();

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark mb-4 border-bottom border-secondary-subtle">
      <div className="container-fluid">
        <Link className="navbar-brand wellcase-brand" to="/" aria-label="WellCase">
          <img src={logo} alt="WELLCASE" className="wellcase-logo" />
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className={`nav-item ${location.pathname === '/' ? 'active' : ''}`}>
              <Link className="nav-link px-3" to="/">Home</Link>
            </li>
            <li className={`nav-item ${location.pathname === '/cases' ? 'active' : ''}`}>
              <Link className="nav-link px-3" to="/cases">Cases</Link>
            </li>
            <li className={`nav-item ${location.pathname === '/market' ? 'active' : ''}`}><Link className="nav-link px-3" to="/market">Marché</Link></li>
            <li className={`nav-item ${location.pathname === '/collections' ? 'active' : ''}`}><Link className="nav-link px-3" to="/collections">Collections</Link></li>
            <li className={`nav-item ${location.pathname === '/inventory' ? 'active' : ''}`}>
              <Link className="nav-link px-3" to="/inventory">Inventory</Link>
            </li>
            <li className={`nav-item ${location.pathname === '/upgrade' ? 'active' : ''}`}>
              <Link className="nav-link px-3" to="/upgrade">Upgrade</Link>
            </li>
            <li className={`nav-item ${location.pathname === '/history' ? 'active' : ''}`}>
              <Link className="nav-link px-3" to="/history">History</Link>
            </li>
            <li className={`nav-item ${location.pathname === '/leaderboard' ? 'active' : ''}`}><Link className="nav-link px-3" to="/leaderboard">Leaderboard</Link></li>
            <li className={`nav-item ${location.pathname === '/profile' ? 'active' : ''}`}>
              <Link className="nav-link px-3" to="/profile">Profile</Link>
            </li>
            <li className={`nav-item ${location.pathname === '/missions' ? 'active' : ''}`}><Link className="nav-link px-3" to="/missions">Quêtes</Link></li>
            <li className={`nav-item ${location.pathname === '/battle-pass' ? 'active' : ''}`}><Link className="nav-link px-3" to="/battle-pass">Pass</Link></li>
            <li className={`nav-item ${location.pathname === '/guide' ? 'active' : ''}`}><Link className="nav-link px-3" to="/guide">Guide</Link></li>
            {user?.is_admin && (
              <li className={`nav-item ${location.pathname === '/admin' ? 'active' : ''}`}>
                <Link className="nav-link px-3" to="/admin">Admin</Link>
              </li>
            )}
          </ul>
          <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
            {/* Balance Display */}
            <li className="nav-item d-flex align-items-center">
              <div className="me-3">
                <span className="me-2">
                  <i className="bi bi-wallet2"></i>
                </span>
                <span className="balance-text fw-medium">{balance.toLocaleString()} €</span>
              </div>
            </li>
            
            {/* User Dropdown */}
            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle d-flex align-items-center" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                {user ? (
                  <>
                    <ImageWithFallback
                         src={user?.avatar_url || "/images/avatars/default.png"}
                         alt="Avatar"
                         className="rounded-circle me-2"
                         style={{ width: '32px', height: '32px', objectFit: 'cover' }}
                    />
                    <span className="d-none d-md-inline" style={{color:user?.name_color&&user.name_color!=='white'?user.name_color:undefined}}>{user.username}</span>
                  </>
                ) : (
                  <span className="d-none d-md-inline">Player</span>
                )}
              </a>
              <ul className="dropdown-menu dropdown-menu-end">
                {user ? (
                  <>
                    <li><Link className="dropdown-item" to="/profile">My Profile</Link></li>
                    <li><hr className="dropdown-divider" /></li>
                    <li><button type="button" className="dropdown-item" onClick={logout}>Logout</button></li>
                  </>
                ) : (
                  <>
                    <li><Link className="dropdown-item" to="/login">Login</Link></li>
                    <li><Link className="dropdown-item" to="/register">Register</Link></li>
                  </>
                )}
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
