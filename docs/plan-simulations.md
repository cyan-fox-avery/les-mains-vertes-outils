# Plan de simulations — Valider l’algorithme d’équité avant de le programmer

> **Statut : proposition à approuver.** Ce plan décrit *comment* on validera l’algorithme. **Aucun coefficient n’est adopté ici.** Les seuils ci-dessous sont **proposés** — ils doivent être approuvés par Avery et Mira avant que les simulations servent à trancher quoi que ce soit. Si un seuil proposé ne convient pas, on le corrige dans ce document, pas silencieusement dans les résultats.

## 1. Pourquoi des simulations d’abord

Les règles sont convenues (`regles-selecteur.md`), mais les nombres ne le sont pas : formule de pondération, normalisation, courbe de récence, lissage des courts historiques, valeur du coup de pouce, méthode technique du repli. On ne programme pas l’algorithme avant que les simulations démontrent que les nombres proposés sont à la fois **utiles** (ils corrigent vraiment les désavantages répétés) et **modestes** (ils préservent un vrai hasard, sans rotation déguisée ni avantage écrasant).

Les simulations utilisent uniquement des **personnes fictives** — aucun vrai prénom, aucune vraie donnée de l’atelier.

**Dépendance :** ce plan dépend de la proposition d’algorithme (`docs/proposition-algorithme-equite.md`, demande nº 2, en brouillon) pour la définition de l’algorithme. Les références à ce document visent ce brouillon jusqu’à sa fusion.

## 2. Ce que les simulations doivent trancher

| Paramètre | Question à trancher | Référence |
| --- | --- | --- |
| Forme de la pondération | Linéaire (`1 + k × (moyenne − 0,5)`) ou autre forme douce? | Q1 |
| Force `k`, bornes `Wmin` / `Wmax`, ratio `Wmax / Wmin` | Quelles valeurs corrigent sans exagérer? | Q1 |
| Normalisation des positions | Quelle formule exacte, y compris les très petits groupes? | Q2 |
| Courbe de récence | Quel poids relatif pour chacune des six sélections comptabilisées? | Q3 |
| Lissage des courts historiques | Quelle fonction / échelle pour une influence graduelle? | Q3 |
| Valeur du coup de pouce | Quel multiplicateur unique, doux mais perceptible? | Q18 |
| Méthode du repli + départage | Quelle méthode d’échantillonnage contraint / repli, et quel départage entre ordres également admissibles? | Q5 |

## 3. Méthode

- **Moteur reproductible :** générateur aléatoire avec graine fixée (*seed*) par scénario; même graine → mêmes résultats. Chaque rapport de simulation indique la graine, la version du code et la grille de paramètres testés.
- **Modèle fidèle aux règles :** les simulations appliquent exactement les règles convenues — six sélections **comptabilisées** par personne et par groupe; absences = pause; anniversaire = pause pour la personne fêtée; séance unique = exclue; priorités comptent normalement; coups de pouce = jour courant seulement; seul l’**ordre final enregistré** nourrit l’historique; brouillons écartés jamais comptés; corrections = ordre final corrigé, versions conservées.
- **Tirages vs trajectoires — ne pas confondre les deux :** sur 500 tirages séquentiels, les poids et l’historique évoluent; ces 500 observations sont corrélées, pas indépendantes et identiquement distribuées. Pour l’équité à long terme, on lance **plusieurs trajectoires indépendantes avec graines différentes** (au moins **100 trajectoires de 500 tirages comptabilisés** chacune) et on rapporte la variation **entre les trajectoires** (moyenne + intervalle à 95 % entre trajectoires, par rééchantillonnage *bootstrap* si nécessaire). Pour un état historique fixe, des tirages conditionnels indépendants sont appropriés pour comparer à la distribution exacte.
- **Volume, explicité :** pour les vérifications de fidélité de distribution, au moins **10 000 tirages conditionnels indépendants par état fixe** — à augmenter si l’intervalle de confiance à 95 % est trop large pour trancher; **10 000 ne suffit pas automatiquement** quand l’espace des permutations grandit, le volume est calibré sur la précision exigée, pas supposé. Pour l’équité à long terme : au moins 100 trajectoires × 500 tirages comptabilisés. Pour les horizons courts : au moins 200 trajectoires × 6 / 12 / 26 sélections. Les scénarios courts (petits groupes, cas limites) utilisent l’énumération exacte quand c’est faisable.
- **Groupes indépendants :** chaque groupe du jour simulé a son propre historique; aucune contamination entre groupes.
- **Comparaisons :** chaque paramètre est testé contre une base neutre (aucune pondération, tirage uniforme sous les mêmes contraintes dures) pour isoler l’effet de la pondération.

## 4. Mesures et seuils proposés

Chaque seuil est une **proposition** à approuver. Un paramètre n’est retenu que s’il respecte **tous** les seuils applicables.

### 4.1 Contraintes dures — zéro tolérance

| Mesure | Seuil proposé |
| --- | --- |
| Violations **non intentionnelles** de non-répétition (première / dernière) quand un ordre valide existe | **0** |
| Repli déclenché par épuisement des essais (et non par impossibilité prouvée) | **0** |
| Doublons (une personne deux fois) ou personne manquante dans un ordre | **0** |
| Inclusion accidentelle d’une personne absente au tirage | **0** |
| Deux résultats finaux officiels pour le même jour / date | **0** (hors portée des simulations de tirage, mais vérifié dans les tests d’intégration) |

**Exceptions acceptées, pas des défauts :** les **exceptions manuelles intentionnelles confirmées** (réorganisation qui crée une répétition, avec avertissement + confirmation) et les **places réservées d’anniversaire** sont exclues de la métrique « zéro violation non intentionnelle » — ce sont des exceptions acceptées et enregistrées, pas des défauts de l’algorithme. Elles sont comptées séparément et doivent correspondre exactement aux exceptions enregistrées.

### 4.2 Fidélité de la distribution

| Mesure | Seuil proposé |
| --- | --- |
| Écart entre la distribution simulée et la distribution pondérée conditionnée voulue (petits groupes, énumération exacte) | Distance en variation totale **≤ 0,02** à 95 % de confiance — avec une taille d’échantillon calibrée pour que la demi-largeur de l’intervalle de confiance à 95 % pour la variation totale soit inférieure à 0,02 sur les tailles énumérables; 10 000 tirages est un plancher, pas une garantie automatique |
| Fidélité de la méthode de repli / petits cas | Même seuil; une méthode qui satisfait les contraintes mais fausse la distribution est rejetée comme « exacte » (elle ne peut être retenue que comme approximation explicite, si Avery l’accepte en connaissance de cause) |

### 4.3 Équité à long terme (scénario neutre : groupe stable de 12 personnes, aucune priorité, aucun coup de pouce, aucun anniversaire, présence complète)

**Horizons :** on teste des horizons réalistes de travail, pas seulement un horizon idéalisé. Un horizon de 500 tirages comptabilisés représente environ 9,6 ans à une séance par semaine — il teste la stabilité statistique, mais l’équipe et Maxime doivent voir une équité utile sur des mois ordinaires et sur la conservation proposée de six mois. On teste donc : **court (6 sélections hebdomadaires), moyen (12 et 26 sélections — 26 ≈ six mois), long (500 tirages comptabilisés par trajectoire, au moins 100 trajectoires)**. Pour les horizons courts et moyens, on ajoute des absences périodiques. Les seuils ci-dessous s’appliquent aux **moyennes entre trajectoires** (avec l’écart-type entre trajectoires rapporté), **pas** à une seule trajectoire : on ne déclare pas un échec parce que le bruit stochastique d’une seule trajectoire sort des bandes. Chaque mesure est comparée à une **base neutre non pondérée appariée** (mêmes contraintes dures, tirage uniforme).

**Critères principaux — mesures intra-trajectoire.** Les parts moyennes par personne entre trajectoires ne suffisent pas comme preuve principale : si tout le monde commence symétriquement et subit les mêmes règles, l’échangeabilité des étiquettes garantit que l’espérance de chaque personne est ≈ 1/12 (premières places) et ≈ 1/2 (première moitié), même pour des stratégies de pondération trop fortes, trop faibles ou très irrégulières. Agréger les moyennes par nom sur de nombreuses graines garantirait presque les larges bandes, tout en masquant l’inéquité *au sein de l’historique d’une vraie équipe*. Les mesures ci-dessous sont donc les critères principaux : chacune est calculée **à l’intérieur d’une trajectoire**, puis on rapporte sa distribution (médiane, 90e percentile) sur les trajectoires indépendantes, comparée à une base non pondérée appariée (mêmes contraintes dures).

| Mesure (critère principal) | Seuil proposé |
| --- | --- |
| Disparité intra-trajectoire : étendue (max − min) des parts de places en première moitié par personne, **dans une même trajectoire** — médiane et 90e percentile sur les trajectoires | **Médiane ≤ médiane de la base appariée**, et **90e percentile ≤ 90e percentile de la base appariée** (la pondération resserre la disparité réelle au sein d’une équipe) |
| Disparité intra-trajectoire : étendue (max − min) du rang normalisé moyen par personne, dans une même trajectoire — médiane et 90e percentile | **Médiane ≤ médiane de la base appariée** |
| Longueur extrême de série tardive : plus longue série de places en deuxième moitié par personne et par trajectoire — 90e percentile sur les trajectoires | **Plus courte qu’avec la base appariée** |
| Personne « due » — (a) longueur moyenne de la plus longue série de places en deuxième moitié par trajectoire, pondéré vs base non pondérée appariée | **Plus courte** avec pondération |
| Personne « due » — (b) P(première moitié au prochain tirage \| 3 places consécutives en deuxième moitié), pondéré vs base non pondérée appariée | **Supérieure d’au moins 10 points de pourcentage** avec pondération |

**Contrôles de cohérence (sanity checks, pas une preuve suffisante à eux seuls) :**

| Mesure | Seuil proposé |
| --- | --- |
| Part de premières places par personne (moyenne entre trajectoires) | Chacune entre **4 % et 13 %** (attendu neutre ≈ 8,3 %) |
| Part de places en première moitié par personne (moyenne entre trajectoires) | Chacune entre **40 % et 60 %** (attendu neutre 50 %) |
| Ratio avantage max / min (parts de premières places, moyennes entre trajectoires) | **≤ 2** |

**Pourquoi pas « ≥ 80 % en première moitié dans les 5 prochains » :** pour un tirage neutre 50/50 sans contrainte, le hasard pur donne déjà P(au moins une première moitié dans les 5 prochains) = 1 − (1/2)⁵ = **96,875 %**. Un tel seuil ne démontrerait pas que la pondération aide. La comparaison contre la base appariée et les mesures (a)–(b) testent une amélioration réelle. **Aucun délai déterministe de récupération n’est promis.**

### 4.4 Douceur — la pondération corrige sans dominer

| Mesure | Seuil proposé |
| --- | --- |
| Poids d’une personne après **une seule** sélection comptabilisée (lissage) | Reste dans **[0,9 ; 1,1]** (pas d’ajustement plein régime après un seul tirage) |
| Contribution de la sélection comptabilisée la plus récente au poids total (récence, **fenêtre complète de six sélections uniquement**) | **≤ 30 %** (un seul jour ne domine pas l’historique) |
| Écart entre la personne la plus avantagée et la plus désavantagée en probabilité de première place, à historique égal sauf un tirage | **≤ 2×** — mesuré sur les **poids de base sans contrainte** (pour isoler l’effet de la pondération; ce ratio est toujours défini). En complément, le ratio des probabilités conditionnelles de première place est mesuré **uniquement entre personnes ayant la même admissibilité à la première place, sans place réservée de priorité / anniversaire, et avec une probabilité de base positive** — sans ce cadrage, la règle dure de non-répétition rendrait le ratio indéfini (division par zéro) ou infiniment grand, quelle que soit la douceur de la pondération. Les tests de non-répétition restent stricts et séparés (§4.1). |

**Historiques courts :** le plafond de 30 % sur la contribution de la sélection la plus récente **ne s’applique que si la fenêtre complète de six sélections existe**. Pour 1, 2 ou 3 sélections comptabilisées, il est mathématiquement impossible : si les contributions sont normalisées sur les seuls éléments observés, la plus récente reçoit nécessairement ≥ 1/n (et davantage avec une pondération de récence). Les courts historiques sont évalués par le test de lissage séparé (poids dans [0,9 ; 1,1] après une seule sélection), pas par le plafond de 30 %.

### 4.5 Coup de pouce (scénario standard : groupe de 12, une personne avec coup de pouce, les autres sans)

| Mesure | Seuil proposé |
| --- | --- |
| Probabilité de première place de la personne avec coup de pouce, vs sa probabilité sans coup de pouce — **dans un scénario de comparaison précisément défini : personne admissible à la première place (non exclue par la règle de non-répétition), aucune place réservée d’anniversaire ou de priorité, probabilité de base > 0** | Augmentation relative entre **+10 % et +100 %** (soit 1,1× à 2×) — perceptible, mais pas déterminant |
| Probabilité de première moitié de la personne avec coup de pouce, vs sans (même scénario) | **Amélioration mesurable** (métrique complémentaire, pas seulement la première place) |
| Coup de pouce + contraintes dures | Testé séparément : quand la personne ne peut pas être première (non-répétition, place réservée), le coup de pouce **ne contourne jamais** les règles; les règles de non-répétition et les priorités / anniversaires **priment toujours** |
| Toutes les personnes avec le même coup de pouce | Probabilités relatives **inchangées** (à la tolérance statistique près) — un coup de pouce universel est neutre |
| Coup de pouce annulé avant le tirage | **Aucun effet** (non compté comme actif) |

**Note :** sans ce cadrage, le seuil « +10 % à +100 % » serait vide de sens : si un anniversaire ou une priorité réserve déjà la première place, ou si la personne avec coup de pouce est inéligible à la première place, la probabilité de base peut être **zéro** (ratio 0/0 sans signification).

### 4.6 Cas limites

| Cas | Attendu |
| --- | --- |
| Petits groupes (2, 3 personnes) | Contraintes respectées quand c’est possible; repli hiérarchique vérifié (protéger la dernière place d’abord) |
| Séance précédente à une seule personne | Aucun effet sur la pondération ni sur les contraintes du tirage suivant |
| Anniversaire | Personne fêtée première (ou 1–2 pour deux anniversaires); pause d’historique vérifiée; réorganisation hors des places réservées → exemption annulée; anniversaire absent → « Absent(e) au tirage », aucun rattrapage |
| Corrections | Ordre corrigé utilisé pour la suite; versions antérieures conservées; aucune réécriture rétroactive |
| Personne qui revient après une longue absence | Historique restauré (six dernières sélections comptabilisées + séquence première / dernière) |

## 5. Scénarios à simuler

1. **Groupe habituel :** 10–15 personnes, présence complète, 500 tirages comptabilisés.
2. **Absences fréquentes :** chaque personne absente ~20 % des jours, certaines absentes plusieurs semaines d’affilée; vérifier que les pauses fonctionnent et que personne n’est pénalisé pour absence.
3. **Très petits groupes :** 2 et 3 personnes, y compris après une séance à une seule personne.
4. **Priorités fréquentes :** dont une personne prioritaire récurrente; vérifier que les priorités comptent normalement et que le système ne crée pas d’avantage cumulatif caché.
5. **Nouvelle personne :** arrivée dans un groupe avec historique; vérifier le lissage (influence graduelle) et que les règles dures s’appliquent dès la première sélection comptabilisée.
6. **Modifications manuelles du brouillon :** réorganisations, y compris celles qui créent une répétition (exception manuelle enregistrée, résultat réel compté).
7. **Anniversaires :** (a) personne fêtée première; (b) sa place ne modifie ni son poids futur ni sa séquence des extrêmes; (c) les positions réelles des autres continuent de compter; (d) re-tirage / annulation sans historique fantôme; (e) anniversaire avant les priorités (2 anniversaires + 3 priorités → 1–2 anniversaire, 3–5 priorités); (f) personne fêtée déplacée hors des places réservées → exemption annulée; (g) personne fêtée absente → aucun rattrapage.
8. **Coups de pouce :** effet le jour même seulement, sans option permanente; plusieurs coups de pouce égaux; toutes les personnes avec un coup de pouce → neutre; coup de pouce annulé avant le tirage → non compté.
9. **Corrections :** toutes les versions antérieures conservées, ordre corrigé utilisé pour la suite, aucune réécriture rétroactive, aucune limite de temps.
10. **Hiérarchie de repli :** impossibilité conjointe → protéger la non-répétition de la dernière place; même celle-ci impossible → repli secondaire documenté + avis clair.
11. **Récence + lissage :** un tirage malchanceux unique, un tirage chanceux unique, absences; influence graduelle d’un nouvel historique.
12. **Personne qui revient :** réadmission après une longue absence; historique restauré, pas de réinitialisation silencieuse.

## 6. Grille de paramètres à tester

Valeurs de départ **à tester**, pas adoptées :

- **Forme :** linéaire `poids = 1 + k × (moyenne − 0,5)`; variantes douces si la linéaire échoue aux seuils.
- **`k` :** 0,5 · 1 · 1,5 · 2.
- **Bornes :** `(Wmin, Wmax)` = (0,5 ; 1,5) · (0,6 ; 1,4) · (0,75 ; 1,25); le ratio `Wmax / Wmin` est la quantité bornée, pas `Wmax` seul.
- **Récence :** pondération égale (référence) · décroissance linéaire douce · décroissance exponentielle douce — avec la contrainte que la sélection la plus récente contribue ≤ 30 %.
- **Lissage :** influence = `n / 6` (linéaire) · influence = `n / (n + 2)` (progressive) · autres formes douces — où `n = min(nombre de sélections comptabilisées, 6)`, **plafonné à la fenêtre glissante de six entrées**, pour que l’influence ne dérive pas vers le haut simplement parce qu’une personne travaille depuis des années.
- **Coup de pouce :** multiplicateur 1,25 · 1,5 · 2.
- **Méthode du repli :** acceptation / rejet (référence) · énumération directe (petits groupes) · méthode contrainte proposée (à valider sur la fidélité de distribution).

## 7. Recherche par étapes et règle de décision

**Recherche par étapes (budget maîtrisé) :** le produit des paramètres est grand et l’échantillonnage contraint coûte cher. On procède donc par étapes :
1. **Exploration grossière :** grille complète avec peu de trajectoires (par exemple, 20 trajectoires / horizons courts) pour éliminer les candidats clairement défaillants.
2. **Affinage :** candidats survivants, avec les pleines trajectoires.
3. **Validation indépendante :** les paramètres recommandés doivent respecter les seuils sur un **ensemble de validation réservé** — graines et scénarios frais, non utilisés pour la sélection. On sépare l’exploration de la validation finale pour ne pas sur-ajuster (*overfitting*) en choisissant les coefficients contre les mêmes tirages aléatoires.
4. **Budget :** le nombre total de tirages simulés et le temps de calcul sont plafonnés et indiqués dans le rapport; l’énumération directe sert aux petits groupes; la grille est réduite si l’échantillonnage contraint devient trop coûteux.

**Règle de décision :**

1. **Choisir les paramètres les plus doux** qui respectent tous les seuils applicables **sur l’ensemble de validation**. En cas d’égalité, préférer la forme la plus simple à expliquer.
2. **Si aucun jeu de paramètres ne respecte tous les seuils,** le rapport le dit explicitement : on revoit les seuils (avec Avery et Mira) ou les règles — on ne relâche **jamais** silencieusement une contrainte dure pour faire passer un résultat.
3. **Si un seuil proposé s’avère inadapté,** on le corrige dans ce plan (avec approbation), on ne l’ignore pas dans les résultats.
4. **Aucun coefficient n’est adopté** tant que le rapport de simulation n’est pas approuvé par Avery et Mira.

## 8. Livrables

- **Rapport de simulation** par scénario : paramètres testés, mesures observées, seuils respectés / non respectés, intervalles de confiance, graines utilisées.
- **Recommandation** : le jeu de paramètres retenu + pourquoi (avec les résultats qui l’appuient), ou la mention explicite qu’aucun jeu ne satisfait tous les seuils.
- **Reproductibilité :** code de simulation versionné, graines publiées dans le rapport, instructions pour relancer les mêmes simulations.

## 9. Ce que ce plan ne décide pas

- Aucun coefficient, aucune courbe, aucune valeur de coup de pouce.
- Aucun seuil définitif (les seuils ci-dessus sont proposés).
- Aucun fournisseur, aucune base de données, aucun schéma d’authentification, aucune région d’hébergement.
- Aucune approbation de Maxime (accès partagé, conservation) — voir `docs/decisions-pour-maxime.md`.
