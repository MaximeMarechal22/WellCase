import React from 'react';
import CaseVisual from './CaseVisual';
import './CaseOpeningSplashFinal.css';

const themeFor = (name='') => {
  const n = String(name).toLowerCase();
  if (n.includes('rifle arsenal')) return { accent:'#9d3347', accent2:'#d95b70', label:'RIFLE ARSENAL', subtitle:'Arsenal de fusils d’assaut' };
  if (n.includes('knife arsenal') || n.includes('knives arsenal')) return { accent:'#9a7226', accent2:'#e4b454', label:'KNIFE ARSENAL', subtitle:'Arsenal de couteaux' };
  if (n.includes('gloves arsenal') || n.includes('glove arsenal')) return { accent:'#356f96', accent2:'#70afd3', label:'GLOVES ARSENAL', subtitle:'Arsenal de gants' };
  return { accent:'#4b556d', accent2:'#8fa0bd', label:String(name||'WELLCASE').toUpperCase(), subtitle:'Drop sécurisé' };
};

export default function CaseOpeningSplashFinal({ caseData }) {
  const theme = themeFor(caseData?.name);
  return (
    <div className="wc-final-splash" style={{'--final-accent':theme.accent,'--final-accent2':theme.accent2}} data-splash-version="46">
      <div className="wc-final-backdrop" />
      <div className="wc-final-panel">
        <div className="wc-final-brand">WELLCASE <span>DROP SECURITY</span></div>
        <div className="wc-final-kicker">OUVERTURE DE LA CAISSE</div>
        <h1>{theme.label}</h1>
        <p>{theme.subtitle}</p>
        <div className="wc-final-visual"><CaseVisual caseData={caseData} large splash /></div>
        <div className="wc-final-status"><span /> DROP SÉCURISÉ — RÉSULTAT DÉJÀ DÉTERMINÉ</div>
        <div className="wc-final-progress"><i /></div>
      </div>
    </div>
  );
}
