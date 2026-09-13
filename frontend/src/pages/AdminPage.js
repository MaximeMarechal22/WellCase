import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { adminAPI } from '../services/api';
import './AdminPage.css';
import ImageWithFallback from '../components/ImageWithFallback';

const money = n => `${Number(n || 0).toLocaleString('fr-FR', { maximumFractionDigits: 2 })} €`;

export default function AdminPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [activity, setActivity] = useState({ openings: [], upgrades: [] });
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(''); const [amounts,setAmounts]=useState({});

  const load = async () => {
    setLoading(true);
    try {
      const [a,b,c] = await Promise.all([adminAPI.getStats(), adminAPI.getUsers(), adminAPI.getActivity()]);
      setStats(a.data); setUsers(b.data); setActivity(c.data);
    } catch (e) {
      setToast(e?.response?.data?.detail || 'Accès administrateur requis.');
    } finally { setLoading(false); }
  };
  useEffect(() => { load(); }, []);

  const action = async (fn, message) => {
    try { await fn(); setToast(message); await load(); }
    catch(e) { setToast(e?.response?.data?.detail || 'Action impossible.'); }
  };

  if (user && !user.is_admin) return <div className="admin-denied"><div className="admin-denied-icon">✦</div><h2>Zone administrateur</h2><p>Ce panneau est réservé aux comptes administrateurs.</p></div>;
  const filtered = users.filter(u => `${u.username} ${u.email}`.toLowerCase().includes(query.toLowerCase()));

  return <div className="admin-page">
    <div className="admin-hero">
      <div><div className="admin-eyebrow">WELLCASE CONTROL CENTER</div><h1>Administration</h1><p>Supervise la plateforme, les joueurs et l'activité en temps réel.</p></div>
      <button className="admin-refresh" onClick={load}>↻ Actualiser</button>
    </div>
    {toast && <div className="inline-notice admin-inline-notice">{toast}<button onClick={()=>setToast('')}>×</button></div>}
    {loading && !stats ? <div className="admin-loading">Chargement du centre de contrôle…</div> : <>
      <div className="admin-stat-grid">
        {[['Joueurs',stats?.users,'◉'],['Ouvertures',stats?.openings,'▣'],['Upgrades',stats?.upgrades,'↗'],['Caisses',stats?.cases,'◇'],['Inventaire',stats?.inventory_items,'◈'],['Balance totale',money(stats?.total_virtual_balance),'€']].map(([label,value,icon])=><div className="admin-stat" key={label}><div className="admin-stat-icon">{icon}</div><span>{label}</span><strong>{value}</strong></div>)}
      </div>
      <div className="admin-grid">
        <section className="admin-panel admin-users">
          <div className="panel-head"><div><span className="panel-kicker">UTILISATEURS</span><h2>Gestion des joueurs</h2></div><input className="admin-search" placeholder="Rechercher…" value={query} onChange={e=>setQuery(e.target.value)}/></div>
          <div className="admin-table-wrap"><table><thead><tr><th>Joueur</th><th>Balance</th><th>Statut</th><th>Admin</th><th>Actions</th></tr></thead><tbody>
          {filtered.map(u=><tr key={u.id}><td><div className="admin-user"><ImageWithFallback className="admin-avatar" src={u.avatar_url} alt="" /><div><b>{u.username}</b><small>{u.email}</small></div></div></td><td className="admin-balance">{money(u.balance)}</td><td><span className={`status-pill ${u.is_active?'online':'off'}`}>{u.is_active?'ACTIF':'OFF'}</span></td><td>{u.is_admin?'✓':''}</td><td><div className="admin-actions">
          <input className="admin-amount-input" type="number" step="1" placeholder="€" value={amounts[u.id]||''} onChange={e=>setAmounts(x=>({...x,[u.id]:e.target.value}))}/><button onClick={()=>{const v=Number(amounts[u.id]);if(!v)return;action(()=>adminAPI.adjustBalance(u.id,v),'Balance mise à jour.');setAmounts(x=>({...x,[u.id]:''}))}}>OK</button>
          <button onClick={()=>action(()=>adminAPI.setStatus(u.id,!u.is_active),'Statut mis à jour.')}>{u.is_active?'Bloquer':'Activer'}</button>
          <button onClick={()=>action(()=>adminAPI.setAdmin(u.id,!u.is_admin),'Rôle mis à jour.')}>{u.is_admin?'Retirer admin':'Admin'}</button>
          </div></td></tr>)}
          </tbody></table></div>
        </section>
        <section className="admin-panel">
          <div className="panel-head"><div><span className="panel-kicker">LIVE FEED</span><h2>Dernières ouvertures</h2></div></div>
          <div className="activity-list">{activity.openings.map(o=><div className="activity-row" key={o.id}><span className="activity-dot"></span><div><b>Ouverture #{o.id}</b><small>User #{o.user_id} · Case #{o.case_id}</small></div><strong>DROP</strong></div>)}</div>
          <div className="panel-head activity-title"><div><span className="panel-kicker">UPGRADE</span><h2>Derniers essais</h2></div></div>
          <div className="activity-list">{activity.upgrades.map(o=><div className="activity-row" key={o.id}><span className={`activity-dot ${o.success?'success':'fail'}`}></span><div><b>Upgrade #{o.id}</b><small>User #{o.user_id} · {o.success?'Réussi':'Échec'}</small></div><strong>{o.success?'WIN':'LOSS'}</strong></div>)}</div>
        </section>
      </div>
    </>}
  </div>;
}
