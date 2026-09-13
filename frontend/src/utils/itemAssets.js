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

const byId = {
  1: AkRedline,
  2: AkVulcan,
  3: AkFireSerpent,
  4: AkNeonRider,
  5: AkJaguar,
  6: M4Howl,
  7: M4HyperBeast,
  8: M4NeoNoir,
  9: M4Guardian,
  10: AwpDragonLore,
  11: AwpAsiimov,
  12: AwpMedusa,
  13: AwpLightningStrike,
  14: DeagleBlaze,
  15: DeagleCrimsonWeb,
  16: GlockFade,
  17: UspKillConfirmed,
  18: KarambitFade,
  19: M9CrimsonWeb,
  20: ButterflyDoppler,
  21: SportPandora,
  22: DriverImperial,
  23: AkHeadShot,
  24: M4Printstream,
  25: AwpGungnir,
  26: DeaglePrintstream,
  27: GlockGamma,
  28: KarambitGamma,
  29: M9Doppler,
  30: SportVice,
};

const normalize = (value) => String(value || '').trim().replace(/\s+/g, ' ').toLowerCase();

const byNormalizedName = Object.fromEntries(Object.entries(byName).map(([name, src]) => [normalize(name), src]));

const byFilename = (item) => {
  const raw = String(item?.image_url || '').split('/').pop()?.toLowerCase() || '';
  const key = raw.replace(/\.svg$/i, '.png');
  const aliases = {
    'ak_redline.png': AkRedline,
    'ak_redline.svg': AkRedline,
    'ak_vulcan.png': AkVulcan,
    'ak_vulcan.svg': AkVulcan,
    'ak_fire_serpent.png': AkFireSerpent,
    'ak_fire_serpent.svg': AkFireSerpent,
    'ak_neon_rider.png': AkNeonRider,
    'ak_neon_rider.svg': AkNeonRider,
    'ak_jaguar.png': AkJaguar,
    'ak_jaguar.svg': AkJaguar,
    'm4_howl.png': M4Howl,
    'm4_howl.svg': M4Howl,
    'm4_hyper_beast.png': M4HyperBeast,
    'm4_hyper_beast.svg': M4HyperBeast,
    'm4_neo_noir.png': M4NeoNoir,
    'm4_neo_noir.svg': M4NeoNoir,
    'm4_guardian.png': M4Guardian,
    'm4_guardian.svg': M4Guardian,
    'awp_dragon_lore.png': AwpDragonLore,
    'awp_dragon_lore.svg': AwpDragonLore,
    'awp_asiimov.png': AwpAsiimov,
    'awp_asiimov.svg': AwpAsiimov,
    'awp_medusa.png': AwpMedusa,
    'awp_medusa.svg': AwpMedusa,
    'awp_lightning_strike.png': AwpLightningStrike,
    'awp_lightning_strike.svg': AwpLightningStrike,
    'deagle_blaze.png': DeagleBlaze,
    'deagle_blaze.svg': DeagleBlaze,
    'deagle_crimson_web.png': DeagleCrimsonWeb,
    'deagle_crimson_web.svg': DeagleCrimsonWeb,
    'glock_fade.png': GlockFade,
    'glock_fade.svg': GlockFade,
    'usp_kill_confirmed.png': UspKillConfirmed,
    'usp_kill_confirmed.svg': UspKillConfirmed,
    'karambit_fade.png': KarambitFade,
    'karambit_fade.svg': KarambitFade,
    'm9_crimson_web.png': M9CrimsonWeb,
    'm9_crimson_web.svg': M9CrimsonWeb,
    'butterfly_doppler.png': ButterflyDoppler,
    'butterfly_doppler.svg': ButterflyDoppler,
    'sport_pandora.png': SportPandora,
    'sport_pandora.svg': SportPandora,
    'driver_imperial.png': DriverImperial,
    'driver_imperial.svg': DriverImperial,
    'ak_head_shot.png': AkHeadShot,
    'ak_head_shot.svg': AkHeadShot,
    'm4_printstream.png': M4Printstream,
    'm4_printstream.svg': M4Printstream,
    'awp_gungnir.png': AwpGungnir,
    'awp_gungnir.svg': AwpGungnir,
    'deagle_printstream.png': DeaglePrintstream,
    'deagle_printstream.svg': DeaglePrintstream,
    'glock_gamma.png': GlockGamma,
    'glock_gamma.svg': GlockGamma,
    'karambit_gamma.png': KarambitGamma,
    'karambit_gamma.svg': KarambitGamma,
    'm9_doppler.png': M9Doppler,
    'm9_doppler.svg': M9Doppler,
    'sport_vice.png': SportVice,
    'sport_vice.svg': SportVice,
  };
  return aliases[key] || '';
};

export const resolveItemImage = (item) => {
  if (!item) return '';
  return byId[item.id] || byNormalizedName[normalize(item.name)] || byFilename(item) || item.image_url || '';
};

export default byName;