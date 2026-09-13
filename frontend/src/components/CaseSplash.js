import React, { useMemo } from 'react';
import ImageWithFallback from './ImageWithFallback';
import { resolveCaseImage } from '../utils/caseAssets';
import { resolveItemImage } from '../utils/itemAssets';
import './CaseSplash.css';

const normalize = (value) => String(value || '').trim().toLowerCase();

const getTheme = (name) => {
  const key = normalize(name);
  if (key.includes('gloves')) return { tone: 'gloves', label: 'GLOVES ARSENAL', subtitle: 'Arsenal de gants rares', glow: '#3b82f6' };
  if (key.includes('knife') || key.includes('knives')) return { tone: 'knives', label: 'KNIFE ARSENAL', subtitle: 'Arsenal de couteaux', glow: '#d59a32' };
  if (key.includes('rifle') || key.includes('assault')) return { tone: 'rifles', label: 'RIFLE ARSENAL', subtitle: 'Arsenal de fusils d’assaut', glow: '#ef3340' };
  if (key.includes('sniper')) return { tone: 'snipers', label: 'SNIPER ARSENAL', subtitle: 'Arsenal de fusils de précision', glow: '#38bdf8' };
  if (key.includes('pistol')) return { tone: 'pistols', label: 'PISTOL ARSENAL', subtitle: 'Arsenal de pistolets', glow: '#f59e0b' };
  return { tone: 'default', label: String(name || 'WELLCASE CASE').toUpperCase(), subtitle: 'Résultat sécurisé côté serveur', glow: '#8b5cf6' };
};

const CaseSplash = ({ caseData, rewards = [] }) => {
  const theme = useMemo(() => getTheme(caseData?.name), [caseData?.name]);
  const representative = useMemo(() => {
    const pool = Array.isArray(rewards) ? rewards.filter(Boolean) : [];
    const unique = [];
    const seen = new Set();
    for (const item of pool) {
      const key = item.id ?? item.name;
      if (seen.has(key)) continue;
      seen.add(key);
      unique.push(item);
      if (unique.length >= 2) break;
    }
    return unique;
  }, [rewards]);

  const caseImage = useMemo(() => {
    if (!caseData) return '';
    const name = normalize(caseData.name);
    if (name.includes('arsenal')) return '';
    return resolveCaseImage(caseData);
  }, [caseData]);

  return (
    <div className={`wc-splash-overlay wc-splash-${theme.tone}`} style={{ '--splash-glow': theme.glow }}>
      <div className="wc-splash-card">
        <div className="wc-splash-grid" aria-hidden="true" />
        <div className="wc-splash-brand">WELLCASE</div>
        <div className="wc-splash-title">DROP SÉCURISÉ</div>
        <div className="wc-splash-subtitle">{theme.subtitle}</div>

        <div className="wc-splash-stage">
          {representative[0] && (
            <div className="wc-splash-item wc-splash-item-left">
              <ImageWithFallback src={resolveItemImage(representative[0])} alt={representative[0].name} />
              <span>{representative[0].name}</span>
            </div>
          )}

          <div className="wc-splash-case-shell">
            <div className="wc-splash-case-top" />
            <div className="wc-splash-case-body">
              {caseImage ? (
                <ImageWithFallback src={caseImage} alt="" className="wc-splash-case-image" />
              ) : (
                <div className="wc-splash-case-mark">W</div>
              )}
              <div className="wc-splash-case-lock" />
            </div>
            <div className="wc-splash-case-base" />
          </div>

          {representative[1] && (
            <div className="wc-splash-item wc-splash-item-right">
              <ImageWithFallback src={resolveItemImage(representative[1])} alt={representative[1].name} />
              <span>{representative[1].name}</span>
            </div>
          )}
        </div>

        <div className="wc-splash-case-name">{caseData?.name || theme.label}</div>
        <div className="wc-splash-progress"><span /></div>
        <div className="wc-splash-status">RÉSULTAT VERROUILLÉ · OUVERTURE DE LA ROULETTE…</div>
      </div>
    </div>
  );
};

export default CaseSplash;
