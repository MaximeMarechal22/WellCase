import React from 'react';

const RewardCard = ({ dayStreak, rewardAmount, onClaim }) => (
  <div className="card text-center daily-reward-card">
    <div className="card-header"><h3>BONUS QUOTIDIEN · JOUR {dayStreak}</h3></div>
    <div className="card-body">
      <h2 className="text-success">{Number(rewardAmount || 0).toLocaleString('fr-FR')} €</h2>
      <p className="card-text">Récupère ton bonus une fois par jour.</p>
      <button className="btn btn-primary w-100" onClick={onClaim} disabled={!onClaim}>RÉCUPÉRER LE BONUS</button>
    </div>
  </div>
);
export default RewardCard;
