import React, { useMemo } from 'react';
import { resolveItemImage } from '../utils/itemAssets';
import ImageWithFallback from './ImageWithFallback';
import './CaseOpeningSplash.css';

const normalize = (value) => String(value || '').trim().toLowerCase();

const getTheme = (name) => {
  const key = normalize(name);
  if (key.includes('gloves arsenal')) return { tone: 'gloves', title: 'GLOVES ARSENAL', subtitle: 'Gants rares · Drop sécurisé', accent: '#4aa3c7', soft: 'rgba(74,163,199,.22)', icon: '✦' };
  if (key.includes('knife arsenal') || key.includes('knives arsenal')) return { tone: 'knives', title: 'KNIFE ARSENAL', subtitle: 'Couteaux rares · Drop sécurisé', accent: '#d3a03c', soft: 'rgba(211,160,60,.22)', icon: '✦' };
  if (key.includes('rifle arsenal') || key.includes('assault rifle arsenal')) return { tone: 'rifles', title: 'RIFLE ARSENAL', subtitle: 'Fusils d’assaut · Drop sécurisé', accent: '#d53e4d', soft: 'rgba(213,62,77,.22)', icon: '✦' };
  if (key.includes('sniper arsenal')) return { tone: 'snipers', title: 'SNIPER ARSENAL', subtitle: 'Fusils de précision · Drop sécurisé', accent: '#4e9ed1', soft: 'rgba(78,158,209,.22)', icon: '✦' };
  if (key.includes('pistol arsenal')) return { tone: 'pistols', title: 'PISTOL ARSENAL', subtitle: 'Pistolets · Drop sécurisé', accent: '#c99332', soft: 'rgba(201,147,50,.22)', icon: '✦' };
  return { tone: 'default', title: String(name || 'WELLCASE').toUpperCase(), subtitle: 'Drop sécurisé côté serveur', accent: '#8c6fe8', soft: 'rgba(140,111,232,.22)', icon: '✦' };
};

export default function CaseOpeningSplash({ caseData, rewards = [] }) {
  const theme = useMemo(() => getTheme(caseData?.name), [caseData?.name]);
  const featured = useMemo(() => {
    const list = Array.isArray(rewards) ? rewards.filter(Boolean) : [];
    const out = [];
    const seen = new Set();
    for (const item of list) {
      const key = item.id ?? item.name;
      if (seen.has(key)) continue;
      seen.add(key);
      out.push(item);
      if (out.length >= 2) break;
    }
    return out;
  }, [rewards]);

  return (
    <div className={`wc40-splash wc40-${theme.tone}`} style={{ '--accent': theme.accent, '--soft': theme.soft }} data-splash-version="40">
      <div className="wc40-noise" />
      <div className="wc40-panel">
        <div className="wc40-brand">WELLCASE</div>
        <div className="wc40-title-row"><span className="wc40-icon">{theme.icon}</span><span>{theme.title}</span></div>
        <div className="wc40-subtitle">{theme.subtitle}</div>

        <div className="wc40-stage">
          <div className="wc40-side-card wc40-side-left">
            {featured[0] ? <ImageWithFallback src={resolveItemImage(featured[0])} alt={featured[0].name} /> : <div className="wc40-side-fallback">DROP</div>}
            <div>{featured[0]?.name || 'ITEMS DE LA CAISSE'}</div>
          </div>

          <div className="wc40-crate-wrap">
            <div className="wc40-floor" />
            <div className="wc40-crate">
              <div className="wc40-crate-top" />
              <div className="wc40-crate-body">
                <div className="wc40-crate-logo">W</div>
                <div className="wc40-crate-label">{theme.title}</div>
                <div className="wc40-crate-lock"><span /></div>
              </div>
              <div className="wc40-crate-rib wc40-rib-1" />
              <div className="wc40-crate-rib wc40-rib-2" />
            </div>
          </div>

          <div className="wc40-side-card wc40-side-right">
            {featured[1] ? <ImageWithFallback src={resolveItemImage(featured[1])} alt={featured[1].name} /> : <div className="wc40-side-fallback">DROP</div>}
            <div>{featured[1]?.name || 'DROP SÉCURISÉ'}</div>
          </div>
        </div>

        <div className="wc40-footer">
          <strong>{caseData?.name || theme.title}</strong>
          <div className="wc40-progress"><span /></div>
          <small>RESULTAT VERROUILLÉ · OUVERTURE DE LA ROULETTE…</small>
        </div>
      </div>
    </div>
  );
}
