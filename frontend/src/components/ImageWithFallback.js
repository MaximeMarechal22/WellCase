import React from 'react';

const FALLBACK_IMAGE =
  'data:image/svg+xml,%3Csvg xmlns=%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22 viewBox=%220 0 160 120%22%3E%3Crect width=%22160%22 height=%22120%22 rx=%2216%22 fill=%22%230d121b%22/%3E%3Cpath d=%22M45 82l20-24 15 15 12-16 23 25%22 fill=%22%23333c4d%22/%3E%3Ccircle cx=%2261%22 cy=%2244%22 r=%2210%22 fill=%22%23515c70%22/%3E%3C/svg%3E';

const resolveSrc = (value) => {
  if (!value) return FALLBACK_IMAGE;
  if (/^(https?:|data:|blob:)/i.test(value)) return value;
  if (value.startsWith('/')) return value;
  return `/${value}`;
};

const ImageWithFallback = ({ src, alt = '', onError, ...props }) => {
  const handleError = (event) => {
    event.currentTarget.onerror = null;
    event.currentTarget.src = FALLBACK_IMAGE;
    onError?.(event);
  };

  return <img {...props} src={resolveSrc(src)} alt={alt} onError={handleError} />;
};

export default ImageWithFallback;
