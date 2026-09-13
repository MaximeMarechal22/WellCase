import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { casesAPI, dailyRewardsAPI, openingsAPI, progressionAPI } from '../services/api';
import CaseCard from '../components/CaseCard';
import RewardCard from '../components/RewardCard';
import CaseOpeningAnimation from '../components/CaseOpeningAnimation';
import ImageWithFallback from '../components/ImageWithFallback';

const HomePage = () => {
  const { balance, updateBalance } = useAuth();

  const [cases, setCases] = useState([]);
  const [dailyReward, setDailyReward] = useState(null);
  const [loading, setLoading] = useState(true);

  const [showAnimation, setShowAnimation] = useState(false);
  const [animationCaseId, setAnimationCaseId] = useState(null);
  const [wonItemFromAnimation, setWonItemFromAnimation] = useState(null);
  const [openingResult, setOpeningResult] = useState(null);
  const [openingRequest, setOpeningRequest] = useState(false);
  const [progression, setProgression] = useState({open3_tokens:0, open5_tokens:0});
  const [batchResults, setBatchResults] = useState([]);
  const [batchIndex, setBatchIndex] = useState(0);
  const [notice, setNotice] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const casesResponse = await casesAPI.getCases();
        setCases(casesResponse.data);
        try { const p = await progressionAPI.getOverview(); setProgression(p.data); } catch(e) { console.warn('progression', e); }

        const rewardResponse = await dailyRewardsAPI.getStatus();
        setDailyReward(rewardResponse.data?.can_claim ? rewardResponse.data : null);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
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
    if (openingRequest) return; setOpeningRequest(true);
    try { const r = await openingsAPI.openBatch(caseId, count); setBatchResults(r.data.results||[]); setBatchIndex(0); setOpeningResult(r.data.results?.[0]||null); setAnimationCaseId(caseId); setShowAnimation(true); setProgression(p=>({...p,open3_tokens:r.data.open3_tokens,open5_tokens:r.data.open5_tokens})); }
    catch(e){ setNotice(e.response?.data?.detail || `Impossible de lancer l'ouverture ×${count}.`); } finally { setOpeningRequest(false); }
  };

  const handleAnimationComplete = async (wonItem) => {
    setWonItemFromAnimation(wonItem);
    await updateBalance();
  };

  const handleAnimationClose = () => {
    if (batchResults.length && batchIndex < batchResults.length - 1) { const next=batchIndex+1; setBatchIndex(next); setOpeningResult(batchResults[next]); return; }
    setShowAnimation(false); setWonItemFromAnimation(null); setOpeningResult(null); setAnimationCaseId(null); setBatchResults([]); setBatchIndex(0); updateBalance();
  };

  const handleClaimDailyReward = async () => {
    try {
      const response = await dailyRewardsAPI.claimReward();

      setDailyReward(null);
      await updateBalance();

      setNotice(`Bonus récupéré : +${response.data.reward_amount} €`);
    } catch (error) {
      console.error('Error claiming daily reward:', error);

      setNotice(error.response?.data?.detail || error.message || 'Impossible de récupérer le bonus.');
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="text-center py-5">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      {notice && <div className="inline-notice home-notice">{notice}<button onClick={()=>setNotice('')}>×</button></div>}

      <section className="home-hero">
        <div className="home-hero-copy">
          <div className="section-kicker">WELLCASE / OPEN. WIN. REPEAT.</div>
          <h1>Le prochain <span>gros drop</span><br />commence ici.</h1>
          <p>Ouvre, upgrade, construis ton inventaire et bats ton pote sur 48 heures.</p>
          <div className="hero-actions">
            <a href="#popular-cases" className="hero-primary">VOIR LES CAISSES <b>↗</b></a>
            <div className="hero-stat"><strong>{Number(balance || 0).toLocaleString('fr-FR')} €</strong><span>BANKROLL ACTUEL</span></div>
          </div>
        </div>
        <div className="home-hero-art">
          <div className="hero-orb hero-orb-one" />
          <div className="hero-orb hero-orb-two" />
          <div className="hero-case-stack">
            <div className="hero-case-back" />
            <div className="hero-case-front"><span>W</span><small>WELLCASE</small></div>
          </div>
          <div className="hero-watermark">48H<br/><span>DUEL</span></div>
        </div>
      </section>

      <section className="duel-strip home-duel">
        <div className="duel-icon">VS</div>
        <div><strong>TON POTE EST-IL MEILLEUR QUE TOI ?</strong><span>Lancez un challenge de 48H : skins gagnés, upgrades et bankroll comptent.</span></div>
        <div className="duel-rule">48H / 1 GAGNANT</div>
      </section>

      {/* Daily Reward */}
      {dailyReward?.can_claim ? (
        <div className="row mb-5">
          <div className="col-md-4">
            <RewardCard
              dayStreak={dailyReward.day_streak || dailyReward.dayStreak || 0}
              rewardAmount={dailyReward.reward_amount || 0}
              onClaim={handleClaimDailyReward}
            />
          </div>
        </div>
      ) : dailyReward ? (
        <div className="daily-claimed-strip" aria-live="polite">✓ Bonus quotidien déjà récupéré — reviens demain pour la prochaine récompense.</div>
      ) : null}

      {/* Popular Cases */}
      <div className="mb-5" id="popular-cases">
        <div className="section-heading"><div><div className="section-kicker">THE DROP WALL</div><h2>Caisses populaires</h2></div><span>CHOISIS TON RISQUE</span></div>

        <div className="cases-grid-premium">
          {cases.map((caseItem) => (
            <CaseCard key={caseItem.id} case={caseItem} onOpen={handleOpenCase} onMultiOpen={handleMultiOpen} balance={balance} open3Tokens={progression.open3_tokens || 0} open5Tokens={progression.open5_tokens || 0} />
          ))}
        </div>
      </div>

      {/* Case Opening Animation */}
      {showAnimation && (
        <div
          className="opening-overlay active"
        >
          <div
            className="opening-overlay-content"
            onClick={(e) => e.stopPropagation()}
          >
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

export default HomePage;