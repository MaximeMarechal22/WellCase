import React, { useState, useEffect, useRef } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { casesAPI, openingsAPI } from '../services/api';
import ImageWithFallback from '../components/ImageWithFallback';
import { resolveCaseImage } from '../utils/caseAssets';
import CaseOpeningSplashUnified from '../components/CaseOpeningSplashUnified';
import { resolveItemImage } from '../utils/itemAssets';
import CaseOpeningAnimation from '../components/CaseOpeningAnimation';

const CaseDetailPage = () => {
  const { balance, updateBalance } = useAuth();
  const { caseId } = useParams();
  const navigate = useNavigate();

  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [showAnimation, setShowAnimation] = useState(false);
  const [showCaseSplash, setShowCaseSplash] = useState(false);
  const [animationCaseId, setAnimationCaseId] = useState(null);
  const [openingResult, setOpeningResult] = useState(null);
  const [openingRequest, setOpeningRequest] = useState(false);
  const [notice, setNotice] = useState('');
  const splashTimerRef = useRef(null);

  useEffect(() => () => clearTimeout(splashTimerRef.current), []);

  useEffect(() => {
    const fetchCaseDetails = async () => {
      try {
        const response = await casesAPI.getCaseById(caseId);
        setCaseData(response.data);
      } catch (err) {
        console.error(err);
        setError('Failed to load case details');
      } finally {
        setLoading(false);
      }
    };

    if (caseId) {
      fetchCaseDetails();
    }
  }, [caseId]);

  const handleOpenCase = async (count) => {
    if (!caseData || balance < Number(caseData.price) || openingRequest) return;
    setOpeningRequest(true);
    try {
      const response = await openingsAPI.openCase(caseData.id);
      setOpeningResult(response.data);
      setAnimationCaseId(caseData.id);
      setShowCaseSplash(true);
      clearTimeout(splashTimerRef.current);
      splashTimerRef.current = setTimeout(() => { setShowCaseSplash(false); setShowAnimation(true); }, 2200);
    } catch (error) {
      setNotice(error.response?.data?.detail || error.message || "Impossible d'ouvrir la caisse.");
    } finally {
      setOpeningRequest(false);
    }
  };

  const handleAnimationComplete = async (wonItem) => {
    await updateBalance();
  };

  const handleAnimationClose = () => {
    setShowAnimation(false);
    setAnimationCaseId(null);
    setOpeningResult(null);
  };

  if (loading) {
    return (
      <div className="container">
      {notice&&<div className="inline-notice">{notice}<button onClick={()=>setNotice('')}>×</button></div>}
        <div className="text-center py-5">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">
              Loading...
            </span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-6">

            <div className="alert alert-danger">
              {error}
            </div>

            <Link
              className="btn btn-outline-primary"
              to="/cases"
            >
              ← Back to Cases
            </Link>

          </div>
        </div>
      </div>
    );
  }

  if (!caseData) {
    return (
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-4">

            <div className="text-center py-5">
              <h3>Case not found</h3>

              <Link
                className="btn btn-outline-primary"
                to="/cases"
              >
                ← Back to Cases
              </Link>
            </div>

          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">

      {/* Header */}
      <div className="row mb-4">

        <div className="col-md-8">
          <h1 className="gradient-text">
            {caseData.name}
          </h1>

          <p className="lead">
            {caseData.description ||
              'A mysterious case with valuable rewards'}
          </p>
        </div>

        <div className="col-md-4 text-end">
          <div className="d-flex flex-column align-items-end">

            <span className="badge bg-primary fs-5 mb-2">
              {caseData.price.toLocaleString()} €
            </span>

            <h2>
              Balance:{' '}
              <span className="text-success">
                {balance.toLocaleString()} €
              </span>
            </h2>

          </div>
        </div>

      </div>

      {/* Case Image */}
      <div className="text-center mb-5">

        <ImageWithFallback
          src={resolveCaseImage(caseData)}
          alt={caseData.name}
          className="case-detail-image img-fluid"
          style={{
            maxWidth: '300px',
            maxHeight: '300px',
            borderRadius: '16px'
          }}
        />

      </div>

      {/* Case Contents */}
      <div className="row mb-5">

        <div className="col-12">

          <div className="card">

            <div className="card-header">
              <h5 className="mb-0">
                Case Contents
              </h5>
            </div>

            <div className="card-body">

              <div className="row g-4">
                {(caseData.items || []).map((item) => (
                  <div key={item.id} className="col-md-3 col-sm-6">
                    <div className="card-item text-center p-3 border rounded h-100">
                      <div className="item-icon mb-3">
                        <ImageWithFallback
                          src={resolveItemImage(item)}
                          alt={item.name}
                          className="img-fluid"
                          style={{ width: '90px', height: '90px', objectFit: 'contain' }}
                        />
                      </div>
                      <div className="item-name fw-medium">{item.name}</div>
                      <div className="text-muted small mt-1">{item.category}</div>
                      <div className="item-rarity badge mt-2" style={{ backgroundColor: item.color || '#6c757d' }}>
                        {item.rarity}
                      </div>
                      <div className="item-probability text-muted small mt-2">
                        {Number(item.probability).toFixed(2)}%
                      </div>
                      <div className="small text-muted">
                        {Number(item.virtual_value).toLocaleString()} €
                      </div>
                    </div>
                  </div>
                ))}
              </div>

            </div>

          </div>

        </div>

      </div>

      {/* Open Options */}
      <div className="row g-4 mb-5">

        <div className="col-12">

          <h4>
            Open Options
          </h4>

          <button
            type="button"
            className="btn btn-primary w-100"
            disabled={balance < Number(caseData.price) || showAnimation}
            onClick={() => handleOpenCase(caseData.id)}
          >
            {balance >= Number(caseData.price) ? `Open for ${Number(caseData.price).toLocaleString()} €` : `Need ${(Number(caseData.price) - Number(balance)).toLocaleString()} € more`}
          </button>
          <div className="form-text mt-2">The server selects the drop first; the roulette only reveals it.</div>

        </div>

      </div>


      {showCaseSplash && <CaseOpeningSplashUnified caseData={caseData} />}

      {/* Case Opening Animation */}
      {showAnimation && (
        <div
          className="opening-overlay active"
        >

          <div
            className="opening-overlay-content"
            onClick={(e) => e.stopPropagation()}
          >

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

export default CaseDetailPage;