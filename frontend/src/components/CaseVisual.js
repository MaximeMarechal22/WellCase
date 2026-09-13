import React from 'react';
import './CaseVisual.css';

const normalize = (name = '') => String(name)
  .toLowerCase()
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '')
  .replace(/[^a-z0-9]/g, '');

export default function CaseVisual({ caseData, large = false, splash = false }) {
  const name = caseData?.name || 'WELLCASE CASE';
  const cleanName = normalize(name).replace(/case$/,'');
  const title = String(name).replace(/\s*case\s*$/i, '').toUpperCase() || 'WELLCASE';
  const initials = cleanName.slice(0, 3).toUpperCase() || 'WC';
  return (
    <div
      data-case-visual={title}
      className={`case-visual ${large ? 'case-visual-large' : ''} ${splash ? 'case-visual-splash' : ''}`}
      style={{ '--cv-accent': caseData?.color || '#556477', '--cv-accent2': '#94aac4', '--cv-glow': `${caseData?.color || '#94aac4'}55` }}
    >
      <div className="cv-stars" />
      <div className="cv-halo" />
      <div className="cv-floor" />
      <div className="cv-crate">
        <div className="cv-lid" />
        <div className="cv-body">
          <div className="cv-corner cv-corner-tl" /><div className="cv-corner cv-corner-tr" />
          <div className="cv-corner cv-corner-bl" /><div className="cv-corner cv-corner-br" />
          <div className="cv-panel"><b>{initials}</b><span>WELLCASE</span><em>{title}</em></div>
          <div className="cv-lock cv-lock-left" /><div className="cv-lock cv-lock-right" />
        </div>
      </div>
      <div className="cv-caption">{title}</div>
    </div>
  );
}
