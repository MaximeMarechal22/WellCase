import React, { useEffect, useMemo, useRef, useState } from 'react';
import ImageWithFallback from './ImageWithFallback';
import './CaseOpeningAnimation.css';
import { playOpeningStart, playOpeningTick, playOpeningWin } from '../utils/sounds';
import { resolveItemImage } from '../utils/itemAssets';

const SLOT_WIDTH = 164;
const WINNER_INDEX = 44;
const TOTAL_SLOTS = 70;
const ANIMATION_MS = 6800;

const money = (value) => `${Number(value || 0).toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} €`;

const normalizeImage = (url) => {
  if (!url) return '';
  const value = String(url).trim();
  if (/^https?:\/\//i.test(value) || value.startsWith('data:')) return value;
  return `/${value.replace(/^\/+/, '')}`;
};

const CaseOpeningAnimation = ({ caseId, openingResult, onComplete, onClose }) => {
  const [phase, setPhase] = useState('rolling');
  const [translateX, setTranslateX] = useState(0);
  const viewportRef = useRef(null);
  const completedRef = useRef(false);
  const onCompleteRef = useRef(onComplete);

  useEffect(() => { onCompleteRef.current = onComplete; }, [onComplete]);

  useEffect(() => {
    const previousOverflow = document.body.style.overflow;
    const previousPaddingRight = document.body.style.paddingRight;
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    document.body.style.overflow = 'hidden';
    if (scrollbarWidth > 0) document.body.style.paddingRight = `${scrollbarWidth}px`;
    return () => {
      document.body.style.overflow = previousOverflow;
      document.body.style.paddingRight = previousPaddingRight;
    };
  }, []);

  const result = openingResult;
  const wonItem = result?.item ? {
    ...result.item,
    image_url: resolveItemImage(result.item),
  } : null;

  const caseData = result ? {
    id: result.case_id || caseId,
    name: result.case_name || `Case #${result.case_id || caseId}`,
    price: Number(result.case_price || 0),
  } : null;

  const sequence = useMemo(() => {
    if (!wonItem) return [];

    // Build a real roulette from the rewards of the opened case instead of
    // cloning the winning item into every slot. This makes every opening
    // visually different while the server result remains authoritative.
    const rewards = Array.isArray(result?.rewards) && result.rewards.length
      ? result.rewards.map((item) => ({ ...item, image_url: resolveItemImage(item) }))
      : [wonItem];

    const shuffled = [...rewards].sort(() => Math.random() - 0.5);
    const slots = [];
    for (let index = 0; index < TOTAL_SLOTS; index += 1) {
      // Cycle through a shuffled reward pool so adjacent slots aren't always
      // the same weapon, even for a small case.
      slots.push({ ...shuffled[index % shuffled.length] });
    }

    slots[WINNER_INDEX] = { ...wonItem };
    return slots;
  }, [result?.id, result?.rewards, wonItem?.id, wonItem?.image_url, wonItem?.name]);

  useEffect(() => {
    if (!wonItem || !sequence.length) return undefined;
    const viewportWidth = viewportRef.current?.clientWidth || Math.min(window.innerWidth - 36, 1180);
    const winnerCenter = WINNER_INDEX * SLOT_WIDTH + SLOT_WIDTH / 2;
    const target = Math.round((viewportWidth / 2) - winnerCenter);

    playOpeningStart();
    let tickIndex = 0;
    const tickTimer = window.setInterval(() => {
      playOpeningTick(tickIndex++);
    }, 520);

    const frame = window.requestAnimationFrame(() => setTranslateX(target));
    const finishTimer = window.setTimeout(() => {
      window.clearInterval(tickTimer);
      playOpeningWin();
      setPhase('finished');
      if (!completedRef.current) {
        completedRef.current = true;
        onCompleteRef.current?.(wonItem);
      }
    }, ANIMATION_MS + 140);
    return () => {
      window.cancelAnimationFrame(frame);
      window.clearTimeout(finishTimer);
      window.clearInterval(tickTimer);
    };
  }, [!!wonItem, sequence.length]);

  if (!result || !wonItem || !caseData) {
    return (
      <div className="opening-animation-container opening-state">
        <div className="opening-loader" />
        <span className="opening-kicker">WELLCASE DROP</span>
        <strong>Préparation du drop…</strong>
        <small>Résultat serveur en attente.</small>
      </div>
    );
  }

  const isFinished = phase === 'finished';
  const casePrice = Number(result.case_price ?? caseData.price ?? 0);
  const itemValue = Number(result.item_value ?? wonItem.virtual_value ?? 0);
  const netGain = Number(result.net_gain ?? (itemValue - casePrice));
  const rarityClass = (rarity) => rarity ? `rarity-${rarity.toLowerCase().replace(/\s+/g, '-')}` : 'rarity-default';

  return (
    <div className={`opening-animation-container ${phase}`}>
      <div className="opening-backdrop-orb orb-a" /><div className="opening-backdrop-orb orb-b" />
      <div className="opening-header">
        <span className="opening-kicker">WELLCASE / OPENING</span>
        <h3>{caseData.name}</h3>
        <p>La roue ralentit jusqu’au drop exact.</p>
      </div>

      <div className="opening-viewport" ref={viewportRef}>
        <div className="opening-viewport-vignette" />
        <div className="opening-pointer" aria-hidden="true"><span /></div>
        <div className="opening-track" style={{ width: `${sequence.length * SLOT_WIDTH}px`, transform: `translate3d(${translateX}px,0,0)` }}>
          {sequence.map((item, index) => (
            <div className="opening-slide-item" key={`${item.id}-${index}`} style={{ width: SLOT_WIDTH }}>
              <div className="opening-item-card">
                <div className="opening-item-rarity-line" />
                <ImageWithFallback src={resolveItemImage(item)} alt={item.name} className="opening-item-image" />
                <div className="item-name" title={item.name}>{item.name}</div>
                <div className={`item-rarity ${rarityClass(item.rarity)}`}>{item.rarity}</div>
                {Number.isFinite(Number(item.probability)) && <small className="opening-item-probability">{Number(item.probability).toFixed(2)}% chance</small>}
                <small className="opening-item-value">{money(item.virtual_value)}</small>
              </div>
            </div>
          ))}
        </div>
      </div>

      {!isFinished && <div className="opening-status opening-status-clean"><span className="status-label">OUVERTURE EN COURS</span><strong>La roue révèle ton drop…</strong></div>}

      {isFinished && (
        <div className="opening-result-panel">
          <div className="opening-result-main">
            <div className="won-item-glow"><div className="won-item-rays" /><ImageWithFallback src={resolveItemImage(wonItem)} alt={wonItem.name} className="won-item-image" /></div>
            <div className="won-item-copy"><span className="status-label win">DROP CONFIRMÉ</span><div className="won-item-name">{wonItem.name}</div>{openingResult?.condition && <div className="opening-condition">{openingResult.condition}</div>}<div className={`won-item-rarity ${rarityClass(wonItem.rarity)}`}>{wonItem.rarity}</div></div>
          </div>
          <div className="opening-earnings">
            <div><span>PRIX DE LA CAISSE</span><strong>- {money(casePrice)}</strong></div>
            <div><span>VALEUR DU DROP</span><strong>{money(itemValue)}</strong></div>
            <div className={netGain >= 0 ? 'positive' : 'negative'}><span>GAIN NET</span><strong>{netGain >= 0 ? '+' : ''}{money(netGain)}</strong></div>
          </div>
          <div className="opening-secured-line">✓ DROP AJOUTÉ À L’INVENTAIRE · PATRIMOINE APRÈS DROP : <b>{money(result.total_wealth_after)}</b></div>
          <button className="opening-collect-button" onClick={onClose}>RÉCUPÉRER LE SKIN</button>
        </div>
      )}
    </div>
  );
};

export default CaseOpeningAnimation;
