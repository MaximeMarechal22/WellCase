import axios from 'axios';

const API_BASE_URL =
  process.env.REACT_APP_API_URL ||
  (process.env.NODE_ENV === 'production' ? '' : 'http://127.0.0.1:8000');

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');

    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => Promise.reject(error)
);

// Auth endpoints
export const authAPI = {
  login: (username, password) =>
    api.post('/auth/token', new URLSearchParams({ username, password }).toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  register: (userData) => api.post('/auth/users/', userData),
  getCurrentUser: () => api.get('/auth/users/me'),
  updateAvatar: (avatar_url) => api.put('/auth/users/me/avatar', { avatar_url }),
};

// Cases endpoints
export const casesAPI = {
  getCases: () => api.get('/cases/'),
  getCaseById: (caseId) => api.get(`/cases/${caseId}`),
  getCasePreview: (caseId) => api.get(`/cases/preview/${caseId}`),
};

// Inventory endpoints
export const inventoryAPI = {
  getInventory: () => api.get('/inventory/'),
  addItem: (itemData) => api.post('/inventory/', itemData),
  removeItem: (inventoryId) => api.delete(`/inventory/${inventoryId}`),
  sellItem: (inventoryId) => api.post(`/inventory/${inventoryId}/sell`),
};

// Openings endpoints
export const openingsAPI = {
  openCase: (caseId) => api.post(`/openings/${caseId}`),
  openBatch: (caseId, count) => api.post(`/openings/${caseId}/batch?count=${count}`),
};

// Upgrades endpoints
export const upgradesAPI = {
  performUpgrade: (upgradeData) => api.post('/upgrades/', upgradeData),
};

// Daily rewards endpoints
export const dailyRewardsAPI = {
  getStatus: () => api.get('/daily-rewards/'),
  claimReward: () => api.post('/daily-rewards/claim'),
};

// Missions endpoints
export const missionsAPI = {
  getMissions: () => api.get('/missions/'),
  checkCaseOpening: () => api.post('/missions/check_case_opening'),
  checkUpgrade: () => api.post('/missions/check_upgrade'),
};

// Leaderboard endpoints
export const leaderboardAPI = {
  getLeaderboard: (limit = 50) => api.get(`/leaderboard/?limit=${limit}`),
};

// Admin endpoints
export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
  getUsers: () => api.get('/admin/users'),
  getActivity: () => api.get('/admin/activity'),
  adjustBalance: (userId, amount, mode = 'add') => api.post(`/admin/users/${userId}/balance`, { amount, mode }),
  setStatus: (userId, is_active) => api.post(`/admin/users/${userId}/status`, { is_active }),
  setAdmin: (userId, is_admin) => api.post(`/admin/users/${userId}/admin`, { is_admin }),
  repairCatalog: () => api.post('/admin/catalog/repair'),
};

// Dashboard endpoints
export const dashboardAPI = {
  getBalance: () => api.get('/balance'),
  getHistory: () => {
    const token = localStorage.getItem('token');

    return api.get('/history', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
};

export default api;
export const marketAPI = {
  getListings: (params={}) => api.get('/market/', { params }),
  createListing: (inventoryId, price) => api.post('/market/', { inventory_id: inventoryId, price }),
  buy: (listingId) => api.post(`/market/${listingId}/buy`),
  cancel: (listingId) => api.post(`/market/${listingId}/cancel`),
};

export const collectionsAPI = { getOverview: () => api.get('/collections/overview') };

export const progressionAPI = {
  getOverview: () => api.get('/progression/overview'),
  claimQuest: (questKey) => api.post(`/progression/quests/${questKey}/claim`),
  claimBattlePass: (level) => api.post(`/progression/battle-pass/${level}/claim`),
  prestige: () => api.post('/progression/prestige'),
};
