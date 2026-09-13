import React, { useMemo } from 'react';
import { createPortal } from 'react-dom';
import ImageWithFallback from './ImageWithFallback';
import { resolveCaseImage } from '../utils/caseAssets';
import { resolveItemImage } from '../utils/itemAssets';
import './CasePreviewModal.css';

const colorFor = (rarity) => ({
  'Mil-Spec':'#5ea7e8', Restricted:'#7f6acb', Classified:'#bd5bd0', Covert:'#d85a5a',
  Contraband:'#ce9c43', Extraordinary:'#b7a74b', Legendary:'#c85e76', Mythic:'#c88fd0'
}[rarity] || '#93a2b2');

export default function CasePreviewModal({ caseData, onClose, onOpen, externalLoading = false }) {
  const details = caseData || {};
  const items = useMemo(() => [...(Array.isArray(details.items) ? details.items : [])].sort((a,b) => Number(b.probability||0)-Number(a.probability||0)), [details]);
  if (!caseData) return null;

  const root = document.getElementById('root');
  const mount = document.body;
  const node = (
    <div className="case-preview-backdrop" role="dialog" aria-modal="true" aria-label={`Drops de ${details.name||'caisse'}`} onMouseDown={e=>{if(e.target===e.currentTarget) onClose?.();}}>
      <div className="case-preview-modal">
        <button className="case-preview-close" onClick={onClose} aria-label="Fermer">×</button>
        <div className="case-preview-hero">
          <div className="case-preview-image-wrap">
            <div className="case-preview-glow" />
            <div className="case-preview-art-stage">
              <ImageWithFallback src={resolveCaseImage(details)} alt={details.name} className="case-preview-image" />
            </div>
          </div>
          <div className="case-preview-head">
            <span className="case-preview-kicker">APERÇU DE LA CAISSE</span>
            <h2>{details.name}</h2>
            <p>{details.description || 'Découvre précisément le contenu et les probabilités avant ouverture.'}</p>
            <div className="case-preview-meta"><strong>{Number(details.price||0).toLocaleString('fr-FR')} €</strong><span>{items.length} drops</span></div>
            <div className="case-preview-actions">
              <button className="case-preview-open" disabled={externalLoading} onClick={()=>onOpen?.(details.id)}>{externalLoading ? 'CHARGEMENT DES TAUX…' : 'OUVRIR LA CAISSE'}</button>
              <button className="case-preview-secondary" onClick={onClose}>FERMER</button>
            </div>
          </div>
        </div>

        <div className="case-preview-section-title"><span>PROBABILITÉS DE DROP</span><small>{externalLoading ? 'Calcul des taux serveur…' : 'Probabilité réelle de chaque drop dans cette caisse.'}</small></div>
        <div className="case-preview-items">
          {externalLoading ? <div className="case-preview-loading">Chargement des taux de drop…</div> : items.length === 0 ? <div className="case-preview-loading">Aucun drop n'est encore associé à cette caisse.</div> : items.map(item=>{
            const chance=Number(item.probability||0), rc=colorFor(item.rarity);
            return <div className="case-preview-item" key={item.id}>
              <div className="case-preview-item-image"><ImageWithFallback src={resolveItemImage(item)} alt={item.name}/></div>
              <div className="case-preview-item-info">
                <div className="case-preview-item-top"><strong>{item.name}</strong></div>
                <div className="case-preview-meter"><i style={{width:`${Math.max(.2,Math.min(100,chance))}%`,background:rc}}/></div>
                <div className="case-preview-item-bottom"><span>{chance.toFixed(3)}% de chance de drop</span></div>
              </div>
            </div>;
          })}
        </div>
      </div>
    </div>
  );
  return createPortal(node, mount);
}
