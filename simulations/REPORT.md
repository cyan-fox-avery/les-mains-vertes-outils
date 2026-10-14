# Rapport de simulations — première exécution du plan

> **Statut : résultats à examiner, recommandation PROPOSÉE, rien n’est adopté.**
> Les seuils du plan sont des propositions. Quand un seuil n’est pas
> respecté, ce rapport le dit explicitement — on ne relâche jamais
> silencieusement une contrainte ou un seuil.

## Méthode (rappel)

- Moteur reproductible, graines fixées, personnes fictives, bibliothèque
  standard seulement. Commandes :
  ```sh
  python3 tests.py
  python3 run.py --stage all --out results.json
  python3 analyze.py   # base neutre (k=0) + effet du coup de pouce
  ```
- Recherche par étapes : **grossière** (grille complète, 20 trajectoires),
  **fine** (survivants, pleines trajectoires), **validation** (graines
  réservées, non utilisées pour la sélection).
- Base de comparaison : **k = 0** (poids tous égaux à 1,0) avec les mêmes
  contraintes dures — la base non pondérée appariée.
- Volumes : fine = 50 trajectoires × 500 tirages (horizon long) + 100
  trajectoires × 26 tirages (horizons courts) par scénario. Durée totale
  de l’exécution : ~137 s.

## Résultats

### Étape grossière : 27 survivants sur 72

- **k = 1,5 et k = 2,0 : éliminés partout** — ils échouent au test de
  lissage : après une seule sélection comptabilisée en dernière place,
  le poids dépasse 1,1 (ex. k = 2, lissage n/6 : 1,167).
- **k = 1,0 + lissage n/(n+2) : éliminé** — même raison (1,167 > 1,1).
- Survivants : k = 0,5 (les deux lissages) et k = 1,0 (lissage n/6
  seulement), toutes récence / bornes.

### Contraintes dures : respectées

- **0 tirage en repli secondaire** sur toute l’étape fine (8 scénarios ×
  27 combinaisons). **0 repli de niveau 1** dans les scénarios fins
  (les deux contraintes étaient toujours conjointement réalisables dans
  ces scénarios; le chemin de repli est vérifié par test unitaire).
- **Fidélité de distribution :** distance en variation totale **0,009 à
  0,012 < 0,02** pour tous les survivants (vérification à état fixe,
  20 000 tirages conditionnels).

### Critères principaux vs base neutre (horizon long, 500 tirages)

| Mesure (médiane entre trajectoires) | Base k = 0 | Meilleur (k = 1,0, exp, n/6) | Verdict |
| --- | --- | --- | --- |
| Disparité intra-trajectoire (étendue des parts de première moitié) | 0,076 (p90 0,088) | **0,061** (p90 0,082) | ✅ −20 % |
| Longueur de la plus longue série tardive (médiane) | 12 | **9** | ✅ plus courte |
| Personne « due » (b) : P(première moitié \| 3 places tardives d’affilée) | 0,506 | **0,560** (+5,4 points) | ⚠️ seuil +10 **non atteint** |
| Repli secondaire | 0 | 0 | ✅ |

- **Personne « due » (b) : le seuil proposé de +10 points n’est atteint
  par AUCUNE combinaison** (meilleur : +5,4 points). Le critère (a)
  (séries plus courtes) est respecté. Conformément au plan §7, on ne
  prétend pas que le seuil est respecté : il faut **réviser le seuil**
  (par exemple +5 points) avec Avery et Mira, ou accepter que l’effet
  « due » de la pondération est modeste.
- **Horizons courts (26 tirages) :** disparité médiane **0,269** vs
  0,308 (base); avec absences **0,317** vs 0,359 — l’amélioration est
  présente dès les horizons ordinaires, pas seulement sur 500 tirages.
- **Validation (graines réservées), 2 meilleures combinaisons :**
  disparité médiane **0,066** (fine : 0,061; base : 0,076), série
  médiane 10 (fine : 9; base : 12), due (b) 0,566 — cohérent, pas
  d’effondrement par sur-ajustement.

### Contrôles de cohérence (sanity checks, pas une preuve à eux seuls)

Meilleure combinaison, horizon long, parts moyennes par personne
(regroupées sur 50 trajectoires) : premières places **0,081 à 0,085**
(seuil 0,04–0,13 ✅), première moitié **0,495 à 0,505** (seuil 0,40–0,60
✅). Comme le plan le prévoit, ces moyennes auraient l’air bonnes pour
n’importe quelle règle symétrique — ce sont les mesures
intra-trajectoire ci-dessus qui constituent la preuve.

### Coup de pouce (scénario défini : admissible, sans place réservée, base > 0)

| Facteur | P(première) sans → avec | Augmentation relative | Seuil +10 % à +100 % |
| --- | --- | --- | --- |
| 1,25 | 0,086 → 0,100 | **+16,9 %** | ✅ |
| 1,5 | 0,086 → 0,119 | **+38,4 %** | ✅ |
| 2,0 | 0,086 → 0,153 | **+78,4 %** | ✅ (près du haut de la bande) |

Les trois facteurs respectent la bande proposée. P(première moitié)
passe de 0,506 à 0,576 / 0,638 / 0,732 respectivement.

### Bornes : (0,5 ; 1,5) vs (0,6 ; 1,4) indiscernables

À k = 1,0, les bornes (0,5 ; 1,5) ne contraignent jamais (poids brut
dans [0,5 ; 1,5]) et (0,6 ; 1,4) ne mord presque jamais — les résultats
sont quasi identiques. On recommande les bornes les plus simples.

## Recommandation PROPOSÉE (à approuver, pas adoptée)

- **k = 1,0** — récence **exponentielle** (1,25^i) — lissage **n/6** —
  bornes **(0,5 ; 1,5)**, ratio 3 — **coup de pouce 1,5**.
- Pourquoi celle-ci : meilleure disparité intra-trajectoire (0,061),
  séries plus courtes (9 vs 12), due (b) parmi les meilleures (+5,4
  points), fidélité 0,011 < 0,02, et validée sur graines réservées.
- Pourquoi le coup de pouce 1,5 : +38 % — perceptible sans dominer;
  2,0 (+78 %) frôle le haut de la bande et s’éloigne de « doux ».
- **Point ouvert explicite :** le seuil « due » (b) de +10 points n’est
  pas atteint. Proposition : réviser ce seuil à **+5 points** (avec
  examen) plutôt que de forcer une pondération plus forte qui échouerait
  au test de lissage. À trancher avec Avery et Mira.

## Limites

- Groupes de 12 personnes principalement; petits groupes (2, 3) testés
  à l’étape grossière seulement (0 repli secondaire).
- Le chemin de repli de niveau 1 (protéger la dernière place) est
  vérifié par test unitaire, mais n’a pas été déclenché dans les
  scénarios fins (contraintes toujours conjointement réalisables).
- Scénarios d’anniversaire, priorités et corrections inclus à l’étape
  fine (0 repli secondaire); leurs effets détaillés ne sont pas
  ventilés séparément dans ce premier rapport.
- `results.json` (527 Ko) n’est pas versé dans la demande : il est
  régénérable par les commandes ci-dessus (graines fixées).
