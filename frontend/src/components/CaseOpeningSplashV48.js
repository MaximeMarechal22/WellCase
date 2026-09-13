import React from 'react';
import CaseVisual from './CaseVisual';
import './CaseOpeningSplashV48.css';

const metaFor = (name = '') => {
  const n = String(name).toLowerCase();
  if (n.includes('rifle arsenal')) return { label: 'RIFLE ARSENAL', sub: 'FUSILS D’ASSAUT', accent: '#7f3142' };
  if (n.includes('sniper arsenal')) return { label: 'SNIPER ARSENAL', sub: 'SNIPERS & AWP', accent: '#2e6688' };
  if (n.includes('pistol arsenal')) return { label: 'PISTOL ARSENAL', sub: 'PISTOLETS', accent: '#866226' };
  if (n.includes('knife arsenal') || n.includes('knives arsenal')) return { label: 'KNIFE ARSENAL', sub: 'COUTEAUX', accent: '#8e6a2e' };
  if (n.includes('gloves arsenal') || n.includes('glove arsenal')) return { label: 'GLOVES ARSENAL', sub: 'GANTS', accent: '#315f78' };
  return { label: String(name || 'WELLCASE').toUpperCase(), sub: 'DROP SÉCURISÉ', accent: '#556477' };
};

export default function CaseOpeningSplashV48({ caseData }) {
  const meta = metaFor(caseData?.name);
  return (
    <div className="wc48-splash" data-splash-version="48" style={{ '--wc48-accent': meta.accent }}>
      <div className="wc48-backdrop" />
      <div className="wc48-card">
        <div className="wc48-kicker">WELLCASE / OUVERTURE</div>
        <h1>{meta.label}</h1>
        <p>{meta.sub}</p>
        <div className="wc48-case-stage">
          <CaseVisual caseData={caseData} large splash />
        </div>
        <div className="wc48-status"><span /> DROP SÉCURISÉ</div>
        <div className="wc48-progress"><i /></div>
      </div>
    </div>
  );
}
