import React, { useEffect, useMemo, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { dashboardAPI } from '../services/api';
import ImageWithFallback from '../components/ImageWithFallback';
import './HistoryPage.css';

const HistoryPage = () => {
  const { balance } = useAuth();
  const [history, setHistory] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadHistory = async () => {
    try {
      setError('');
      const response = await dashboardAPI.getHistory();
      setHistory(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      console.error('History error:', err);
      setError(err.response?.data?.detail || 'Impossible de charger l’historique.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadHistory(); }, []);

  const filteredHistory = useMemo(() => (
    filter === 'all' ? history : history.filter((entry) => entry.type === filter)
  ), [history, filter]);

  const formatDate = (value) => value ? new Date(value).toLocaleString('fr-FR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }) : '—';
  const formatMoney = (value) => value == null ? '—' : `${Number(value).toLocaleString('fr-FR', { maximumFractionDigits: 0 })} €`;

  if (loading) return <div className="history-page container py-5"><div className="history-loading"><div className="history-spinner" /><span>Chargement de l’activité…</span></div></div>;

  return (
    <div className="history-page container py-4">
      <div className="history-head">
        <div>
          <span className="history-kicker">WELLCASE ACTIVITY</span>
          <h1>Historique</h1>
          <p>Toutes tes ouvertures, améliorations et récompenses au même endroit.</p>
        </div>
        <div className="history-balance"><span>SOLDE ACTUEL</span><strong>{formatMoney(balance)}</strong></div>
      </div>

      <div className="history-tabs">
        {[['all','Tout'],['opening','Ouvertures'],['upgrade','Upgrades'],['reward','Récompenses']].map(([value,label]) => (
          <button key={value} className={filter === value ? 'active' : ''} onClick={() => setFilter(value)}>{label}</button>
        ))}
      </div>

      {error && <div className="history-error"><strong>Historique indisponible</strong><span>{error}</span><button onClick={loadHistory}>Réessayer</button></div>}

      {!error && <div className="history-list">
        {filteredHistory.length === 0 && <div className="history-empty"><span>◌</span><h3>Aucune activité</h3><p>Ton activité apparaîtra ici dès ta première ouverture ou amélioration.</p></div>}
        {filteredHistory.map((entry) => {
          const isOpening = entry.type === 'opening';
          const isUpgrade = entry.type === 'upgrade';
          const success = entry.wasSuccessful;
          const image = isOpening ? entry.itemImageUrl : isUpgrade ? (success ? entry.targetImageUrl : entry.originalImageUrl) : null;
          return (
            <article className={`history-entry ${entry.type} ${isUpgrade ? (success ? 'success' : 'failed') : ''}`} key={entry.id}>
              <div className="history-entry-icon">{isOpening ? '▣' : isUpgrade ? '↗' : '★'}</div>
              <div className="history-entry-main">
                <div className="history-entry-top"><span>{formatDate(entry.timestamp)}</span><b>{isOpening ? 'OUVERTURE' : isUpgrade ? 'UPGRADE' : 'RÉCOMPENSE'}</b></div>
                {isOpening && <><h3>{entry.itemName}</h3><p>{entry.caseName} · {entry.itemRarity || 'Skin'} · {formatMoney(entry.itemValue)}</p></>}
                {isUpgrade && <><h3>{success ? `→ ${entry.targetName}` : `× ${entry.originalName}`}</h3><p>{success ? 'Upgrade réussi' : 'Upgrade échoué'} · {Number(entry.successChance).toFixed(1)}% de chance</p></>}
                {!isOpening && !isUpgrade && <><h3>Récompense quotidienne</h3><p>Jour {entry.dayStreak} · +{formatMoney(entry.rewardAmount)}</p></>}
              </div>
              {image && <div className="history-entry-image"><ImageWithFallback src={image} alt="" /></div>}
              <div className="history-entry-value">
                {isUpgrade && <span className={success ? 'value-success' : 'value-fail'}>{success ? 'SUCCÈS' : 'ÉCHEC'}</span>}
                {isOpening && <span>{formatMoney(entry.itemValue)}</span>}
                {!isUpgrade && !isOpening && <span className="value-success">+{formatMoney(entry.rewardAmount)}</span>}
                <small>{entry.balanceBefore == null ? 'Solde —' : `${formatMoney(entry.balanceBefore)} → ${formatMoney(entry.balanceAfter)}`}</small>
              </div>
            </article>
          );
        })}
      </div>}
    </div>
  );
};

export default HistoryPage;
