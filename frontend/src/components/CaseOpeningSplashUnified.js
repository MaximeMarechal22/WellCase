import React from 'react';
import CaseVisual from './CaseVisual';
import ImageWithFallback from './ImageWithFallback';
import { resolveCaseImage } from '../utils/caseAssets';
import './CaseOpeningSplashUnified.css';

export default function CaseOpeningSplashUnified({ caseData }) {
  const accent = caseData?.color || '#58697a';
  return (
    <div
      className="wc61-splash"
      style={{ '--wc61-accent': accent }}
      data-splash-version="67-no-arsenal"
      role="dialog"
      aria-label={`Ouverture de ${caseData?.name || 'caisse'}`}
    >
      <div className="wc61-backdrop" />
      <div className="wc61-card">
        <div className="wc61-kicker">WELLCASE / OUVERTURE SÉCURISÉE</div>
        <h1>{caseData?.name || 'WELLCASE'}</h1>
        <div className="wc61-stage">
          {resolveCaseImage(caseData) ? (
            <div className="wc61-case-art">
              <ImageWithFallback src={resolveCaseImage(caseData)} alt={caseData?.name || 'WELLCASE'} className="wc61-case-art-image" />
            </div>
          ) : (
            <CaseVisual caseData={caseData} large splash />
          )}
        </div>
        <div className="wc61-status"><span />DROP SÉCURISÉ</div>
        <div className="wc61-progress"><i /></div>
      </div>
    </div>
  );
}
