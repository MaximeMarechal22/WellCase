let audioContext = null;

const getContext = () => {
  if (typeof window === 'undefined') return null;
  const AudioCtx = window.AudioContext || window.webkitAudioContext;
  if (!AudioCtx) return null;
  if (!audioContext) audioContext = new AudioCtx();
  if (audioContext.state === 'suspended') audioContext.resume().catch(() => {});
  return audioContext;
};

const tone = ({ frequency = 440, duration = 0.07, volume = 0.035, type = 'sine', delay = 0 }) => {
  const ctx = getContext();
  if (!ctx) return;
  const now = ctx.currentTime + delay;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(frequency, now);
  gain.gain.setValueAtTime(0.0001, now);
  gain.gain.exponentialRampToValueAtTime(volume, now + 0.008);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start(now);
  osc.stop(now + duration + 0.02);
};

export const playOpeningStart = () => {
  tone({ frequency: 220, duration: 0.09, volume: 0.028, type: 'triangle' });
  tone({ frequency: 330, duration: 0.12, volume: 0.02, type: 'triangle', delay: 0.045 });
};

export const playOpeningTick = (index = 0) => {
  const frequencies = [560, 620, 680, 740];
  tone({ frequency: frequencies[index % frequencies.length], duration: 0.045, volume: 0.018, type: 'square' });
};

export const playOpeningWin = () => {
  tone({ frequency: 523, duration: 0.13, volume: 0.028, type: 'sine' });
  tone({ frequency: 659, duration: 0.16, volume: 0.025, type: 'sine', delay: 0.08 });
  tone({ frequency: 784, duration: 0.22, volume: 0.022, type: 'sine', delay: 0.16 });
};
