import React, { useMemo } from 'react';
import './CaseOpeningSplashV42.css';
import { resolveCaseImage } from '../utils/caseAssets';

const normalize = (value) => String(value || '').trim().toLowerCase();
const THEMES = {
  rifles: { match: ['rifle arsenal', 'assault rifle arsenal'], label: 'RIFLE ARSENAL', subtitle: 'Armes d’assaut sélectionnées', accent: '#8f2330', glow: 'rgba(143,35,48,.34)' },
  knives: { match: ['knife arsenal', 'knives arsenal'], label: 'KNIFE ARSENAL', subtitle: 'Couteaux et lames premium', accent: '#a06f22', glow: 'rgba(160,111,34,.34)' },
  gloves: { match: ['gloves arsenal', 'glove arsenal'], label: 'GLOVES ARSENAL', subtitle: 'Gants rares et premium', accent: '#2b5f7b', glow: 'rgba(43,95,123,.34)' },
};
function getTheme(name) { const key = normalize(name); for (const [tone, theme] of Object.entries(THEMES)) if (theme.match.some(term => key.includes(term))) return { tone, ...theme }; return { tone:'default', label:String(name || 'WELLCASE').toUpperCase(), subtitle:'Drop sécurisé côté serveur', accent:'#51456f', glow:'rgba(81,69,111,.30)' }; }
export default function CaseOpeningSplashV42({ caseData }) {
  const theme = useMemo(() => getTheme(caseData?.name), [caseData?.name]);
  const image = useMemo(() => resolveCaseImage(caseData || {}), [caseData]);
  const style = { '--accent': theme.accent, '--glow': theme.glow };
  return <div className={`wc42-splash wc42-${theme.tone}`} style={style} data-splash-version="42" role="dialog" aria-label={`Ouverture de ${caseData?.name || 'caisse'}`}>
    <div className="wc42-backdrop" />
    <div className="wc42-content">
      <div className="wc42-brand">WELLCASE</div>
      <div className="wc42-kicker">OUVERTURE DE LA CAISSE</div>
      <h1>{theme.label}</h1>
      <p className="wc42-subtitle">{theme.subtitle}</p>
      <div className="wc42-stage">
        <div className="wc42-orbit wc42-orbit-a" /><div className="wc42-orbit wc42-orbit-b" />
        <div className="wc42-card">{image ? <img src={image} alt={caseData?.name || theme.label} /> : <div className="wc42-card-fallback">W</div>}</div>
      </div>
      <div className="wc42-status"><span className="wc42-pulse" /><strong>DROP SÉCURISÉ</strong><span>Le résultat a déjà été déterminé.</span></div>
      <div className="wc42-progress"><span /></div>
    </div>
  </div>;
}
