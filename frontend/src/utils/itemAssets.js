import AkRedline from '../assets/items/ak_redline.png';
import AkVulcan from '../assets/items/ak_vulcan.png';
import AkFireSerpent from '../assets/items/ak_fire_serpent.png';
import AkNeonRider from '../assets/items/ak_neon_rider.png';
import AkJaguar from '../assets/items/ak_jaguar.png';
import M4Howl from '../assets/items/m4_howl.png';
import M4HyperBeast from '../assets/items/m4_hyper_beast.png';
import M4NeoNoir from '../assets/items/m4_neo_noir.png';
import M4Guardian from '../assets/items/m4_guardian.png';
import AwpDragonLore from '../assets/items/awp_dragon_lore.png';
import AwpAsiimov from '../assets/items/awp_asiimov.png';
import AwpMedusa from '../assets/items/awp_medusa.png';
import AwpLightningStrike from '../assets/items/awp_lightning_strike.png';
import DeagleBlaze from '../assets/items/deagle_blaze.png';
import DeagleCrimsonWeb from '../assets/items/deagle_crimson_web.png';
import GlockFade from '../assets/items/glock_fade.png';
import UspKillConfirmed from '../assets/items/usp_kill_confirmed.png';
import KarambitFade from '../assets/items/karambit_fade.png';
import M9CrimsonWeb from '../assets/items/m9_crimson_web.png';
import ButterflyDoppler from '../assets/items/butterfly_doppler.png';
import SportPandora from '../assets/items/sport_pandora.png';
import DriverImperial from '../assets/items/driver_imperial.png';
import AkHeadShot from '../assets/items/ak_head_shot.png';
import M4Printstream from '../assets/items/m4_printstream.png';
import AwpGungnir from '../assets/items/awp_gungnir.png';
import DeaglePrintstream from '../assets/items/deagle_printstream.png';
import GlockGamma from '../assets/items/glock_gamma.png';
import KarambitGamma from '../assets/items/karambit_gamma.png';
import M9Doppler from '../assets/items/m9_doppler.png';
import SportVice from '../assets/items/sport_vice.png';

const byName = {
  'AK-47 | Redline': AkRedline,
  'AK-47 | Vulcan': AkVulcan,
  'AK-47 | Fire Serpent': AkFireSerpent,
  'AK-47 | Neon Rider': AkNeonRider,
  'AK-47 | Jaguar': AkJaguar,
  'M4A4 | Howl': M4Howl,
  'M4A1-S | Hyper Beast': M4HyperBeast,
  'M4A4 | Neo-Noir': M4NeoNoir,
  'M4A1-S | Guardian': M4Guardian,
  'AWP | Dragon Lore': AwpDragonLore,
  'AWP | Asiimov': AwpAsiimov,
  'AWP | Medusa': AwpMedusa,
  'AWP | Lightning Strike': AwpLightningStrike,
  'Desert Eagle | Blaze': DeagleBlaze,
  'Desert Eagle | Crimson Web': DeagleCrimsonWeb,
  'Glock-18 | Fade': GlockFade,
  'USP-S | Kill Confirmed': UspKillConfirmed,
  'Karambit | Fade': KarambitFade,
  'M9 Bayonet | Crimson Web': M9CrimsonWeb,
  'Butterfly Knife | Doppler': ButterflyDoppler,
  "Sport Gloves | Pandora's Box": SportPandora,
  'Driver Gloves | Imperial Plaid': DriverImperial,
  'AK-47 | Head Shot': AkHeadShot,
  'M4A1-S | Printstream': M4Printstream,
  'AWP | Gungnir': AwpGungnir,
  'Desert Eagle | Printstream': DeaglePrintstream,
  'Glock-18 | Gamma Doppler': GlockGamma,
  'Karambit | Gamma Doppler': KarambitGamma,
  'M9 Bayonet | Doppler': M9Doppler,
  'Sport Gloves | Vice': SportVice,
};

const normalize = (value) => String(value || '')
  .trim()
  .replace(/\s+/g, ' ')
  .toLowerCase();

const byNormalizedName = Object.fromEntries(
  Object.entries(byName).map(([name, src]) => [normalize(name), src])
);

const byLegacyFilename = {
  'ak_redline.png': AkRedline,
  'ak_vulcan.png': AkVulcan,
  'ak_fire_serpent.png': AkFireSerpent,
  'ak_neon_rider.png': AkNeonRider,
  'ak_jaguar.png': AkJaguar,
  'm4_howl.png': M4Howl,
  'm4_hyper_beast.png': M4HyperBeast,
  'm4_neo_noir.png': M4NeoNoir,
  'm4_guardian.png': M4Guardian,
  'awp_dragon_lore.png': AwpDragonLore,
  'awp_asiimov.png': AwpAsiimov,
  'awp_medusa.png': AwpMedusa,
  'awp_lightning_strike.png': AwpLightningStrike,
  'deagle_blaze.png': DeagleBlaze,
  'deagle_crimson_web.png': DeagleCrimsonWeb,
  'glock_fade.png': GlockFade,
  'usp_kill_confirmed.png': UspKillConfirmed,
  'karambit_fade.png': KarambitFade,
  'm9_crimson_web.png': M9CrimsonWeb,
  'butterfly_doppler.png': ButterflyDoppler,
  'sport_pandora.png': SportPandora,
  'driver_imperial.png': DriverImperial,
  'ak_head_shot.png': AkHeadShot,
  'm4_printstream.png': M4Printstream,
  'awp_gungnir.png': AwpGungnir,
  'deagle_printstream.png': DeaglePrintstream,
  'glock_gamma.png': GlockGamma,
  'karambit_gamma.png': KarambitGamma,
  'm9_doppler.png': M9Doppler,
  'sport_vice.png': SportVice,
};

export const resolveItemImage = (item) => {
  if (!item) return '';
  // IMPORTANT: name is the stable identity. Never use numeric DB ids first,
  // because PostgreSQL/SQLite migrations can assign different ids.
  const byNameMatch = byNormalizedName[normalize(item.name)];
  if (byNameMatch) return byNameMatch;

  const raw = String(item.image_url || '').split('/').pop()?.toLowerCase() || '';
  const key = raw.replace(/\.svg$/i, '.png');
  return byLegacyFilename[key] || '';
};

export default byName;
