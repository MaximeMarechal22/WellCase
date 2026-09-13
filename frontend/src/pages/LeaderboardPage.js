import React, { useEffect, useState } from 'react';
import { leaderboardAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './LeaderboardPage.css';
import ImageWithFallback from '../components/ImageWithFallback';

const LeaderboardPage = () => {
  const { user } = useAuth();
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = async () => {
    try {
      setError('');
      const response = await leaderboardAPI.getLeaderboard(50);
      setRows(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      setError(err.response?.data?.detail || 'Impossible de charger le classement.');
    } finally { setLoading(false); }
  };
  useEffect(() => { load(); }, []);

  const top = rows.slice(0, 3);
  const medal = ['🥇', '🥈', '🥉'];

  if (loading) return <div className="leaderboard-page container py-5"><div className="leaderboard-loading"><div className="leaderboard-spinner" /><span>Chargement du classement…</span></div></div>;
  if (error) return <div className="leaderboard-page container py-5"><div className="leaderboard-error"><strong>Classement indisponible</strong><span>{error}</span><button onClick={load}>Réessayer</button></div></div>;

  return (
    <div className="leaderboard-page container py-4">
      <div className="leaderboard-head">
        <div><span className="leaderboard-kicker">WELLCASE / RANKING</span><h1>Classement général</h1><p>Monte dans le classement grâce à ton activité sur WellCase.</p></div>
        <div className="leaderboard-season"><span>SAISON</span><strong>ALL-TIME</strong></div>
      </div>

      <section className="podium">
        {[top[1], top[0], top[2]].filter(Boolean).map((row, index) => {
          const rank = row.rank;
          return <article key={row.userId} className={`podium-card rank-${rank} ${user?.id === row.userId ? 'me' : ''}`}>
            <div className="podium-medal">{medal[rank - 1]}</div><span className="podium-rank">#{rank}</span>
            <h2 style={{color: row.name_color || undefined}}>{row.username}</h2><strong>{row.xp.toLocaleString('fr-FR')} XP</strong><small>Niveau {row.level}</small>
            <div className="podium-stats"><span>{row.casesOpened} caisses</span><span>{row.upgrades} upgrades</span></div>
          </article>;
        })}
      </section>

      <section className="leaderboard-table">
        <div className="leaderboard-table-head"><span>RANG</span><span>JOUEUR</span><span>NIVEAU</span><span>ACTIVITÉ</span><span>XP</span></div>
        {rows.map((row) => <div className={`leaderboard-row ${user?.id === row.userId ? 'me' : ''}`} key={row.userId}>
          <b className="rank-number">#{row.rank}</b><div className="player-cell"><ImageWithFallback src={row.avatar_url} alt="" className="player-avatar" /><div><strong style={{color: row.name_color || undefined}}>{row.username}</strong>{user?.id === row.userId && <small>{user?.id===row.userId?'TOI':(row.cosmetic_badge||'')}</small>}</div></div>
          <span className="level-pill">LVL {row.level}{row.prestige_level>0?` · P${row.prestige_level}`:''}</span><span className="activity-cell">{row.casesOpened} caisses · {row.upgrades} upgrades</span><strong className="xp-cell">{row.xp.toLocaleString('fr-FR')} XP</strong>
        </div>)}
        {!rows.length && <div className="leaderboard-empty">Aucune activité pour le moment.</div>}
      </section>
    </div>
  );
};
export default LeaderboardPage;
