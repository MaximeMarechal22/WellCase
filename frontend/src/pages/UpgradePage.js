import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api, { inventoryAPI, upgradesAPI, dashboardAPI } from '../services/api';
import ImageWithFallback from '../components/ImageWithFallback';
import './UpgradePage.css';
import { resolveItemImage } from '../utils/itemAssets';

const SPIN_MS = 5000;
const chanceFor = (source, target) => source && target ? Math.min(95, Math.max(1, Number(source.virtual_value) / Number(target.virtual_value) * 100)) : 0;
const money = (v) => `${Number(v || 0).toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} €`;

const UpgradePage = () => {
  const { updateBalance } = useAuth();
  const [inventory, setInventory] = useState([]);
  const [allItems, setAllItems] = useState([]);
  const [sourceId, setSourceId] = useState(null);
  const [targetId, setTargetId] = useState(null);
  const [balance, setBalance] = useState(0);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [phase, setPhase] = useState('idle');
  const [result, setResult] = useState(null);
  const [arrowRotation, setArrowRotation] = useState(0);
  const finishTimer = useRef(null);

  const refresh = async () => {
    const [inv, items, bal] = await Promise.all([inventoryAPI.getInventory(), api.get('/items/'), dashboardAPI.getBalance()]);
    setInventory(Array.isArray(inv.data) ? inv.data : []);
    setAllItems(Array.isArray(items.data) ? items.data : []);
    setBalance(Number(bal.data?.balance || 0));
  };
  useEffect(() => { refresh().catch(console.error).finally(() => setLoading(false)); return () => clearTimeout(finishTimer.current); }, []);

  const source = inventory.find((row) => row.item_id === sourceId)?.item || null;
  const targets = useMemo(() => source ? allItems.filter((item) => item.id !== source.id && item.is_active !== false && Number(item.virtual_value) > Number(source.virtual_value)).sort((a,b) => Number(a.virtual_value)-Number(b.virtual_value)) : [], [allItems, source]);
  const target = targets.find((item) => item.id === targetId) || null;
  const chance = chanceFor(source, target);

  const selectSource = (id) => { if (phase !== 'idle') return; setSourceId(id); setTargetId(null); setResult(null); };
  const selectTarget = (id) => { if (phase !== 'idle') return; setTargetId(id); setResult(null); };

  const chooseLandingAngle = (success, probability) => {
    const green = probability * 3.6;
    if (success) return 360 * 5 + 8 + Math.random() * Math.max(4, green - 16);
    const safeStart = Math.min(350, green + 10);
    const safeWidth = Math.max(8, 350 - safeStart);
    return 360 * 5 + safeStart + Math.random() * safeWidth;
  };

  const runUpgrade = async () => {
    if (!source || !target || busy || phase !== 'idle') return;
    setBusy(true); setResult(null); setPhase('spinning'); setArrowRotation(0);
    try {
      // Server decides the result first. The wheel only reveals that server result.
      const response = await upgradesAPI.performUpgrade({ original_item_id: source.id, target_item_id: target.id });
      const serverResult = response.data;
      const finalAngle = chooseLandingAngle(Boolean(serverResult.was_successful), Number(serverResult.success_chance || chance));
      // Force a fresh transition even when two attempts use the same angle bucket.
      requestAnimationFrame(() => setArrowRotation(finalAngle));
      finishTimer.current = window.setTimeout(async () => {
        setResult(serverResult); setPhase('result');
        try { await refresh(); await updateBalance(); } finally { setBusy(false); }
      }, SPIN_MS + 80);
    } catch (error) {
      setBusy(false); setPhase('idle'); console.error(error);
    }
  };

  const reset = () => { clearTimeout(finishTimer.current); setPhase('idle'); setResult(null); setSourceId(null); setTargetId(null); setArrowRotation(0); setBusy(false); };

  if (loading) return <div className="upgrade-page container py-5"><div className="upgrade-loading"><div className="upgrade-spinner" /><span>Préparation de l’Upgrade…</span></div></div>;
  const resultSuccess = Boolean(result?.was_successful);
  const displayTarget = target || allItems.find((item) => item.id === result?.target_item_id);

  return <div className="upgrade-page container py-4">
    <div className="upgrade-topbar"><div><span className="upgrade-kicker">WELLCASE / UPGRADE</span><h1>Upgrade</h1><p>Choisis une skin plus chère. La flèche va tenter d’atterrir dans la zone verte.</p></div><div className="upgrade-balance"><span>SOLDE</span><strong>{money(balance)}</strong></div></div>

    <section className={`upgrade-machine ${phase}`}>
      <div className="upgrade-item-card source-card"><span className="machine-label">VOTRE SKIN</span>{source ? <><div className="upgrade-art"><ImageWithFallback src={resolveItemImage(source)} alt={source.name} /></div><h3>{source.name}</h3><strong>{money(source.virtual_value)}</strong></> : <div className="upgrade-placeholder">Sélectionne une skin<br/>dans ton inventaire</div>}</div>

      <div className="upgrade-wheel-zone">
        <div className="upgrade-wheel-shell">
          <div className="wheel-glow" />
          <div className="upgrade-wheel" style={{ '--chance': `${chance}%` }}>
            <div className="wheel-ticks" />
            <div className="wheel-green-zone" />
            <div className="wheel-center"><strong>{chance ? `${chance.toFixed(1)}%` : '—'}</strong><span>CHANCE</span><small>D’AMÉLIORATION</small></div>
            <div className="wheel-arrow" style={{ transform: `translateX(-50%) rotate(${arrowRotation}deg)` }}><span /></div>
          </div>
          <div className="wheel-hub"><span /></div>
          <div className="wheel-fixed-pointer"><span /></div>
        </div>
        <div className="wheel-caption">{phase === 'spinning' ? 'LA FLÈCHE TOURNE…' : phase === 'result' ? (resultSuccess ? 'ZONE VERTE ATTEINTE' : 'HORS DE LA ZONE VERTE') : 'LA ZONE VERTE = TA CHANCE'}</div>
      </div>

      <div className="upgrade-item-card target-card"><span className="machine-label">CIBLE</span>{target ? <><div className="upgrade-art"><ImageWithFallback src={resolveItemImage(target)} alt={target.name} /></div><h3>{target.name}</h3><strong>{money(target.virtual_value)}</strong><small>{chance.toFixed(1)}% de réussite</small></> : <div className="upgrade-placeholder">Choisis une cible<br/>plus chère</div>}</div>
    </section>

    {phase === 'idle' && <>
      <section className="upgrade-selector-grid"><div className="selector-panel"><div className="selector-title"><span>01</span><div><b>Votre skin</b><small>Une skin que vous possédez</small></div></div><div className="skin-grid">{inventory.map((row) => <button key={row.id} className={sourceId === row.item_id ? 'active' : ''} onClick={() => selectSource(row.item_id)}><ImageWithFallback src={resolveItemImage(row.item)} alt="" /><div><b>{row.item?.name}</b><span>{money(row.item?.virtual_value)}</span></div>{row.quantity > 1 && <em>x{row.quantity}</em>}</button>)}</div></div>
        <div className="selector-panel"><div className="selector-title"><span>02</span><div><b>Skin cible</b><small>{source ? `${targets.length} cibles plus chères` : 'Sélectionne une skin d’abord'}</small></div></div><div className="skin-grid">{targets.map((item) => <button key={item.id} className={targetId === item.id ? 'active' : ''} onClick={() => selectTarget(item.id)}><ImageWithFallback src={resolveItemImage(item)} alt="" /><div><b>{item.name}</b><span>{money(item.virtual_value)} · {chanceFor(source, item).toFixed(1)}%</span></div></button>)}</div></div></section>
      <button className="upgrade-main-btn" disabled={!source || !target || busy} onClick={runUpgrade}><span>LANCER L’UPGRADE</span><small>{target ? `${chance.toFixed(1)}% de chance d’atteindre la zone verte` : 'Choisis une cible plus chère'}</small></button>
    </>}

    {phase === 'spinning' && <div className="upgrade-live"><div className="live-dot" /><span>UPGRADE EN COURS</span><strong>La flèche tourne…</strong><small>Le serveur a déjà verrouillé le résultat.</small></div>}

    {phase === 'result' && result && <div className={`upgrade-result-card ${resultSuccess ? 'success' : 'failure'}`}><div className="result-burst">{resultSuccess ? '✓' : '×'}</div><span>{resultSuccess ? 'UPGRADE SUCCESS' : 'UPGRADE FAILED'}</span><h2>{resultSuccess ? `Tu as obtenu ${displayTarget?.name}` : 'La flèche est passée hors de la zone verte'}</h2><p>Chance au lancement : <b>{Number(result.success_chance).toFixed(1)}%</b></p>{resultSuccess && displayTarget && <div className="result-art"><ImageWithFallback src={displayTarget.image_url} alt={displayTarget.name} /></div>}<button onClick={reset}>NOUVEL UPGRADE</button></div>}
  </div>;
};
export default UpgradePage;
