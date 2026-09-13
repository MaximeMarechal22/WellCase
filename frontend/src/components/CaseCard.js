import React from 'react';
import ImageWithFallback from './ImageWithFallback';
import neonCase from '../assets/cases/neon.png';
import knifeCase from '../assets/cases/knife.png';
import covertCase from '../assets/cases/covert.png';
import supremeCase from '../assets/cases/supreme.png';

const LOCAL_CASE_IMAGES = {
  'Neon Case': neonCase,
  'Knife Case': knifeCase,
  'Covert Case': covertCase,
  'Supreme Case': supremeCase,
};

const CaseCard = ({ case: caseData, onOpen, onMultiOpen, balance = Infinity, open3Tokens = 0, open5Tokens = 0 }) => {
  const affordable = Number(balance) >= Number(caseData.price);
  const accent = caseData.color || '#ef3340';
  const itemCount = Array.isArray(caseData.items) ? caseData.items.length : null;
  const generatedFallback = `/images/cases/${String(caseData.name || '').toLowerCase().replace(/ case$/,'').replace(/ /g,'_')}.png`;
  // New cases use webpack-imported assets so they are bundled into the production build.
  // This avoids any dependency on Vercel/public-file routing or stale DB image paths.
  const src = LOCAL_CASE_IMAGES[caseData.name] || caseData.image_url || generatedFallback;

  return (
    <article className="case-card-premium" style={{ '--case-accent': accent }}>
      <div className="case-card-glow" />
      <div className="case-image-container">
        <div className="case-card-badge">WELLCASE</div>
        <ImageWithFallback
          src={src}
          alt={caseData.name}
          className="case-image img-fluid"
        />
      </div>
      <div className="case-card-content">
        <div className="case-card-meta"><span>CASE DROP</span>{itemCount !== null && <span>{itemCount} DROPS</span>}</div>
        <h3>{caseData.name}</h3>
        <p>{caseData.description || 'Des skins rares, des surprises et une chance de faire exploser ton inventaire.'}</p>
        <div className="case-card-footer">
          <div className="case-price"><span>PRIX</span><strong>{Number(caseData.price).toLocaleString('fr-FR')} €</strong></div>
          <div className="case-open-actions">
            <button className="case-open-btn" disabled={!affordable} onClick={() => onOpen(caseData.id)}><span>{affordable ? 'OUVRIR' : 'SOLDE INSUFFISANT'}</span><b>↗</b></button>
            {onMultiOpen && open3Tokens > 0 && Number(balance) >= Number(caseData.price) * 3 && <button className="case-multi-btn" onClick={() => onMultiOpen(caseData.id, 3)}>×3 <small>{open3Tokens}</small></button>}
            {onMultiOpen && open5Tokens > 0 && Number(balance) >= Number(caseData.price) * 5 && <button className="case-multi-btn hot" onClick={() => onMultiOpen(caseData.id, 5)}>×5 <small>{open5Tokens}</small></button>}
          </div>
        </div>
      </div>
    </article>
  );
};
export default CaseCard;
