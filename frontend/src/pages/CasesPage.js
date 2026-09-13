import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { casesAPI, openingsAPI, progressionAPI } from '../services/api';
import CaseCard from '../components/CaseCard';
import CaseOpeningAnimation from '../components/CaseOpeningAnimation';

const CasesPage = () => {
  const { balance, updateBalance } = useAuth();
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAnimation, setShowAnimation] = useState(false);
  const [animationCaseId, setAnimationCaseId] = useState(null);
  const [openingResult, setOpeningResult] = useState(null);
  const [openingRequest, setOpeningRequest] = useState(false);
  const [progression, setProgression] = useState({ open3_tokens: 0, open5_tokens: 0 });
  const [batchResults, setBatchResults] = useState([]);
  const [batchIndex, setBatchIndex] = useState(0);
  const [notice, setNotice] = useState('');

  useEffect(() => {
    const fetchCases = async () => {
      try {
        const casesResponse = await casesAPI.getCases();
        setCases(casesResponse.data);
        try { const p = await progressionAPI.getOverview(); setProgression(p.data); } catch (e) { console.warn('progression', e); }
      } catch (error) {
        console.error('Error fetching cases:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCases();
  }, []);

  const handleOpenCase = async (caseId) => {
    if (openingRequest) return;
    setOpeningRequest(true);
    try {
      const response = await openingsAPI.openCase(caseId);
      setOpeningResult(response.data);
      setAnimationCaseId(caseId);
      setShowAnimation(true);
    } catch (error) {
      setNotice(error.response?.data?.detail || error.message || "Impossible d'ouvrir la caisse.");
    } finally {
      setOpeningRequest(false);
    }
  };


  const handleMultiOpen = async (caseId, count) => {
    if (openingRequest) return;
    setOpeningRequest(true);
    try {
      const response = await openingsAPI.openBatch(caseId, count);
      setBatchResults(response.data.results || []);
      setBatchIndex(0);
      setOpeningResult(response.data.results?.[0] || null);
      setAnimationCaseId(caseId);
      setShowAnimation(true);
      setProgression((p) => ({ ...p, open3_tokens: response.data.open3_tokens, open5_tokens: response.data.open5_tokens }));
    } catch (error) {
      setNotice(error.response?.data?.detail || error.message || `Impossible de lancer l'ouverture ×${count}.`);
    } finally { setOpeningRequest(false); }
  };

  const handleAnimationComplete = (wonItem) => {
    // Update balance after animation
    updateBalance();
  };

  const handleAnimationClose = () => {
    if (batchResults.length && batchIndex < batchResults.length - 1) {
      const next = batchIndex + 1;
      setBatchIndex(next);
      setOpeningResult(batchResults[next]);
      return;
    }
    setShowAnimation(false); setAnimationCaseId(null); setOpeningResult(null); setBatchResults([]); setBatchIndex(0);
    updateBalance();
  };



  if (loading) {
    return (
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-4">
            <div className="text-center py-5">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container cases-page">{notice&&<div className="inline-notice">{notice}<button onClick={()=>setNotice('')}>×</button></div>}
      <section className="cases-hero">
        <div>
          <div className="section-kicker">WELLCASE / CASE MARKET</div>
          <h1>Choisis ton <em>drop.</em></h1>
          <p>Des caisses pensées pour les gros coups, les upgrades et les duels entre potes.</p>
        </div>
        <div className="cases-balance-card">
          <span>TON CASH</span>
          <strong>{Number(balance || 0).toLocaleString('fr-FR')} €</strong>
        </div>
      </section>

      <section className="duel-strip">
        <div className="duel-icon">48H</div>
        <div>
          <strong>MODE DUEL — TOI VS TON POTE</strong>
          <span>Le plus gros inventaire + le plus gros bankroll à la fin gagne.</span>
        </div>
        <div className="duel-rule">SKINS + CASH</div>
      </section>

      <div className="cases-grid-premium">
        {cases.map(caseItem => (
          <CaseCard
            key={caseItem.id}
            case={caseItem}
            onOpen={handleOpenCase}
            balance={balance}
            onMultiOpen={handleMultiOpen}
            open3Tokens={progression.open3_tokens || 0}
            open5Tokens={progression.open5_tokens || 0}
          />
        ))}
      </div>

      {/* Case Opening Animation Overlay */}
      {showAnimation && (
        <div className={`opening-overlay ${showAnimation ? 'active' : ''}`}>
          <div className="opening-overlay-content" onClick={(e) => e.stopPropagation()}>
            <div className="batch-opening-indicator">{batchResults.length > 1 ? `OUVERTURE ${batchIndex + 1} / ${batchResults.length}` : "OUVERTURE"}</div>
            <CaseOpeningAnimation
              caseId={animationCaseId}
              openingResult={openingResult}
              onComplete={handleAnimationComplete}
              onClose={handleAnimationClose}
            />
            </div>
        </div>
      )}


    </div>
  );
};

export default CasesPage;