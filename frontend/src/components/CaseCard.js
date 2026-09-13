import React from 'react';
import ImageWithFallback from './ImageWithFallback';
import { resolveCaseImage } from '../utils/caseAssets';
import CaseVisual from './CaseVisual';

const CaseCard = ({ case: caseData, onOpen, onPreview, onMultiOpen, balance = Infinity, open3Tokens = 0, open5Tokens = 0 }) => {
  const affordable = Number(balance) >= Number(caseData.price);
  const accent = caseData.color || '#ef3340';
  const itemCount = Array.isArray(caseData.items) ? caseData.items.length : null;
  const src = resolveCaseImage(caseData);

  return (
    <article className="case-card-premium case-card-previewable" style={{ '--case-accent': accent }} onClick={() => onPreview?.(caseData.id)} role="button" tabIndex={0} onKeyDown={(event) => { if (event.key === 'Enter' || event.key === ' ') onPreview?.(caseData.id); }}>
      <div className="case-card-glow" />
      <div className="case-image-container" onDoubleClick={(e)=>{e.stopPropagation(); onPreview?.(caseData.id);}}>
        <div className="case-card-badge">APERÇU</div>
        <ImageWithFallback src={src} alt={caseData.name} className="case-image img-fluid" />
      </div>
      <div className="case-card-content">
        <div className="case-card-meta"><span>CASE DROP</span>{itemCount !== null && <span>{itemCount} DROPS</span>}</div>
        <h3>{caseData.name}</h3>
        <p>{caseData.description || 'Des skins rares, des surprises et une chance de faire exploser ton inventaire.'}</p>
        <div className="case-card-footer">
          <div className="case-price"><span>PRIX</span><strong>{Number(caseData.price).toLocaleString('fr-FR')} €</strong></div>
          <div className="case-open-actions" aria-label="Actions de la caisse">
            <button className="case-open-btn" disabled={!affordable} onClick={(e) => { e.stopPropagation(); onOpen(caseData.id); }}><span>{affordable ? 'OUVRIR' : 'SOLDE INSUFFISANT'}</span><b>↗</b></button>
            {onMultiOpen && open3Tokens > 0 && Number(balance) >= Number(caseData.price) * 3 && <button className="case-multi-btn" onClick={(e) => { e.stopPropagation(); onMultiOpen(caseData.id, 3); }}>×3 <small>{open3Tokens}</small></button>}
            {onMultiOpen && open5Tokens > 0 && Number(balance) >= Number(caseData.price) * 5 && <button className="case-multi-btn hot" onClick={(e) => { e.stopPropagation(); onMultiOpen(caseData.id, 5); }}>×5 <small>{open5Tokens}</small></button>}
          </div>
        </div>
        
      </div>
    </article>
  );
};
export default CaseCard;
