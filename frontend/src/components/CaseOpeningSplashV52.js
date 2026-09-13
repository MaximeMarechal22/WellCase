import React from 'react';
import CaseVisual from './CaseVisual';
import './CaseOpeningSplashV52.css';

const toneFor = (name = '') => {
  const n = String(name).toLowerCase();
  if (n.includes('rifle arsenal')) return '#7f3142';
  if (n.includes('sniper arsenal')) return '#2e6688';
  if (n.includes('pistol arsenal')) return '#866226';
  if (n.includes('knife arsenal') || n.includes('knives arsenal') || n.includes('solid knife')) return '#8e6a2e';
  if (n.includes('gloves arsenal') || n.includes('glove arsenal')) return '#315f78';
  return '#556477';
};

export default function CaseOpeningSplashV52({ caseData }) {
  const accent = toneFor(caseData?.name);
  return (
    <div className="wc52-splash" data-splash-version="52" style={{ '--wc52-accent': accent }}>
      <div className="wc52-backdrop" />
      <div className="wc52-card">
        <div className="wc52-kicker">WELLCASE / OUVERTURE</div>
        <h1>{caseData?.name || 'WELLCASE'}</h1>
        <div className="wc52-stage"><CaseVisual caseData={caseData} large splash /></div>
        <div className="wc52-status"><i /> DROP SÉCURISÉ</div>
        <div className="wc52-progress"><span /></div>
      </div>
    </div>
  );
}
