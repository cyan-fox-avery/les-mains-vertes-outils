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
- Les **priorités manuelles** (max 3) sont appliquées avant le tirage aléatoire et comptent quand même dans l’historique. En l’absence d’anniversaires, elles occupent les places 1–3; si le mode anniversaire est actif, les personnes fêtées occupent les premières places et les priorités suivent (voir §4).
- Les **absences** ne pénalisent pas : une absence ne compte ni comme une place ni comme une mauvaise place.

**Décisions confirmées 2026-10-14 (Avery) intégrées à la proposition — paramètres mathématiques toujours à valider par simulations :**

- **Absences = pause :** pour les règles de non-répétition, on compare les **deux dernières sélections comptabilisées** de la personne, dans le groupe du jour. Une semaine d’absence ne réinitialise ni ne fait avancer la séquence de la personne et ne fournit aucune position. Une séance à une seule personne peut être enregistrée comme événement, mais sa première/dernière place inévitable est **exclue de la pondération d’équité et de la contrainte des extrêmes consécutifs**.
- **Fenêtre d’historique : six dernières sélections comptabilisées dans l’historique d’équité de cette personne**, par groupe du jour (six sélections comptabilisées, pas six semaines civiles : seules les sélections ordinaires participées comptent).
- **Priorités comptent normalement :** toute place prioritaire compte pleinement dans l’historique, avec sa provenance manuelle enregistrée. Aucune catégorie d’accommodement, aucun champ de raison médicale, aucune exclusion spéciale.
- **Pause anniversaire :** la place de première obtenue en mode anniversaire est exclue de la fenêtre de pondération et de la séquence des extrêmes consécutifs de la personne fêtée; les autres personnes comptent normalement (voir §5.5).
- **Ajustements manuels des chances (coups de pouce) : strictement le jour courant seulement, sans option permanente** (voir §5.6). Ce ne sont pas des priorités : ils changent les chances, ils n’attribuent pas de place garantie.
- **Re-tirage :** possible avant la révélation, avec confirmation obligatoire « Êtes-vous sûr(e)? »; après le début de la sélection, corrections manuelles explicites. Les propositions écartées n’entrent **jamais** dans l’historique d’équité.
- **Corrections :** version antérieure conservée, correction enregistrée; l’ordre corrigé sert aux calculs futurs; pas de nouveau tirage rétroactif des séances passées. Une réorganisation manuelle qui crée une répétition première/dernière déclenche un avertissement + confirmation, puis est conservée comme exception manuelle, le résultat réel comptant quand même.

## 2. Vue d’ensemble de la proposition

En six étapes, pour chaque tirage :

1. **Déterminer les personnes admissibles** (présentes, moins les priorités).
2. **Placer les anniversaires d’abord** (places réservées), **puis les priorités** aux places suivantes (en l’absence d’anniversaires : places 1–3), avec avertissement si une priorité répète la première place.
3. **Calculer un poids** pour chaque personne restante, à partir de son historique de places normalisées.
4. **Tirer un ordre pondéré** en une seule fois (mélange pondéré), pas un choix glouton place par place.
5. **Vérifier les contraintes** de non-répétition (première / dernière) : d’abord déterminer explicitement si un ordre valide existe; si oui, échantillonner dans la distribution pondérée conditionnée au respect des contraintes (voir §7.2); le repli ne s’applique que s’il n’existe vraiment aucun ordre valide ou lors d’une dérogation manuelle explicitement autorisée.
6. **Présenter l’ordre comme brouillon.** L’équipe peut le modifier; seul le résultat final enregistré nourrit l’historique.

## 3. Étape 1 — Personnes admissibles

- Partir de la liste du groupe du jour.
- Retirer les personnes **absentes au tirage**.
- Retirer les personnes **fêtées** (mode anniversaire, placées d’abord à l’étape 2) et les personnes **prioritaires** (placées ensuite à l’étape 2).
- Les personnes restantes sont celles que l’algorithme place par hasard pondéré.

## 4. Étape 2 — Anniversaires, puis priorités

- **Anniversaires d’abord (décision confirmée) :** placer les personnes fêtées aux premières places, AVANT les priorités ordinaires. Un anniversaire : place 1. Deux anniversaires : places 1–2, ordre aléatoire entre elles. Les anniversaires **s’ajoutent** à la limite de trois priorités ordinaires, ils n’y sont pas inclus (deux anniversaires + trois priorités : places 1–2 anniversaire, places 3–5 priorités). La sélection simultanée anniversaire / priorité de la même personne et les cas avec plus de places spéciales que de personnes présentes sont des détails explicites de validation de l’interface.
- Placer ensuite les priorités ordinaires selon l’ordre indiqué (voir `regles-selecteur.md` §6).
- **Personne prioritaire absente (décision confirmée) :** retirer automatiquement cette personne de la liste des priorités du jour, en gardant l’ordre des autres et en resserrant les places. Son historique se met en pause, aucune priorité reportée.
- Si une priorité placerait quelqu’un en première place pour une deuxième fois consécutive : **avertissement + dérogation explicite**, comme convenu.
- Les places prioritaires comptent dans l’historique d’équité, comme convenu.
- **Décision confirmée (question 14, résolue) :** les places prioritaires comptent exactement comme les autres (« tout compte pareil »). Aucune catégorie d’accommodement, aucun champ de raison médicale, aucune exclusion spéciale. Cette proposition applique ce traitement.

## 5. Étape 3 — Poids à partir de l’historique (proposition à tester)

### 5.1 Position normalisée

Pour chaque tirage passé d’une personne, on convertit sa place en une valeur entre 0 (première) et 1 (dernière) :

> position normalisée = (place − 1) / (nombre de personnes présentes − 1)

Exemples : 1re sur 12 → 0. 12e sur 12 → 1. 6e sur 11 → 0,5. 10e sur 14 → environ 0,69.

**Point ouvert (question 2) :** cette formule est la proposition de départ. Une autre normalisation (percentile, autre ajustement pour les très petits groupes) reste possible. Le cas d’une seule personne présente (division par zéro) doit être traité explicitement : une séance à une personne ne produit pas de position normalisée utilisable.

### 5.2 Fenêtre d’historique

**Décision confirmée :** la moyenne des positions normalisées sur les **six dernières sélections comptabilisées dans l’historique d’équité de cette personne**, par groupe du jour. Six sélections comptabilisées, pas nécessairement six semaines civiles : seules les sélections ordinaires participées comptent; une absence, une sélection d’anniversaire (pour la personne fêtée) et une séance à une seule personne ne font pas avancer la fenêtre.

**Récence (décision confirmée) :** les sélections comptabilisées plus récentes ont une influence légèrement plus grande que les plus anciennes dans la fenêtre de six. Décroissance douce : les six contribuent. La récence reflète l’ordre des six dernières sélections comptabilisées, pas les semaines civiles écoulées pendant les pauses.

**Courts historiques (décision confirmée) :** l’influence de l’historique propre d’une nouvelle personne augmente graduellement à mesure que ses sélections comptabilisées s’accumulent (voir §5.4). Une seule première ou dernière place ne produit pas un ajustement à pleine force.

**Points toujours ouverts (question 3) :** poids relatifs / courbe exacts de la récence; fonction / échelle exactes de lissage; seuils d’acceptation des simulations pour la récence + le lissage ensemble.

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

**Point ouvert (question 1) :** la forme exacte (linéaire, exponentielle, autre), la force k, le plancher Wmin et le plafond Wmax restent à décider après simulations. La formule finale doit aussi intégrer les composantes décidées : moyenne pondérée par la récence douce, facteur de lissage des courts historiques, et coup de pouce positif unique éventuel (voir §5.6). Les valeurs de ces composantes restent à calibrer par simulations.

### 5.4 Nouvelle personne et courts historiques

**Décision confirmée :** une personne sans historique commence avec un **poids neutre**, sans avantage ni désavantage, puis l’influence de son propre historique comptabilisé **augmente graduellement** à mesure qu’il s’accumule. Une seule première ou dernière place ne doit pas produire un ajustement de poids à pleine force. À mesure que la personne s’approche de six sélections comptabilisées dans ce groupe du jour, l’influence de son historique s’approche en douceur du niveau calibré normal. La fonction / l’échelle exactes de lissage seront choisies par simulations. Les règles strictes de non-répétition s’appliquent quand même dès la première sélection comptabilisée, quand c’est mathématiquement possible, sous réserve du repli convenu (voir §7.3). Le lissage ne vise **que** l’équilibrage probabiliste doux, pas ces règles strictes. On ne compte que les sélections individuelles réellement enregistrées et admissibles. Les historiques restent séparés par groupe du jour.

**Personne qui revient :** ne pas réinitialiser silencieusement une personne qui revient comme « nouvelle ». Si elle réintègre le même groupe du jour, son historique existant est conservé (voir `regles-selecteur.md` §2.3). L’identifiant interne stable préserve l’historique à travers les changements de nom, les retraits / réadmissions et les groupes.

### 5.5 Pause anniversaire (décision confirmée)

Le mode anniversaire est une exception célébratoire, pas une priorité ordinaire ni un résultat pondéré :

- La personne fêtée obtient la première place, même si elle était première à son dernier tirage ordinaire participé.
- Sa position du jour d’anniversaire **n’entre pas** dans sa fenêtre glissante de six sélections comptabilisées, et sa séquence des extrêmes consécutifs continue à partir de sa dernière sélection ordinaire comptabilisée. Autrement dit, la sélection d’anniversaire est essentiellement un tirage sauté **pour sa propre histoire d’équité**, même si elle a participé et choisi une tâche.
- Sa position réelle reste dans l’ordre final enregistré de la date, explicitement marquée comme exception d’anniversaire.
- Les autres personnes (non fêtées) comptent normalement : leurs positions finales réelles nourrissent leur équité future.
- **Deux anniversaires le même jour (décision confirmée) :** les deux personnes obtiennent les deux premières places, ordonnées **aléatoirement entre elles**, et les deux bénéficient de la pause d’historique.
- On distingue `absent au tirage` de `participant anniversaire (présent; position réelle conservée, exclue du calcul personnel)`.
- Activation manuelle le jour même, sans base de données de dates de naissance : recommandation UX, pas une exigence confirmée.
- **Anniversaire avant les priorités (décision confirmée) :** les personnes fêtées occupent toujours les premières places, avant les priorités ordinaires; les anniversaires s’ajoutent à la limite de trois priorités, ils n’y sont pas inclus (voir §4).
- **Réorganisation manuelle (décision confirmée) :** une personne fêtée déplacée manuellement hors des places réservées aux anniversaires **perd son exemption**; sa position finale réelle enregistrée compte normalement. Échanger simplement deux personnes fêtées entre les places 1 et 2 conserve les deux exemptions. Évaluer sur l’ordre final enregistré (ou corrigé), pas sur un brouillon ni l’ordre généré initial.
- **Personne fêtée absente (décision confirmée) :** le mode anniversaire s’applique seulement si la personne fêtée est **présente à la sélection**. Sinon, « Absent(e) au tirage », aucune place réservée, pause normale due à l’absence, aucune priorité transférée, **aucun rattrapage automatique**. Aucun indicateur d’anniversaire périmé dans un brouillon ou un résultat final pour la personne absente.

### 5.6 Coups de pouce manuels (« Donner un coup de pouce ») : aujourd’hui seulement, sans option permanente (décisions confirmées)

Option avancée « Donner un coup de pouce », hors de l’écran quotidien ordinaire :

- **Positif seulement :** un coup de pouce peut seulement augmenter les chances d’une personne; aucun contrôle pour diminuer explicitement la pondération / les chances de quelqu’un. Nuance : augmenter le poids relatif d’une personne diminue par définition légèrement les probabilités relatives des autres — acceptable, mais ne pas présenter la fonction comme laissant toutes les autres exactement inchangées.
- **Un seul niveau fixe, doux et positif :** pas de niveaux sélectionnables, pas de curseur. Le multiplicateur / effet numérique n’est **pas** approuvé : à calibrer par simulations (utile mais modeste, hasard préservé, non-répétition respectée).
- **Plusieurs coups de pouce égaux :** plus d’une personne peut recevoir le même coup de pouce calibré. Pas de forces différentes par personne, pas d’empilement, pas de réduction. Si toutes les personnes admissibles reçoivent le même facteur, leurs probabilités relatives restent inchangées (neutre / redondant).
- **Qui :** tout membre autorisé de l’équipe qui est autorisé à faire fonctionner le sélecteur; aucun mot de passe supplémentaire, code administrateur distinct, ni permission réservée à Maxime. Enregistrer l’action (sous réserve du modèle d’identification); avec une connexion partagée, enregistrer au minimum les coups de pouce appliqués, à qui, pour quel tirage.
- **Aucune confirmation pour appliquer :** l’interface indique clairement chaque personne dont le coup de pouce est actif; on peut retirer / annuler avant de générer le tirage, sans confirmation supplémentaire. Cela n’affaiblit pas la confirmation pour recommencer un brouillon ni l’avertissement + confirmation pour déroger à une règle de première / dernière.
- **Durée :** strictement la sélection du jour courant, **sans option permanente ni report**. Un coup de pouce est une entrée pour une seule sélection, jamais un ajustement à long terme de la pondération de base.
- Ce n’est **pas** une priorité : un coup de pouce change les chances, il n’attribue pas de place garantie. Il reste soumis à l’admissibilité, aux réservations d’anniversaire, aux priorités et aux contraintes strictes / repli convenu. Le dossier montre les coups de pouce réellement actifs pour le brouillon généré utilisé dans le résultat final; les coups de pouce annulés avant le tirage ne comptent pas comme actifs; un tirage écarté n’entre jamais dans l’historique.
- **Points ouverts (question 18) :** valeur numérique exacte (simulations), garde-fous pendant le tirage, détails de la représentation de vérification, que faire quand une personne ayant reçu un coup de pouce devient absente. Aucun biais permanent caché du système d’équité.

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

« Tirage pertinent précédent » — **décision confirmée (question 4 résolue) :** on compare les **deux dernières sélections comptabilisées** de la personne, dans le groupe du jour. Une semaine d’absence ne réinitialise ni ne fait avancer sa séquence. Une séance à une seule personne est exclue de la contrainte des extrêmes consécutifs (voir §1).

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

Quand il n’existe vraiment aucun ordre valide (cas particuliers : priorités en conflit avec les règles de non-répétition; ou les deux personnes admissibles ont toutes les deux été premières à leur dernier tirage comptabilisé respectif — voir `regles-selecteur.md` §5.4), il faut une hiérarchie de repli explicite. Le repli ne se déclenche jamais au simple motif qu’un nombre limité d’essais a échoué.

**Hiérarchie de repli (décision confirmée, question 5, politique réglée) :** quand il est mathématiquement impossible de respecter les deux règles de non-répétition à la fois, **protéger en priorité la non-répétition de la DERNIÈRE place**. D’abord essayer de respecter les deux règles; seulement quand les deux sont conjointement impossibles, protéger la non-répétition de la dernière place si un ordre valide la respectant existe, même si cela veut dire permettre une répétition de la première place. Si même la non-répétition de la dernière place ne peut pas être respectée, produire un ordre valide au moyen d’un repli secondaire clairement documenté (encore à concevoir / tester), avec un avis clair; ne pas échouer, ne pas inventer de garantie, ne pas écarter la règle silencieusement. Les priorités manuelles / dérogations et les exemptions d’anniversaire restent régies par leurs règles propres.

**Points ouverts (question 5) :** la méthode technique exacte d’échantillonnage contraint / repli et le départage entre ordres également admissibles. Les séances à une seule personne sont exemptées des contraintes de positions consécutives (décision confirmée).

### 7.4 Exception manuelle

Si l’équipe **modifie manuellement** l’ordre (brouillon) de façon à créer une répétition de première ou de dernière place, le traitement est **décidé (question 8, résolue) :** avertissement + confirmation explicite + enregistrement comme exception manuelle; le résultat réel compte. L’application ne doit pas traiter silencieusement une exception manuelle comme un résultat aléatoire conforme.

## 8. Étape 6 — Brouillon et résultat final

- L’ordre produit est un **brouillon**, comme convenu.
- L’équipe peut le modifier, puis **enregistrer le résultat final**.
- **Seul le résultat final enregistré** nourrit l’historique d’équité des tirages suivants.
- **Re-tirage (décision confirmée, question 6, résolue) :** recommencer un tirage provisoire exige une confirmation explicite avant la révélation; après la révélation, l’équipe fait des corrections manuelles explicites; les ordres écartés ne comptent jamais pour l’équité. Seul le détail d’un journal d’audit minimal des tentatives annulées reste ouvert.
- **Conserver les deux ordres (décision confirmée, question 15, résolue) :** pour une sélection terminée, conserver l’ordre généré d’origine **et** l’ordre final confirmé, consultables ensemble dans le détail d’un résultat passé. Seul l’ordre final sert à la pondération et à l’historique première / dernière; l’original sert à la transparence / vérification. Les corrections conservent les versions antérieures; seul l’ordre final corrigé courant fournit les positions faisant foi.
- **Page de statistiques d’équité (décision confirmée, question 12, résolue) :** page facultative, distincte et facile à comprendre, à partir des résultats réellement enregistrés (par exemple, comptes de places en première vs deuxième moitié). Elle ne doit pas ressembler à une évaluation du rendement ni classer par mérite. Les affichages doivent distinguer absences, pauses d’anniversaire, séances uniques exclues et priorités / modifications manuelles, pour ne pas contredire le calcul d’équité.
- Un brouillon non enregistré ne compte pas.

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
- Exceptions d’anniversaire : (a) la personne fêtée est placée première; (b) sa place d’anniversaire ne modifie pas son poids futur ni sa séquence des extrêmes; (c) les positions réelles des autres continuent de compter; (d) un re-tirage / une annulation ne crée pas d’historique fantôme. Brouillons non enregistrés : jamais comptés. (e) Anniversaire avant les priorités : deux anniversaires + trois priorités → places 1–2 anniversaire, places 3–5 priorités. (f) Personne fêtée déplacée hors des places réservées → exemption annulée. (g) Personne fêtée absente → « Absent(e) au tirage », aucune place réservée, aucun rattrapage.
- Coups de pouce manuels : effet le jour même seulement, sans option permanente, ajustement identifiable comme manuel; plusieurs coups de pouce égaux; toutes les personnes avec un coup de pouce → probabilités relatives inchangées; coup de pouce annulé avant le tirage → non compté comme actif.
- Corrections de résultats enregistrés : toutes les versions antérieures conservées, ordre corrigé utilisé pour la suite, aucune réécriture rétroactive des séances passées, aucune limite de temps.
- Hiérarchie de repli : impossibilité conjointe → protéger la non-répétition de la dernière place; même celle-ci impossible → repli secondaire documenté + avis clair.
- Récence + lissage : un tirage malchanceux unique, un tirage chanceux unique, absences; influence graduelle d’un nouvel historique.

**Seuils d’acceptation :** à définir avec Avery et Mira avant de considérer l’algorithme acceptable. Tant que les simulations ne sont pas faites, la pondération reste une hypothèse, pas une garantie.

## 10. Liste des décisions : tranchées vs à prendre (pour la discussion)

**Tranchées (décisions confirmées 2026-10-14, Avery) :**

- Fenêtre d’historique : six sélections comptabilisées par personne, par groupe; récence douce (les récentes comptent légèrement plus); lissage graduel des courts historiques (question 3, partiellement résolue — courbes / seuils ouverts).
- « Consécutive » = deux dernières sélections comptabilisées de la personne (question 4, résolue).
- Séances à une seule personne : exclues de la pondération et de la contrainte des extrêmes consécutifs (question 5, partiellement résolue — méthode technique ouverte).
- Hiérarchie de repli : quand les deux règles sont conjointement impossibles, protéger la non-répétition de la **dernière** place; si même celle-ci est impossible, repli secondaire documenté + avis clair (question 5, politique réglée).
- Re-tirage : possible avant la révélation avec confirmation « Êtes-vous sûr(e)? »; après le début, corrections manuelles; propositions écartées jamais dans l’historique (question 6, résolue; la conservation d’une trace d’audit minimale des tentatives annulées est un détail d’implémentation).
- Réorganisation manuelle qui crée une répétition : avertissement + confirmation + enregistrement comme exception manuelle; le résultat réel compte (question 8, résolue).
- Corrections : tout membre autorisé; raison écrite facultative; aucune limite de temps; toutes les versions conservées, vérification automatique (question 7, résolue).
- Prénoms identiques : nom usuel préféré; initiale seulement si deux noms d’affichage identiques dans le groupe (question 13, résolue).
- Priorités : tout compte pareil; aucune catégorie d’accommodement, aucun champ de raison médicale, aucune exclusion spéciale (question 14, résolue).
- Original + final conservés; seul le final sert à l’équité; l’original sert à la transparence (question 15, résolue).
- Personne qui revient : historique conservé dans le même groupe; identifiant interne stable (question 16, résolue).
- Coups de pouce : positifs seulement; un seul niveau fixe doux; plusieurs égaux possibles; tout membre autorisé, sans privilège supplémentaire; aucune confirmation pour appliquer; strictement le jour courant, sans option permanente (question 18, partiellement résolue — valeur numérique et détails ouverts).
- Mode anniversaire : pause d’historique pour la personne fêtée; deux anniversaires → deux premières places, ordre aléatoire, les deux en pause; anniversaires avant les priorités (en plus de la limite de trois); réorganisation hors des places réservées → exemption annulée; personne fêtée absente → « Absent(e) au tirage », aucun rattrapage (question 19, résolue).
- Personne prioritaire absente : retrait automatique + resserrement de la liste, sans pénalité ni report (question 6.4 des règles, décidée).
- Page de statistiques d’équité facultative approuvée (question 12, résolue).
- Poursuite hors connexion d’un tirage déjà ouvert; sauvegardes automatiques + exportation sur demande (questions 20–21, exigences réglées; détails techniques ouverts).
- Accès d’équipe partagée proposé, en attente de Maxime / examen de sécurité (question 10, proposition approuvée).
- « Comment ça fonctionne? » : 1–2 pages + page distincte « L’essentiel en bref » (question 17, résolue).
- Conservation : six mois proposés, en attente de Maxime; tension conservation / continuité OUVERTE (question 22, provisoire).

**À prendre (pour la discussion / les simulations) :**

1. Formule de pondération : forme, force k, plancher Wmin, plafond Wmax, et ratio Wmax / Wmin — en intégrant récence, lissage et coup de pouce (question 1).
2. Normalisation exacte des positions, y compris le cas d’une seule personne présente (question 2).
3. Fenêtre : courbe exacte de récence; fonction / échelle exactes de lissage; seuils de simulation (question 3).
4. Repli : méthode technique exacte d’échantillonnage contraint / repli; départage entre ordres également admissibles (question 5).
5. Plan de simulations : mesures, scénarios, seuils d’acceptation (question 9).
6. Méthode de tirage et d’application des contraintes : la course exponentielle et le tirage séquentiel pondéré produisent la même distribution (Plackett-Luce) — le choix est une question d’implémentation. Pour les contraintes : la base « faisabilité explicite + échantillonnage conditionné (acceptation / rejet + solution exacte pour petits cas ou faible taux d’acceptation) » convient-elle comme base testable?
7. Coups de pouce : valeur numérique exacte (simulations), garde-fous pendant le tirage, détails de la représentation de vérification, coup de pouce + absence (question 18).
8. Synchronisation hors connexion (stratégie technique + fournisseur de mise en cache), fréquence / format / outillage des sauvegardes et exportations, réconciliation conservation / continuité + approbations de Maxime (conservation, accès partagé) (questions 20–22, 10).

Tant que les paramètres mathématiques ne sont pas validés par simulations, on ne programme pas l’algorithme. Ce document est une base de discussion et de simulation, pas une spécification finale.
