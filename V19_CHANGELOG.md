# WellCase V19 — économie + audio léger

## Économie des caisses
Les probabilités stockées en base restent intactes pour conserver le catalogue. Au moment du tirage, un coefficient économique est appliqué selon le ratio `valeur du skin / prix de la caisse`, puis les poids sont renormalisés à 100%.

Coefficients :
- <= 0,75x : 1,35x
- <= 1x : 1,15x
- <= 1,5x : 0,90x
- <= 2x : 0,65x
- <= 4x : 0,45x
- > 4x : 0,20x

Les drops très rentables sont donc moins fréquents, sans rendre les caisses mortes.

## Audio
Pas de fichiers audio externes : les petits sons sont synthétisés via Web Audio API.
- petit son de lancement
- quelques ticks très discrets pendant la roulette
- petit jingle de victoire à l'arrêt

Le volume est volontairement bas et les sons ne sont joués qu'à l'ouverture.
