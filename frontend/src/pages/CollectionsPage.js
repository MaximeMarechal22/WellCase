import React, { useEffect, useMemo, useState } from 'react';
import { collectionsAPI } from '../services/api';
import ImageWithFallback from '../components/ImageWithFallback';
import { resolveItemImage } from '../utils/itemAssets';

const ICONS = {
  'Assault Rifles': '✦',
  Snipers: '⌁',
  Pistols: '◈',
  Knives: '◬',
  Gloves: '◉',
};

export default function CollectionsPage() {
  const [data, setData] = useState(null);
  const [selectedKey, setSelectedKey] = useState('Assault Rifles');

  useEffect(() => {
    collectionsAPI.getOverview().then((r) => {
      setData(r.data);
      const first = r.data?.collections?.find((x) => x.total > 0);
      if (first) setSelectedKey(first.key);
    }).catch(console.error);
  }, []);

  const selected = useMemo(
    () => data?.collections?.find((c) => c.key === selectedKey) || data?.collections?.[0],
    [data, selectedKey]
  );

  if (!data) return <div className="container py-5">Chargement…</div>;

  return (
    <div className="container collections-page">
      <section className="collections-hero">
        <span className="section-kicker">WELLCASE / COLLECTIONS</span>
        <h1>Complète tes <em>collections.</em></h1>
        <p>Choisis une catégorie pour voir chaque arme, celles déjà obtenues et celles qu'il te manque encore.</p>
      </section>

      <div className="collections-grid">
        {data.collections.map((c) => (
          <button
            className={`collection-card ${selected?.key === c.key ? 'selected' : ''} ${c.complete ? 'complete' : ''}`}
            key={c.key}
            onClick={() => setSelectedKey(c.key)}
            type="button"
          >
            <div className="collection-icon">{ICONS[c.key] || '✦'}</div>
            <div>
              <span>{c.label}</span>
              <h2>{c.owned} / {c.total}</h2>
              <div className="collection-track"><i style={{ width: `${c.total ? (c.owned / c.total) * 100 : 0}%` }} /></div>
              <p>{c.bonus}</p>
              {c.complete && <strong>✓ {c.badge}</strong>}
            </div>
          </button>
        ))}
      </div>

      {selected && (
        <section className="collection-detail-panel">
          <div className="collection-detail-header">
            <div>
              <span className="section-kicker">COLLECTION SÉLECTIONNÉE</span>
              <h2>{selected.label} <small>{selected.owned}/{selected.total}</small></h2>
              <p>{selected.complete ? 'Collection terminée : tous les skins sont dans ton inventaire.' : 'Chaque carte te montre précisément ce que tu possèdes et ce qu’il te reste à obtenir.'}</p>
            </div>
            <div className="collection-detail-badge">{selected.complete ? 'COMPLÈTE' : `${selected.total - selected.owned} À TROUVER`}</div>
          </div>

          <div className="collection-items-grid">
            {selected.items.map((item) => (
              <article className={`collection-item-card ${item.owned ? 'owned' : 'missing'}`} key={item.id}>
                <div className="collection-item-visual">
                  <ImageWithFallback src={resolveItemImage(item)} alt={item.name} />
                  <span className="collection-rarity">{item.rarity}</span>
                </div>
                <div className="collection-item-copy">
                  <span>{item.owned ? 'OBTENUE' : 'MANQUANTE'}</span>
                  <h3>{item.name}</h3>
                  <strong>{Number(item.virtual_value || 0).toLocaleString('fr-FR')} €</strong>
                </div>
              </article>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
