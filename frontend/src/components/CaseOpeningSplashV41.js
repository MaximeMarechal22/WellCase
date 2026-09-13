import React, { useMemo } from 'react';
import './CaseOpeningSplashV41.css';

const normalize = (value) => String(value || '').trim().toLowerCase();

const getTheme = (name) => {
  const key = normalize(name);
  if (key.includes('gloves arsenal')) return {
    tone: 'gloves', title: 'GLOVES ARSENAL', subtitle: 'Collection exclusive · gants',
    accent: '#4b82a3', accent2: '#7aaac4', icon: '✦', glow: 'rgba(75,130,163,.24)'
  };
  if (key.includes('knife arsenal') || key.includes('knives arsenal')) return {
    tone: 'knives', title: 'KNIFE ARSENAL', subtitle: 'Collection exclusive · couteaux',
    accent: '#c4943f', accent2: '#e1bc6a', icon: '◆', glow: 'rgba(196,148,63,.24)'
  };
  if (key.includes('rifle arsenal') || key.includes('assault rifle arsenal')) return {
    tone: 'rifles', title: 'RIFLE ARSENAL', subtitle: 'Collection exclusive · fusils',
    accent: '#ba3d4a', accent2: '#e86a73', icon: '✦', glow: 'rgba(186,61,74,.24)'
  };
  if (key.includes('sniper arsenal')) return { tone: 'snipers', title: 'SNIPER ARSENAL', subtitle: 'Collection exclusive · snipers', accent: '#4e84b0', accent2: '#86b7dc', icon: '✦', glow: 'rgba(78,132,176,.24)' };
  if (key.includes('pistol arsenal')) return { tone: 'pistols', title: 'PISTOL ARSENAL', subtitle: 'Collection exclusive · pistolets', accent: '#b3863d', accent2: '#e0bf75', icon: '✦', glow: 'rgba(179,134,61,.24)' };
  return { tone: 'default', title: String(name || 'WELLCASE').toUpperCase(), subtitle: 'Drop sécurisé côté serveur', accent: '#725fbc', accent2: '#a08cdb', icon: '✦', glow: 'rgba(114,95,188,.22)' };
};

export default function CaseOpeningSplashV41({ caseData }) {
  const theme = useMemo(() => getTheme(caseData?.name), [caseData?.name]);
  return (
    <div
      className={`wc41-splash wc41-${theme.tone}`}
      style={{ '--accent': theme.accent, '--accent2': theme.accent2, '--glow': theme.glow }}
      data-splash-version="41"
      role="dialog"
      aria-label={`Ouverture de ${caseData?.name || 'caisse'}`}
    >
      <div className="wc41-stars" />
      <div className="wc41-vignette" />
      <div className="wc41-shell">
        <div className="wc41-brand">WELLCASE</div>
        <div className="wc41-kicker">OUVERTURE DE LA CAISSE</div>
        <h2>{theme.title}</h2>
        <p>{theme.subtitle} · résultat sécurisé</p>

        <div className="wc41-stage">
          <div className="wc41-light wc41-light-left" />
          <div className="wc41-light wc41-light-right" />
          <div className="wc41-crate-wrap" aria-hidden="true">
            <div className="wc41-crate-shadow" />
            <div className="wc41-crate-top" />
            <div className="wc41-crate-side wc41-crate-side-left" />
            <div className="wc41-crate-side wc41-crate-side-right" />
            <div className="wc41-crate-front">
              <div className="wc41-crate-badge">W</div>
              <div className="wc41-crate-title">{theme.title}</div>
              <div className="wc41-crate-lock"><span /></div>
            </div>
          </div>
          <div className="wc41-ring wc41-ring-a" />
          <div className="wc41-ring wc41-ring-b" />
        </div>

        <div className="wc41-status">
          <span className="wc41-status-dot" />
          <strong>DROP SÉCURISÉ</strong>
          <span>Le résultat est déjà déterminé côté serveur.</span>
        </div>
        <div className="wc41-progress"><span /></div>
        <div className="wc41-case-name">{caseData?.name || theme.title}</div>
      </div>
    </div>
  );
}
