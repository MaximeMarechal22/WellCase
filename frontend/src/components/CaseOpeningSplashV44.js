import React, { useMemo } from 'react';
import './CaseOpeningSplashV44.css';
import CaseVisual from './CaseVisual';

const themes = {
  rifle: { match: ['rifle arsenal', 'assault rifle arsenal'], label: 'RIFLE ARSENAL', subtitle: 'ARSENAL DE FUSILS D’ASSAUT', accent: '#a9273d', accent2: '#e06478', icon: 'AK' },
  knife: { match: ['knife arsenal', 'knives arsenal'], label: 'KNIFE ARSENAL', subtitle: 'ARSENAL DE COUTEAUX', accent: '#a97922', accent2: '#e4b95b', icon: '✦' },
  gloves: { match: ['gloves arsenal', 'glove arsenal'], label: 'GLOVES ARSENAL', subtitle: 'ARSENAL DE GANTS', accent: '#2d6488', accent2: '#6caacb', icon: '✋' },
};

function getTheme(name) {
  const key = String(name || '').trim().toLowerCase();
  for (const theme of Object.values(themes)) {
    if (theme.match.some((term) => key.includes(term))) return theme;
  }
  return { label: String(name || 'WELLCASE').toUpperCase(), subtitle: 'DROP SÉCURISÉ', accent: '#4a5270', accent2: '#8792b4', icon: 'W' };
}

export default function CaseOpeningSplashV44({ caseData }) {
  const theme = useMemo(() => getTheme(caseData?.name), [caseData?.name]);
  return (
    <div className="wc44-splash" style={{ '--wc44-accent': theme.accent, '--wc44-accent2': theme.accent2 }} data-splash-version="44" role="dialog" aria-label={`Ouverture ${caseData?.name || 'WellCase'}`}>
      <div className="wc44-bg" />
      <div className="wc44-grid" />
      <div className="wc44-content">
        <div className="wc44-brand"><span className="wc44-brand-mark">W</span><span>WELLCASE</span></div>
        <div className="wc44-kicker">OUVERTURE SÉCURISÉE</div>
        <h1>{theme.label}</h1>
        <p>{theme.subtitle}</p>
        <div className="wc44-stage"><CaseVisual caseData={caseData} large splash /></div>
        <div className="wc44-status"><span className="wc44-pulse" /> DROP SÉCURISÉ — LE SERVEUR A DÉJÀ TIRÉ TON SKIN</div>
        <div className="wc44-bar"><span /></div>
      </div>
    </div>
  );
}
