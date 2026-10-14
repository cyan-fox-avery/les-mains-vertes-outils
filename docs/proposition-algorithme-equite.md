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
5. **Vérifier les contraintes** de non-répétition (première / dernière). Si elles sont violées, réparer ou retirer à nouveau, puis appliquer le repli si nécessaire.
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

**Proposition de départ à tester :** plus la moyenne des positions normalisées est élevée (places tardives répétées), plus le poids est élevé — mais avec un **plafond**.

Forme proposée (à simuler, pas adoptée) :

> poids = 1 + k × (moyenne normalisée − 0,5), borné entre 1 et un maximum Wmax

- Une personne dont la moyenne est de 0,5 (milieu de groupe en moyenne) obtient un poids neutre de 1.
- Une personne souvent en fin de liste obtient un poids supérieur à 1.
- Une personne souvent en début de liste obtient un poids inférieur à 1, sans jamais descendre sous le plancher.

**Valeurs de départ à tester (pas adoptées) :** k autour de 1 à 2, Wmax autour de 2 à 3 (personne n’obtient plus de 2 à 3 fois les chances d’une autre). Ces valeurs sont des points de départ pour les simulations, pas des décisions.

**Point ouvert (question 1) :** la forme exacte (linéaire, exponentielle, autre), la force k et le plafond Wmax restent à décider après simulations.

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
- Elle évite les distorsions d’un tirage glouton place par place (où les premiers choix « consomment » les poids et faussent les places suivantes).

**Ce que cette méthode ne fait pas :** elle ne garantit pas à elle seule les règles de non-répétition. C’est l’étape 5 qui les vérifie.

## 7. Étape 5 — Contraintes de non-répétition et repli

### 7.1 Vérification

Après le mélange, vérifier :

- La première personne du tirage n’est pas celle qui était première au tirage pertinent précédent.
- La dernière personne du tirage n’est pas celle qui était dernière au tirage pertinent précédent.

« Tirage pertinent précédent » dépend de la définition de « consécutive » — **point ouvert (question 4)** : tirages du groupe, tirages où la personne était présente, ou semaines civiles consécutives. Le choix change la vérification.

### 7.2 Réparation / nouveau tirage

**Proposition à tester :**

1. Si une seule règle est violée, essayer de **réparer par échange** : échanger la personne fautive avec une autre place, en choisissant un échange qui corrige la violation sans en créer une nouvelle.
2. Sinon, **retirer à nouveau** (nouveau mélange pondéré), jusqu’à un petit nombre d’essais (par exemple, 10 — valeur à tester).
3. Si aucun essai ne satisfait les contraintes, appliquer le **repli** (voir §7.3) et l’indiquer clairement dans l’interface.

**Point ouvert :** le nombre d’essais, la méthode de réparation exacte et la façon d’indiquer le repli à l’équipe restent à décider.

### 7.3 Repli quand les contraintes sont impossibles

Quand il est impossible de respecter les deux règles en même temps (cas particuliers : séance précédente à une seule personne avec au plus deux personnes admissibles au tirage suivant, priorités en conflit — voir `regles-selecteur.md` §5.4), il faut une hiérarchie de repli explicite.

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

1. Formule de pondération : forme, force k, plafond Wmax (question 1).
2. Normalisation exacte des positions, y compris le cas d’une seule personne présente (question 2).
3. Fenêtre d’historique : nombre, tirages du groupe vs tirages assistés, pondération des récents, traitement des nouvelles personnes (question 3).
4. Définition de « consécutive » pour la vérification des contraintes (question 4).
5. Hiérarchie de repli + exemption éventuelle des séances uniques (question 5).
6. Régénération d’un brouillon : permise ou non, journalisée ou non (question 6).
7. Traitement d’une réorganisation manuelle qui crée une répétition (question 8).
8. Plan de simulations : mesures, scénarios, seuils d’acceptation (question 9).
9. Traitement des priorités récurrentes / accommodements dans le calcul d’équité (question 14).
10. Méthode de tirage : la course exponentielle proposée convient-elle, ou préfère-t-on une autre méthode de mélange pondéré?

Tant que ces décisions ne sont pas prises, on ne programme pas l’algorithme. Ce document est une base de discussion et de simulation, pas une spécification finale.
