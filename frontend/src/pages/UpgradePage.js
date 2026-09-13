import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api, { inventoryAPI, upgradesAPI, dashboardAPI } from '../services/api';
import ImageWithFallback from '../components/ImageWithFallback';
import './UpgradePage.css';
import { resolveItemImage } from '../utils/itemAssets';

const SPIN_MS = 5000;
const chanceFor = (source, target, upgradeLevel = 0, sourceEffectiveValue = null) => {
  if (!source || !target) return 0;
  const sourceValue = Number(sourceEffectiveValue ?? source.virtual_value);
  const base = Math.min(95, Math.max(1, sourceValue / Number(target.virtual_value) * 100));
  return Math.max(0.5, Math.min(95, base * Math.pow(0.85, Math.max(0, Number(upgradeLevel || 0)))));
};
const money = (v) => `${Number(v || 0).toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} €`;

const UpgradePage = () => {
  const { updateBalance } = useAuth();
  const [inventory, setInventory] = useState([]);
  const [allItems, setAllItems] = useState([]);
  const [sourceRowId, setSourceRowId] = useState(null);
  const [targetId, setTargetId] = useState(null);
  const [balance, setBalance] = useState(0);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [phase, setPhase] = useState('idle');
  const [result, setResult] = useState(null);
  const [arrowRotation, setArrowRotation] = useState(0);
  const [errorMessage, setErrorMessage] = useState('');
  const finishTimer = useRef(null);

  const refresh = async () => {
    const [inv, items, bal] = await Promise.all([inventoryAPI.getInventory(), api.get('/items/'), dashboardAPI.getBalance()]);
    setInventory(Array.isArray(inv.data) ? inv.data : []);
    setAllItems(Array.isArray(items.data) ? items.data : []);
    setBalance(Number(bal.data?.balance || 0));
  };
  useEffect(() => { refresh().catch(console.error).finally(() => setLoading(false)); return () => clearTimeout(finishTimer.current); }, []);

  const sourceRow = inventory.find((row) => row.id === sourceRowId) || null;
  const source = sourceRow?.item || null;
  const sourceEffectiveValue = Number(sourceRow?.effective_value || source?.virtual_value || 0);
  const targets = useMemo(() => source ? allItems.filter((item) => item.id !== source.id && item.is_active !== false && Number(item.virtual_value) > sourceEffectiveValue).sort((a,b) => Number(a.virtual_value)-Number(b.virtual_value)) : [], [allItems, source, sourceEffectiveValue]);
  const target = targets.find((item) => item.id === targetId) || null;
  const chance = chanceFor(source, target, sourceRow?.upgrade_level || 0, sourceEffectiveValue);
  const chanceHue = Math.max(0, Math.min(120, Number(chance || 0) * 1.2));
  const chanceColor = `hsl(${chanceHue} 88% 56%)`;
  const chanceGlow = `hsla(${chanceHue} 88% 56% / .22)`;

  const selectSource = (id) => { if (phase !== 'idle') return; setSourceRowId(id); setTargetId(null); setResult(null); };
  const selectTarget = (id) => { if (phase !== 'idle') return; setTargetId(id); setResult(null); };



  const runUpgrade = async () => {
    if (!source || !target || busy || phase !== 'idle') return;
    setBusy(true); setResult(null); setErrorMessage(''); setPhase('spinning'); setArrowRotation(0);
    try {
      // Server decides the result first. The wheel only reveals that server result.
      const response = await upgradesAPI.performUpgrade({ original_item_id: source.id, target_item_id: target.id, inventory_id: sourceRow?.id });
      const serverResult = response.data;
      // The server returns the exact landing angle corresponding to its result.
      // This prevents any visual contradiction between the green zone and SUCCESS/LOSS.
      const finalAngle = 360 * 5 + Number(serverResult.landing_angle || 0);
      requestAnimationFrame(() => setArrowRotation(finalAngle));
      finishTimer.current = window.setTimeout(async () => {
        setResult(serverResult); setPhase('result');
        try { await refresh(); await updateBalance(); } finally { setBusy(false); }
      }, SPIN_MS + 80);
    } catch (error) {
      setBusy(false); setPhase('idle');
      setErrorMessage(error.response?.data?.detail || "Impossible de lancer l’upgrade. Vérifie que tu possèdes encore la skin et que la cible est plus chère.");
      console.error(error);
    }
  };

  const reset = () => { clearTimeout(finishTimer.current); setPhase('idle'); setResult(null); setSourceRowId(null); setTargetId(null); setArrowRotation(0); setBusy(false); setErrorMessage(''); };

  if (loading) return <div className="upgrade-page container py-5"><div className="upgrade-loading"><div className="upgrade-spinner" /><span>Préparation de l’Upgrade…</span></div></div>;
  const resultSuccess = Boolean(result?.was_successful);
  const displayTarget = target || allItems.find((item) => item.id === result?.target_item_id);

  return <div className="upgrade-page container py-4">
    {errorMessage && <div className="upgrade-error-banner" role="alert"><span>{errorMessage}</span><button onClick={() => setErrorMessage('')} aria-label="Fermer">×</button></div>}
    <div className="upgrade-topbar"><div><span className="upgrade-kicker">WELLCASE / UPGRADE</span><h1>Upgrade</h1><p>Choisis une skin plus chère. La flèche va tenter d’atterrir dans la zone verte.</p></div><div className="upgrade-balance"><span>SOLDE</span><strong>{money(balance)}</strong></div></div>

    <section className={`upgrade-machine ${phase}`}>
      <div className="upgrade-item-card source-card"><span className="machine-label">VOTRE SKIN</span>{source ? <><div className="upgrade-art"><ImageWithFallback src={resolveItemImage(source)} alt={source.name} /></div><h3>{source.name}</h3><strong>{money(sourceEffectiveValue)}</strong></> : <div className="upgrade-placeholder">Sélectionne une skin<br/>dans ton inventaire</div>}</div>

      <div className="upgrade-wheel-zone">
        <div className="upgrade-chance-display" style={{ '--chance-color': chanceColor, '--chance-glow': chanceGlow }}>
          <span>CHANCE DE RÉUSSITE</span>
          <strong>{chance ? `${chance.toFixed(1)}%` : '—'}</strong>
          <small>{chance >= 70 ? 'Très favorable' : chance >= 40 ? 'Équilibré' : chance ? 'Risque élevé' : 'Choisis une cible'}</small>
        </div>
        <div className="upgrade-wheel-shell">
          <div className="wheel-glow" />
          <div className="upgrade-wheel" style={{ '--chance': `${chance}%`, '--chance-color': chanceColor, '--chance-glow': chanceGlow }}>
            <div className="wheel-ticks" />
            <div className="wheel-green-zone" />
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
      <section className="upgrade-selector-grid"><div className="selector-panel"><div className="selector-title"><span>01</span><div><b>Votre skin</b><small>{sourceRow?.upgrade_level ? `Niveau d'amélioration ${sourceRow.upgrade_level}` : 'Une skin que vous possédez'}</small></div></div><div className="skin-grid">{inventory.map((row) => <button key={row.id} className={sourceRowId === row.id ? 'active' : ''} onClick={() => selectSource(row.id)}><ImageWithFallback src={resolveItemImage(row.item)} alt="" /><div><b>{row.item?.name}</b><span>{money(row.item?.virtual_value)}</span></div>{row.quantity > 1 && <em>x{row.quantity}</em>}{row.upgrade_level > 0 && <em className="upgrade-level-pill">U{row.upgrade_level}</em>}</button>)}</div></div>
        <div className="selector-panel"><div className="selector-title"><span>02</span><div><b>Skin cible</b><small>{source ? `${targets.length} cibles plus chères` : 'Sélectionne une skin d’abord'}</small></div></div><div className="skin-grid">{targets.map((item) => <button key={item.id} className={targetId === item.id ? 'active' : ''} onClick={() => selectTarget(item.id)}><ImageWithFallback src={resolveItemImage(item)} alt="" /><div><b>{item.name}</b><span>{money(item.virtual_value)} · {chanceFor(source, item, sourceRow?.upgrade_level || 0, sourceEffectiveValue).toFixed(1)}%</span></div></button>)}</div></div></section>
      <button className="upgrade-main-btn" disabled={!source || !target || busy} onClick={runUpgrade}><span>LANCER L’UPGRADE</span><small>{target ? `${chance.toFixed(1)}% de chance d’atteindre la zone verte` : 'Choisis une cible plus chère'}</small></button>
    </>}

    {phase === 'spinning' && <div className="upgrade-live"><div className="live-dot" /><span>UPGRADE EN COURS</span><strong>La flèche tourne…</strong><small>Le serveur a déjà verrouillé le résultat.</small></div>}

    {phase === 'result' && result && <div className={`upgrade-result-card ${resultSuccess ? 'success' : 'failure'}`}><div className="result-burst">{resultSuccess ? '✓' : '×'}</div><span>{resultSuccess ? 'UPGRADE SUCCESS' : 'UPGRADE FAILED'}</span><h2>{resultSuccess ? `Tu as obtenu ${displayTarget?.name}` : 'La flèche est passée hors de la zone verte'}</h2><p>Chance au lancement : <b>{Number(result.success_chance).toFixed(1)}%</b></p>{resultSuccess && displayTarget && <div className="result-art"><ImageWithFallback src={resolveItemImage(displayTarget)} alt={displayTarget.name} /></div>}<button onClick={reset}>NOUVEL UPGRADE</button></div>}
  </div>;
};
export default UpgradePage;
