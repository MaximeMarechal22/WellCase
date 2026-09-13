import neon from '../assets/cases/neon.png';
import knife from '../assets/cases/knife.png';
import covert from '../assets/cases/covert.png';
import supreme from '../assets/cases/supreme.png';
const map={'Neon Case':neon,'Knife Case':knife,'Covert Case':covert,'Supreme Case':supreme};
export const resolveCaseImage=c=>c?.name&&map[c.name]?map[c.name]:(c?.image_url||'');
export default map;
