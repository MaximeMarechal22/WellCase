import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, dashboardAPI } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [balance, setBalance] = useState(0);

  useEffect(() => {
    const loadUserData = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const userData = await authAPI.getCurrentUser();
          setUser(userData.data);
          // Get balance
          const balanceData = await dashboardAPI.getBalance();
          setBalance(balanceData.data.balance);
        } catch (error) {
          console.error('Failed to load user data:', error);
          if (error.response?.status === 401) {
            localStorage.removeItem('token');
            setUser(null);
            setBalance(0);
          }
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };

    loadUserData();
  }, []);

  const login = async (username, password) => {
    try {
      const response = await authAPI.login(username, password);
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      // Update axios defaults to include the token
      const userData = await authAPI.getCurrentUser();
      setUser(userData.data);
      // Get balance
      const balanceData = await dashboardAPI.getBalance();
      setBalance(balanceData.data.balance);
      return { success: true };
    } catch (error) {
      console.error('Login failed:', error);
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Registration failed:', error);
      return { success: false, error: error.response?.data?.detail || 'Registration failed' };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setBalance(0);
    window.location.href = '/login';
  };

  const updateBalance = async (knownBalance = null) => {
    if (knownBalance !== null && Number.isFinite(Number(knownBalance))) {
      setBalance(Number(knownBalance));
      return;
    }
    if (user) {
      try {
        const balanceData = await dashboardAPI.getBalance();
        setBalance(Number(balanceData.data.balance));
      } catch (error) {
        console.error('Failed to update balance:', error);
      }
    }
  };

  const value = {
    user,
    loading,
    balance,
    login,
    register,
    logout,
    updateBalance
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
