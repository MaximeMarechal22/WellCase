import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { dailyRewardsAPI } from '../services/api';
import RewardCard from '../components/RewardCard';

const HomePage = () => {
  const { balance, updateBalance } = useAuth();

  const [dailyReward, setDailyReward] = useState(null);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const rewardResponse = await dailyRewardsAPI.getStatus();
        setDailyReward(rewardResponse.data?.can_claim ? rewardResponse.data : null);
      } catch (error) {
        console.error('Error fetching daily reward:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

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
      <div className="container home-page">
        <div className="home-loading"><div className="spinner-border text-primary" role="status"><span className="visually-hidden">Chargement…</span></div></div>
      </div>
    );
  }

  return (
    <div className="container home-page home-page-clean">
      {notice && <div className="inline-notice home-notice">{notice}<button onClick={() => setNotice('')}>×</button></div>}

      <section className="home-clean-hero">
        <div className="home-clean-hero-copy">
          <div className="section-kicker">WELLCASE / DROP CENTER</div>
          <div className="home-clean-status"><i /> SYSTÈME EN LIGNE <span>DROP ENGINE ACTIF</span></div>
          <h1>Le risque.<br /><span>Le frisson.</span><br />Le jackpot.</h1>
          <p>Une expérience de cases pensée autour de la transparence : consulte tes probabilités, maîtrise ton bankroll et ouvre uniquement quand le moment est bon.</p>
          <div className="home-clean-actions">
            <a href="/cases" className="home-clean-primary">EXPLORER LES CAISSES <b>↗</b></a>
            <a href="/guide" className="home-clean-secondary">COMMENT ÇA MARCHE <b>?</b></a>
          </div>
        </div>

        <div className="home-clean-visual" aria-hidden="true">
          <div className="home-clean-grid" />
          <div className="home-clean-orbit orbit-one" /><div className="home-clean-orbit orbit-two" />
          <div className="home-clean-core">
            <div className="home-clean-core-mark">W</div>
            <span>WELLCASE</span>
            <small>DROP ENGINE</small>
          </div>
          <div className="home-clean-signal signal-one"><b>01</b><span>CHOISIR</span></div>
          <div className="home-clean-signal signal-two"><b>02</b><span>VÉRIFIER</span></div>
          <div className="home-clean-signal signal-three"><b>03</b><span>OUVRIR</span></div>
        </div>
      </section>

      <section className="home-clean-stats">
        <div><span>SOLDE DISPONIBLE</span><strong>{Number(balance || 0).toLocaleString('fr-FR')} €</strong><small>Ton bankroll en temps réel</small></div>
        <div><span>PROBABILITÉS</span><strong>100%</strong><small>Visibles avant chaque ouverture</small></div>
        <div><span>RÉSULTAT</span><strong>SERVER-SIDE</strong><small>Le drop est déterminé avant la roulette</small></div>
      </section>

      <section className="home-clean-panels">
        <div className="home-clean-panel">
          <span className="section-kicker">01 / TRANSPARENCE</span>
          <h2>Chaque drop a son taux.</h2>
          <p>Un clic sur une caisse suffit pour ouvrir son aperçu. Tu vois directement la probabilité de chaque item avant de prendre ta décision.</p>
          <a href="/cases">VOIR LE CATALOGUE <b>→</b></a>
        </div>
        <div className="home-clean-panel home-clean-panel-accent">
          <span className="section-kicker">02 / BANKROLL</span>
          <h2>Joue ton rythme.</h2>
          <p>Garde une lecture claire de ton solde, de tes gains et de ton inventaire. Ici, l'interface reste au service du drop.</p>
          <a href="/inventory">MON INVENTAIRE <b>→</b></a>
        </div>
      </section>

      <section className="home-clean-bottom">
        <div><span>WELLCASE</span><strong>NOISE OFF. DROP ON.</strong></div>
        <a href="/history">CONSULTER MON HISTORIQUE ↗</a>
      </section>

      {dailyReward?.can_claim ? (
        <div className="home-clean-daily">
          <RewardCard dayStreak={dailyReward.day_streak || dailyReward.dayStreak || 0} rewardAmount={dailyReward.reward_amount || 0} onClaim={handleClaimDailyReward} />
        </div>
      ) : dailyReward ? (
        <div className="daily-claimed-strip" aria-live="polite">✓ Bonus quotidien déjà récupéré — reviens demain pour la prochaine récompense.</div>
      ) : null}
    </div>
  );

};

export default HomePage;