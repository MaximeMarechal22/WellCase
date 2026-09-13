import Advanced from '../assets/cases/advanced.png';
import AkSpecialist from '../assets/cases/ak_specialist.png';
import AwpSpecialist from '../assets/cases/awp_specialist.png';
import Beginner from '../assets/cases/beginner.png';
import Covert from '../assets/cases/covert.png';
import Elite from '../assets/cases/elite.png';
import Knife from '../assets/cases/knife.png';
import Neon from '../assets/cases/neon.png';
import Supreme from '../assets/cases/supreme.png';

const normalize = (value) => String(value || '')
  .trim()
  .replace(/\s+/g, ' ')
  .toLowerCase();

const byName = {
  'Beginner Case': Beginner,
  'Advanced Case': Advanced,
  'Elite Case': Elite,
  'AK Specialist Case': AkSpecialist,
  'AWP Specialist Case': AwpSpecialist,
  'Neon Case': Neon,
  'Knife Case': Knife,
  'Covert Case': Covert,
  'Supreme Case': Supreme,
};

const aliases = {
};

const normalizedMap = Object.fromEntries([
  ...Object.entries(byName),
  ...Object.entries(aliases),
].map(([name, src]) => [normalize(name), src]));

const fromImageUrl = (value) => {
  const raw = normalize(value);
  if (raw.includes('/neon')) return Neon;
  if (raw.includes('/knife')) return Knife;
  if (raw.includes('/covert')) return Covert;
  if (raw.includes('/supreme')) return Supreme;
  return '';
};

export const resolveCaseImage = (value) => {
  if (!value) return '';
  if (typeof value === 'object') {
    const byExactName = normalizedMap[normalize(value.name)];
    if (byExactName) return byExactName;
    const byUrl = fromImageUrl(value.image_url || value.image);
    if (byUrl) return byUrl;
    return '';
  }
  return normalizedMap[normalize(value)] || fromImageUrl(value) || '';
};

// Kept for compatibility with older imports. Arsenal splash images are no longer used.
export const resolveCaseSplashImage = resolveCaseImage;
export const splashByName = {};
export default byName;
