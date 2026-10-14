# Proposition d’algorithme d’équité — Document de discussion

> **Statut : proposition à discuter. Rien n’est décidé ici.**
>
> Ce document propose une façon concrète de réaliser l’équité décrite dans `regles-selecteur.md`, pour que Avery et Mira puissent en discuter et la tester par simulations avant tout choix définitif. Chaque paramètre chiffré ci-dessous est une **valeur de départ à tester**, pas une règle adoptée. Les questions ouvertes correspondantes (`questions-ouvertes.md`) sont citées à chaque étape — elles ne sont pas tranchées ici.

## 1. Rappel : ce que l’algorithme doit faire

D’après les règles convenues :

- Chaque personne admissible apparaît **exactement une fois** dans l’ordre.
- **Pas deux fois première de suite**, **pas deux fois dernière de suite**, quand c’est mathématiquement possible.
- Les personnes qui ont reçu **à répétition des places tardives** obtiennent **un peu plus de chances** d’avoir des places plus hâtives — un équilibrage **doux**, jamais une rotation.
- Les positions historiques sont **normalisées selon la taille du groupe**.
- L’équité se calcule **séparément pour chaque groupe du jour**.
- Seul le **résultat final enregistré** compte pour l’équité future.
- Les **priorités manuelles** (max 3, places 1–3) sont appliquées avant le tirage aléatoire et comptent quand même dans l’historique.
- Les **absences** ne pénalisent pas : une absence ne compte ni comme une place ni comme une mauvaise place.

## 2. Vue d’ensemble de la proposition

En six étapes, pour chaque tirage :

1. **Déterminer les personnes admissibles** (présentes, moins les priorités).
2. **Placer les priorités** aux places 1–3, avec avertissement si une priorité répète la première place.
3. **Calculer un poids** pour chaque personne restante, à partir de son historique de places normalisées.
4. **Tirer un ordre pondéré** en une seule fois (mélange pondéré), pas un choix glouton place par place.
5. **Vérifier les contraintes** de non-répétition (première / dernière) : d’abord déterminer explicitement si un ordre valide existe; si oui, échantillonner dans la distribution pondérée conditionnée au respect des contraintes (voir §7.2); le repli ne s’applique que s’il n’existe vraiment aucun ordre valide ou lors d’une dérogation manuelle explicitement autorisée.
6. **Présenter l’ordre comme brouillon.** L’équipe peut le modifier; seul le résultat final enregistré nourrit l’historique.

## 3. Étape 1 — Personnes admissibles

- Partir de la liste du groupe du jour.
- Retirer les personnes **absentes au tirage**.
- Retirer les personnes **prioritaires** (elles seront placées à l’étape 2).
- Les personnes restantes sont celles que l’algorithme place par hasard pondéré.

## 4. Étape 2 — Priorités

- Placer les priorités aux places 1, 2, 3 selon l’ordre indiqué (voir `regles-selecteur.md` §6).
- Si une priorité placerait quelqu’un en première place pour une deuxième fois consécutive : **avertissement + dérogation explicite**, comme convenu.
- Les places prioritaires comptent dans l’historique d’équité, comme convenu.
- **Point ouvert (question 14) :** si une personne reçoit souvent des priorités pour un accommodement récurrent, ses places prioritaires comptent-elles exactement comme les autres dans le calcul, ou sont-elles signalées / traitées différemment? Cette proposition ne tranche pas — elle suppose pour l’instant le traitement « tout compte pareil », à discuter, parce que l’autre traitement changerait le calcul.

## 5. Étape 3 — Poids à partir de l’historique (proposition à tester)

### 5.1 Position normalisée

Pour chaque tirage passé d’une personne, on convertit sa place en une valeur entre 0 (première) et 1 (dernière) :

> position normalisée = (place − 1) / (nombre de personnes présentes − 1)

Exemples : 1re sur 12 → 0. 12e sur 12 → 1. 6e sur 11 → 0,5. 10e sur 14 → environ 0,69.

**Point ouvert (question 2) :** cette formule est la proposition de départ. Une autre normalisation (percentile, autre ajustement pour les très petits groupes) reste possible. Le cas d’une seule personne présente (division par zéro) doit être traité explicitement : une séance à une personne ne produit pas de position normalisée utilisable.

### 5.2 Fenêtre d’historique

**Proposition de départ à tester :** la moyenne des positions normalisées sur environ les **six derniers tirages auxquels la personne a assisté**.

**Points ouverts (question 3) :**

- Le nombre exact (6? autre chose?).
- Tirages du groupe vs tirages où la personne était présente.
- Pondération égale pour chaque tirage de la fenêtre, ou plus de poids aux tirages récents?
- Nouvelle personne sans historique : poids neutre (voir §5.4).

### 5.3 Conversion en poids

**Proposition de départ à tester :** plus la moyenne des positions normalisées est élevée (places tardives répétées), plus le poids est élevé — mais avec un **plancher et un plafond choisis indépendamment**.

Forme proposée (à simuler, pas adoptée) :

> poids = 1 + k × (moyenne normalisée − 0,5), borné entre Wmin et Wmax

avec Wmin dans ]0, 1[ (plancher) et Wmax > 1 (plafond), choisis indépendamment l’un de l’autre.

- Une personne dont la moyenne est de 0,5 (milieu de groupe en moyenne) obtient un poids neutre de 1.
- Une personne souvent en fin de liste obtient un poids supérieur à 1, sans jamais dépasser Wmax.
- Une personne souvent en début de liste obtient un poids inférieur à 1, sans jamais descendre sous Wmin.
- La borne porte sur le **ratio Wmax / Wmin** (le rapport entre le poids le plus élevé et le poids le plus faible possibles), pas sur Wmax seul. C’est ce ratio qui limite l’écart relatif entre les poids.

**Valeurs de départ à tester (pas adoptées) :** k autour de 1 à 2; Wmin et Wmax choisis de façon que le ratio Wmax / Wmin soit autour de 2 à 3 (par exemple, Wmin = 0,5 et Wmax = 1,5, ratio 3). Ces valeurs sont des points de départ pour les simulations, pas des décisions.

**Limite à ne pas surpromettre :** le ratio Wmax / Wmin borne le rapport entre les poids, pas le rapport entre les probabilités réelles d’obtenir la première place. Les contraintes dures (éligibilité, non-répétition, priorités) modifient les probabilités réalisées. On ne promet donc pas un ratio de probabilités inconditionnel.

**Point ouvert (question 1) :** la forme exacte (linéaire, exponentielle, autre), la force k, le plancher Wmin et le plafond Wmax restent à décider après simulations.

### 5.4 Nouvelle personne

**Proposition de départ :** une personne sans historique (ou avec trop peu d’historique) commence avec un **poids neutre**, sans avantage ni désavantage. Son historique se construit au fil de ses tirages.

**Point ouvert :** à partir de combien de tirages son historique compte-t-il « pleinement »? Faut-il lisser ses premiers tirages pour éviter qu’un seul mauvais tirage fausse son poids? À discuter.

## 6. Étape 4 — Mélange pondéré (tirage en une seule fois)

**Proposition :** utiliser un **mélange pondéré par course exponentielle** (méthode d’Efraimidis et Spirakis, dite A-ES) :

1. Pour chaque personne restante, tirer un nombre aléatoire uniforme U entre 0 et 1 (exclu).
2. Calculer une clé : clé = U^(1 / poids).
3. Trier les personnes par clé décroissante. Cet ordre est le tirage.

**Pourquoi cette méthode (à discuter) :**

- Elle produit un ordre complet en une seule fois, où chaque personne apparaît exactement une fois.
- Elle respecte les poids : une personne avec un poids plus élevé a plus de chances de sortir tôt, mais rien n’est garanti.
- Elle est pratique à programmer : un seul passage, sans renormalisation itérative.

**Équivalence à ne pas perdre de vue :** tirer chaque place l’une après l’autre, avec une probabilité proportionnelle aux poids des personnes encore restantes (tirage séquentiel pondéré sans remise, correctement renormalisé), produit **la même distribution** que la course exponentielle — la distribution dite de Plackett-Luce. La course exponentielle n’évite donc aucune « distorsion » propre au tirage séquentiel : les deux méthodes sont deux implémentations de la même distribution. Le choix entre les deux est une question de commodité d’implémentation, pas de justesse mathématique.

**Ce que cette méthode ne fait pas :** elle ne garantit pas à elle seule les règles de non-répétition. C’est l’étape 5 qui les vérifie.

## 7. Étape 5 — Contraintes de non-répétition et repli

### 7.1 Vérification

Après le mélange, vérifier :

- La première personne du tirage n’est pas celle qui était première au tirage pertinent précédent.
- La dernière personne du tirage n’est pas celle qui était dernière au tirage pertinent précédent.

« Tirage pertinent précédent » dépend de la définition de « consécutive » — **point ouvert (question 4)** : tirages du groupe, tirages où la personne était présente, ou semaines civiles consécutives. Le choix change la vérification.

### 7.2 Faisabilité d’abord, puis échantillonnage conditionné

**Base testable proposée :**

1. **Déterminer explicitement si un ordre valide existe.** Avant tout tirage, vérifier s’il existe au moins un ordre qui respecte les contraintes dures (places prioritaires, non-répétition de la première / dernière, éligibilité). Cette vérification porte sur l’existence d’un ordre valide, pas sur le résultat d’un nombre limité d’essais.
2. **Si un ordre valide existe : échantillonner dans la distribution pondérée conditionnée au respect des contraintes.** Par exemple, par acceptation / rejet : tirer un mélange pondéré, le garder s’il respecte les contraintes, sinon retirer à nouveau — jusqu’à obtenir un ordre valide. L’acceptation / rejet échantillonne correctement la distribution conditionnée, quel que soit le nombre d’essais nécessaires.
3. **Prévoir une solution toujours correcte pour les petits cas ou les cas à faible taux d’acceptation.** L’acceptation / rejet peut prendre longtemps si les ordres valides sont très rares. Pour ces cas, prévoir une autre méthode exacte (par exemple, énumération directe pour les très petits groupes, ou échantillonnage conditionné correctement pondéré). À discuter et à tester.

**Ce que « exacte » veut dire ici — deux propriétés à tester séparément :**

- **(a) Contraintes respectées :** chaque ordre produit respecte bien toutes les contraintes dures (places prioritaires, non-répétition, éligibilité).
- **(b) Distribution non faussée :** les probabilités relatives des ordres valides correspondent bien à la distribution pondérée conditionnée voulue — on ne modifie pas subrepticement les chances en choisissant une méthode plus rapide.

Une construction contrainte générique peut satisfaire (a) tout en violant (b) : elle produit toujours des ordres valides, mais change leurs probabilités relatives. Une telle méthode ne doit pas être présentée comme mathématiquement équivalente à l’échantillonnage conditionné. Elle ne peut être retenue comme approximation explicite que si Avery l’accepte après simulations, en connaissant ce qu’elle sacrifie.

**Ce que cette base exclut, et pourquoi :**

- **Pas de réparation par échange arbitraire.** Échanger des places après coup pour corriger une violation modifie la pondération voulue de façon difficile à prévoir. On n’utilise pas d’échange comme méthode de réparation sans une analyse propre de son effet sur la distribution.
- **Pas de repli au motif que « N essais ont échoué ».** Un nombre fini d’essais infructueux ne prouve pas l’impossibilité. Le repli ne s’applique que lorsqu’il n’existe vraiment aucun ordre valide (voir §7.3) ou lors d’une dérogation manuelle explicitement autorisée (par exemple, dérogation de priorité, ou exception manuelle selon la question 8).

**Point ouvert :** la méthode exacte de vérification de faisabilité, la méthode exacte pour les cas à faible taux d’acceptation, et la façon d’indiquer un repli à l’équipe restent à décider.

### 7.3 Repli quand les contraintes sont impossibles

Quand il n’existe vraiment aucun ordre valide (cas particuliers : séance précédente à une seule personne avec au plus deux personnes admissibles au tirage suivant, priorités en conflit — voir `regles-selecteur.md` §5.4), il faut une hiérarchie de repli explicite. Le repli ne se déclenche jamais au simple motif qu’un nombre limité d’essais a échoué.

**Point ouvert (question 5) :** laquelle relâcher en premier? Options déjà listées (dernière d’abord, première d’abord, les deux avec pondération seulement, tirage parmi les ordres qui violent le moins de règles). **Aucune hiérarchie n’est choisie ici.** Il faut aussi décider si les séances à une seule personne sont exemptées des contraintes de positions consécutives.

### 7.4 Exception manuelle

Si l’équipe **modifie manuellement** l’ordre (brouillon) de façon à créer une répétition de première ou de dernière place, le traitement (avertissement, confirmation, enregistrement de l’exception) est une **question ouverte (question 8)**. La proposition ne choisit pas : l’application ne doit pas traiter silencieusement une exception manuelle comme un résultat aléatoire conforme.

## 8. Étape 6 — Brouillon et résultat final

- L’ordre produit est un **brouillon**, comme convenu.
- L’équipe peut le modifier, puis **enregistrer le résultat final**.
- **Seul le résultat final enregistré** nourrit l’historique d’équité des tirages suivants.
- Un brouillon non enregistré ne compte pas. Une régénération éventuelle d’un brouillon est régie par la **question ouverte 6** (permise ou non, dans quelles circonstances, journalisée ou non).

## 9. Simulations : comment valider avant de décider

**Proposition de plan de test (question 9) :** avant d’adopter une formule, la tester par simulations, sans supposer qu’elle fonctionne.

**Mesures à suivre (proposées) :**

- Distribution des places sur plusieurs centaines de tirages simulés : chaque personne obtient-elle, à long terme, une part équitable de bonnes et de moins bonnes places?
- Taux de répétition première / dernière : les règles de non-répétition sont-elles respectées quand c’est possible?
- Non-relâchement : vérifier que les contraintes ne sont jamais relâchées au simple motif qu’un nombre limité d’essais a échoué — le repli ne doit se produire que lorsqu’il n’existe vraiment aucun ordre valide.
- Fidélité de la distribution : vérifier que la méthode retenue pour les cas à faible taux d’acceptation préserve les probabilités relatives de la distribution pondérée conditionnée (propriété b, §7.2), et pas seulement la validité des ordres (propriété a).
- Temps d’attente : combien de tirages faut-il, en moyenne, pour qu’une personne « due » obtienne une bonne place?
- Écart entre la personne la plus avantagée et la plus désavantagée : l’écart reste-t-il borné, ou une personne accumule-t-elle un avantage?
- Effet des priorités : que se passe-t-il quand une personne reçoit souvent des priorités?

**Scénarios à simuler (proposés) :**

- Groupes habituels de 10–15 personnes, présence complète.
- Absences fréquentes, personnes qui manquent plusieurs semaines.
- Très petits groupes (2, 3 personnes) et séance précédente à une personne.
- Priorités fréquentes (dont une personne prioritaire récurrente).
- Nouvelle personne qui arrive dans un groupe avec historique.
- Tirages avec modifications manuelles du brouillon.

**Seuils d’acceptation :** à définir avec Avery et Mira avant de considérer l’algorithme acceptable. Tant que les simulations ne sont pas faites, la pondération reste une hypothèse, pas une garantie.

## 10. Liste des décisions à prendre (pour la discussion)

1. Formule de pondération : forme, force k, plancher Wmin, plafond Wmax, et ratio Wmax / Wmin (question 1).
2. Normalisation exacte des positions, y compris le cas d’une seule personne présente (question 2).
3. Fenêtre d’historique : nombre, tirages du groupe vs tirages assistés, pondération des récents, traitement des nouvelles personnes (question 3).
4. Définition de « consécutive » pour la vérification des contraintes (question 4).
5. Hiérarchie de repli + exemption éventuelle des séances uniques (question 5).
6. Régénération d’un brouillon : permise ou non, journalisée ou non (question 6).
7. Traitement d’une réorganisation manuelle qui crée une répétition (question 8).
8. Plan de simulations : mesures, scénarios, seuils d’acceptation (question 9).
9. Traitement des priorités récurrentes / accommodements dans le calcul d’équité (question 14).
10. Méthode de tirage et d’application des contraintes : la course exponentielle et le tirage séquentiel pondéré produisent la même distribution (Plackett-Luce) — le choix est une question d’implémentation. Pour les contraintes : la base « faisabilité explicite + échantillonnage conditionné (acceptation / rejet + solution exacte pour petits cas ou faible taux d’acceptation) » convient-elle comme base testable?

Tant que ces décisions ne sont pas prises, on ne programme pas l’algorithme. Ce document est une base de discussion et de simulation, pas une spécification finale.
