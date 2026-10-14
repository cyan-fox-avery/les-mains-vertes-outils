# Sélecteur d’ordre de passage — Règles fonctionnelles

> **Statut :** règles convenues entre Avery et Mira, documentées pour relecture.
> Ce document décrit ce qui est convenu. Tout ce qui n’est pas encore tranché est dans `questions-ouvertes.md` et ne doit pas être lu comme déjà décidé.
>
> **Principe directeur :** l’application détermine l’**ordre de choix** des tâches. Elle n’attribue pas les tâches elle-même.

## 1. Vocabulaire

- **Tirage / sélection :** le processus qui produit un ordre de passage pour une journée donnée.
- **Ordre de passage :** la liste, de la première à la dernière personne, dans laquelle les personnes présentes choisissent leur tâche du jour.
- **Groupe du jour :** la liste des personnes participantes associées à un jour de semaine donné (lundi, mardi, mercredi ou jeudi).
- **Sélection pertinente :** une sélection antérieure du même groupe du jour qui compte pour les règles d’équité. La définition exacte de « consécutive » quand une personne s’est absentée reste une question ouverte (voir `questions-ouvertes.md`).
- **Brouillon :** un ordre généré mais pas encore confirmé.
- **Résultat final :** l’ordre confirmé par l’équipe une fois le choix des tâches terminé. C’est le seul qui compte pour l’équité future.
- **Priorité de passage :** une place de début d’ordre (1, 2 ou 3) attribuée manuellement par l’équipe, avant le tirage aléatoire.

## 2. Groupes par jour de semaine

### 2.1 Groupes séparés

- Il y a un groupe distinct pour chaque jour : **lundi, mardi, mercredi et jeudi**.
- Chaque jour de semaine utilise toujours son propre groupe récurrent. Par exemple, chaque mardi utilise le groupe du mardi.
- Le lundi peut être facultatif, selon l’horaire de l’atelier. Un lundi sans séance ne crée pas de tirage et ne modifie pas l’historique du groupe du lundi.

### 2.2 Composition des groupes

- Un groupe contient habituellement **10 à 15 personnes participantes**.
- Une personne peut appartenir à plusieurs groupes (par exemple, mardi et jeudi).
- Les groupes gardent des historiques **indépendants**, même quand une personne appartient à plusieurs groupes. Être première un mardi ne doit pas influencer un tirage du jeudi.

### 2.3 Gestion de la liste des personnes

L’équipe peut :

- **ajouter** une personne à un groupe;
- **renommer** une personne (par exemple, corriger l’orthographe d’un prénom);
- **retirer** une personne d’un groupe.

Les règles exactes pour l’historique d’une personne renommée ou retirée (est-ce que son historique suit le nouveau nom? est-ce qu’on garde son historique après un retrait?) restent à préciser. On ne supprime pas l’historique d’un tirage déjà enregistré en renommant ou en retirant quelqu’un.

## 3. Présences

### 3.1 Avant chaque tirage

- Avant chaque tirage, l’équipe coche les personnes **absentes** pour cette journée-là.
- Les personnes absentes sont **exclues du tirage**, sans être retirées de la liste du groupe.
- Les présences valent seulement pour la sélection du jour. Une absence un jour ne retire personne du groupe et ne change pas la composition du groupe les semaines suivantes.

### 3.2 Arrivée après la sélection

- Une personne qui arrive après la sélection se fait attribuer une tâche **séparément, par l’équipe**, parmi ce qui reste.
- Elle reste enregistrée comme **absente du tirage**, même si elle a finalement travaillé ce jour-là.
- Règle décidée : elle est simplement traitée comme **absente du tirage**, avec **aucune place et aucune pénalité d’équité** pour cette date. On n’évalue pas si la tâche attribuée plus tard était « bonne », et on ne suit pas cette attribution séparément dans le sélecteur : un seul statut « absent au tirage » suffit.

### 3.3 Ne pas pénaliser les absences

- **Manquer un tirage ne doit pas pénaliser quelqu’un** dans les calculs d’équité futurs.
- Concrètement : une absence ne doit pas être comptée comme une mauvaise place, ni comme une place du tout, dans l’historique d’équité de la personne.
- La façon exacte de calculer la fenêtre d’historique quand une personne manque des semaines (derniers tirages du groupe vs derniers tirages où la personne était présente) reste une question ouverte.

## 4. Deux modes de sélection

L’application doit offrir les deux modes suivants. Les deux utilisent le **même algorithme de hasard**.

### 4.1 Mode « Liste complète »

- Génère et affiche **tout l’ordre** d’un coup.
- L’équipe voit la liste complète et peut la passer en revue.

### 4.2 Mode « Une personne à la fois »

- Génère l’ordre complet à l’interne, **avant** de montrer le premier nom.
- Révèle ensuite les noms **un à un**, à la demande de l’équipe (bouton « Révéler le prochain nom »).
- L’ordre ne doit pas être régénéré entre deux révélations pour « essayer d’avoir un meilleur ordre ». Une fois la révélation commencée, l’ordre généré est l’ordre de référence, sauf modification manuelle explicite par l’équipe (voir section 7).

### 4.3 Règle commune

- Dans les deux modes, chaque personne admissible apparaît **exactement une fois** dans l’ordre.
- Le fait de régénérer un brouillon non terminé (est-ce permis? dans quelles circonstances? combien de fois?) est une question ouverte.

## 5. Règles d’équité obligatoires

Approche choisie : **hasard pondéré avec équilibrage doux à long terme**. Le tirage reste vraiment aléatoire; il n’est jamais une rotation prévisible.

### 5.1 Règles obligatoires, quand c’est mathématiquement possible

1. **Pas deux fois première de suite.** La même personne ne peut pas occuper la première place dans deux sélections pertinentes consécutives.
2. **Pas deux fois dernière de suite.** La même personne ne peut pas occuper la dernière place dans deux sélections pertinentes consécutives.
3. **Chaque personne admissible apparaît exactement une fois.**

« Quand c’est mathématiquement possible » veut dire : dans certains cas particuliers, il peut devenir impossible de respecter les deux règles de non-répétition en même temps. Dans ce cas, le système doit gérer la situation avec élégance (voir section 5.4), pas planter ni produire un ordre invalide.

### 5.2 Équilibrage à long terme

- Les personnes qui ont reçu **à répétition des places tardives** devraient avoir **un peu plus de chances** d’obtenir des places plus hâtives.
- L’effet doit rester **doux** : une amélioration des chances, pas une garantie, et jamais une rotation déguisée.
- Les positions historiques doivent être **normalisées selon la taille du groupe**. Être 12e sur 14, ce n’est pas la même chose qu’être 12e sur 12 ou 5e sur 6. La formule exacte de normalisation reste à décider.
- L’équité se calcule **séparément pour chaque groupe du jour**.
- Point de départ discuté (proposition, pas une règle finalisée) : utiliser **environ les six derniers tirages auxquels la personne a assisté** comme fenêtre d’historique. Le nombre exact, la façon de pondérer les tirages récents par rapport aux plus anciens, et la force de la compensation restent à décider.
- La pondération doit être **testée par simulations** avant d’être considérée comme fiable. On ne suppose pas que la pondération fonctionne comme prévu; on le vérifie.

### 5.3 Ce que l’équilibrage ne doit pas devenir

- Pas une rotation (« chacun son tour »).
- Pas un système où l’ordre devient prévisible après quelques semaines.
- Pas un système qui punit une personne pour une absence.
- Pas un système qui annule l’effet du hasard : même une personne « due » pour une bonne place peut, certains jours, tirer une place tardive. C’est normal.

### 5.4 Petits groupes et contraintes impossibles

- Le système doit gérer les cas limites avec élégance, en particulier quand très peu de personnes sont présentes.
- Exemples de cas limites :
  - **Une seule personne présente :** l’ordre est trivial (une seule place). Les règles de non-répétition n’ont pas de sens.
  - **Deux personnes présentes :** dans le cas ordinaire, les deux règles peuvent être respectées en même temps en inversant l’ordre précédent. Par exemple, si le dernier tirage était `Amélie → Benoît`, le tirage `Benoît → Amélie` respecte les deux règles : la première place change et la dernière place change.
  - **Trois personnes présentes :** les contraintes restreignent les ordres possibles, mais des ordres conformes existent généralement.
- L’impossibilité peut survenir dans des cas plus particuliers, par exemple :
  - une séance précédente avec une seule personne, **à condition** que cette personne participe au tirage suivant et qu’il y ait au plus deux personnes admissibles (sans compter les priorités manuelles) : avec trois personnes ou plus au tirage suivant, l’ancienne participante unique peut être placée au milieu et éviter les deux répétitions;
  - des priorités manuelles qui entrent en conflit avec les règles de non-répétition.
- Question ouverte liée : les séances à une seule personne sont-elles exemptées des contraintes de positions consécutives (c’est-à-dire qu’elles ne créent pas d’historique de première/dernière place), ou compte-t-on quand même leur première/dernière place pour le tirage suivant? Le présent document dit que les règles « n’ont pas de sens » pour un tirage à une seule personne, sans trancher si cette séance compte pour le tirage suivant. Ce choix reste ouvert (voir `questions-ouvertes.md`, question 5).
- L’ordre de priorité entre les règles quand elles entrent en conflit (laquelle on relâche en premier, et comment on l’explique à l’équipe) est une question ouverte. Le système doit au moins :
  - toujours produire un ordre valide (chaque personne présente exactement une fois);
  - ne jamais bloquer l’équipe;
  - indiquer clairement, dans l’interface, quand une règle d’équité n’a pas pu être respectée et pourquoi.

## 6. Priorités manuelles

### 6.1 Règles

- L’équipe peut désigner **jusqu’à trois personnes prioritaires** pour un tirage donné.
- Habituellement, une seule personne a besoin d’une priorité.
- Les personnes prioritaires occupent les places **1, 2 et 3**, selon le cas, **dans l’ordre indiqué** par l’équipe.
  - Une seule priorité → place 1.
  - Deux priorités → places 1 et 2, dans l’ordre indiqué.
  - Trois priorités → places 1, 2 et 3, dans l’ordre indiqué.
- Les autres personnes sont placées par tirage aléatoire avec l’algorithme d’équité, dans les places restantes.
- Les priorités doivent être **enregistrées comme des décisions manuelles** (pas comme des résultats du hasard).
- Les places réellement obtenues **comptent quand même** pour l’équité à long terme. Par exemple, une personne prioritaire qui obtient la place 1 verra cette place 1 dans son historique.

### 6.2 Priorité et règle de non-répétition de la première place

- Si une priorité placerait quelqu’un en première place pour une **deuxième fois consécutive**, l’application affiche un **avertissement**, mais permet une **dérogation intentionnelle**.
- La dérogation doit être un geste explicite de l’équipe (on ne passe pas outre à l’avertissement par accident).
- La dérogation est enregistrée comme une décision manuelle.

### 6.3 Questions liées aux priorités (non tranchées)

- Qu’est-ce qui se passe si une personne prioritaire est absente le jour même? (Sa priorité est-elle ignorée, déplacée, ou annulée?)
- Qu’est-ce qui se passe si une priorité entre en conflit avec la règle de non-répétition de la dernière place dans un très petit groupe? (Voir section 5.4.)
- Est-ce qu’une personne qui reçoit souvent des priorités (par exemple, pour un accommodement récurrent) devrait voir ses priorités compter exactement comme les autres places dans l’historique d’équité, ou être signalée différemment? La règle convenue dit « ça compte », mais la tension avec les accommodements récurrents est notée comme préoccupation à trancher.

## 7. Brouillon, modification et enregistrement du résultat final

C’est une partie particulièrement importante du système.

### 7.1 Brouillon

- Chaque tirage du jour produit d’abord un **brouillon**.
- L’équipe doit pouvoir **passer en revue** l’ordre généré avant de le confirmer.
- Un brouillon non terminé devrait **survivre à un rafraîchissement accidentel de la page**, quand c’est pratiquement faisable (par exemple, en gardant le brouillon en mémoire locale ou côté serveur, selon l’architecture retenue).

### 7.2 Modification manuelle

- L’équipe doit pouvoir **réorganiser manuellement** les personnes pour refléter les changements du monde réel (par exemple, quelqu’un doit partir plus tôt, une contrainte de dernière minute).
- La modification manuelle est un geste normal, pas une exception. L’outil ne doit pas la décourager ni la cacher.
- Si une réorganisation manuelle crée une répétition de première ou de dernière place, la façon de le traiter (avertissement, confirmation, enregistrement de l’exception) est une question ouverte (voir `questions-ouvertes.md`, question 8). L’application ne doit pas traiter silencieusement une exception manuelle comme un résultat aléatoire conforme.

### 7.3 Enregistrement final

- Une fois le choix des tâches terminé, l’équipe **enregistre explicitement le résultat final** (bouton « Enregistrer le résultat final »).
- **Seul le résultat final confirmé devient le dossier officiel** utilisé pour les calculs d’équité futurs.
- Autrement dit, l’application doit se souvenir de **ce qui s’est vraiment passé**, pas seulement de ce qu’elle avait proposé au départ.
- Tant que le résultat n’est pas enregistré, il ne doit pas compter dans l’historique d’équité.

### 7.4 Corrections après enregistrement

- On a discuté de permettre des **corrections à des résultats déjà enregistrés**, idéalement avec un **historique de vérification** de base (qui a changé quoi, et quand).
- Le flux de travail précis (qui peut corriger, jusqu’à quand, est-ce qu’on garde l’ancienne version, est-ce que la correction recalcule l’équité future?) **reste à finaliser**. Voir `questions-ouvertes.md`.

## 8. Historique

### 8.1 Ce qu’on conserve pour chaque tirage enregistré

Pour chaque tirage enregistré, on conserve :

- la **date**;
- le **groupe du jour** (lundi, mardi, mercredi ou jeudi);
- les **noms des personnes participantes** (les personnes présentes au tirage);
- l’**ordre final**;
- les **priorités manuelles** attribuées, le cas échéant;
- les **renseignements de présence** pertinents pour le tirage (qui était absent au tirage).

### 8.2 Règles d’historique

- Les historiques restent **séparés par groupe**. L’historique du mardi ne se mélange jamais avec celui du jeudi.
- Si une séance d’un jour de semaine est **sautée** (par exemple, pas de séance un mardi), la séance suivante utilise le **dernier historique pertinent complété** pour ce groupe-là. On ne « repart pas à zéro » parce qu’on a sauté une semaine.
- Idéalement, l’application offre une **page d’historique** où l’équipe peut consulter les résultats passés.

### 8.3 Vue « Équité des tirages » (proposition, pas une exigence initiale)

- On pourrait éventuellement ajouter une vue simple « Équité des tirages » pour expliquer comment les places ont été réparties.
- C’est une **fonctionnalité proposée**, pas une exigence initiale. Son utilité réelle (est-ce que l’équipe la consulterait? est-ce qu’elle aide à la confiance?) reste à évaluer.

## 9. Interface et accessibilité

### 9.1 Langue

- Tout ce que les personnes participantes et les membres de l’équipe voient doit être en **français québécois**.
- Les étiquettes proposées (à valider avec l’équipe) :
  - « Groupe du jour »
  - « Présences »
  - « Tirer au sort »
  - « Révéler le prochain nom »
  - « Priorités de passage »
  - « Modifier l’ordre »
  - « Enregistrer le résultat final »
  - « Historique »
  - « Comment ça fonctionne? »

### 9.2 Exigences

- **Simple à utiliser** avec un minimum de formation.
- **Confortable** sur téléphone, tablette et ordinateur.
- **Accessible** : libellés clairs, typographie lisible, grandes zones tactiles.
- **Accueillant visuellement**, sans être encombré.
- **Cohérent** avec l’identité visuelle de Les Mains Vertes.
- Le logo officiel apparaîtra dans l’en-tête ou dans un coin. Avery fournira le logo. On ne génère pas de logo de remplacement.
- Voir aussi §13 — critère d’acceptation non négociable (« plus facile que le contenant de yogourt »).

## 10. Données et stockage

- Direction privilégiée : un système **partagé et synchronisé**, accessible par plusieurs membres de l’équipe à partir de différents appareils.
- Solution de repli acceptable : une solution sur **un seul appareil**, si le stockage partagé ajoute une complexité disproportionnée.
- On ne conserve que les **prénoms**. Malgré tout, les données des personnes participantes et les historiques de présence doivent rester **en dehors du code source**, avec une protection d’accès raisonnable.
- Aucune base de données, aucun fournisseur d’authentification ni aucune plateforme d’hébergement n’est choisi à ce stade. Les options techniques seront documentées sans engagement lors de l’étape d’architecture.

## 11. Ce que l’outil ne fait pas

- Il ne choisit pas les tâches à la place des personnes.
- Il ne gère pas les horaires, la paie, les dossiers médicaux ou les plans d’intervention.
- Il ne classe pas les personnes selon leur rendement.
- Il ne publie rien à l’extérieur de l’atelier.
- Il ne prend pas de décision à la place de l’équipe : en cas de doute, l’équipe tranche, et l’outil enregistre ce qui a été décidé.

## 12. Cas limites à gérer (liste non exhaustive)

- Très peu de personnes présentes (1, 2 ou 3).
- Tout le monde est absent (aucun tirage possible).
- Une personne prioritaire est absente.
- Une personne arrive après la sélection.
- Une séance est annulée ou sautée.
- Un brouillon est abandonné sans être enregistré.
- La page est rafraîchie pendant un brouillon ou pendant une révélation un à un.
- Deux membres de l’équipe modifient le même tirage en même temps, à partir de deux appareils.
- Deux personnes ont le même prénom dans un groupe.
- Une personne change de groupe ou quitte l’atelier.

Chaque cas limite doit avoir un comportement défini avant ou pendant la programmation. Les cas qui n’ont pas encore de réponse sont repris dans `questions-ouvertes.md`.

## 13. Critère d’acceptation non négociable : plus facile que le contenant de yogourt

**Règle décidée (exigence d’Avery, confirmée, non négociable) :** le sélecteur doit être réellement **plus facile et plus intuitif à utiliser que les petits papiers dans le contenant de yogourt** qu’il remplace.

Ce n’est pas une préférence esthétique générale ni un élément de finition à venir. C’est un **critère d’acceptation central** qui gouverne l’interface *et* l’architecture. Un processus de sélection mathématiquement meilleur ne suffit pas si Max et l’équipe doivent naviguer dans plusieurs écrans, mémoriser des instructions ou attendre.

### Traduction pratique proposée (à valider avec Avery et l’équipe, pas finale)

Les critères ci-dessous traduisent le principe en exigences pratiques. Ils sont proposés pour validation — la disposition exacte des écrans, les réglages par défaut et les cibles mesurables d’utilisabilité restent des choix de conception à évaluer avec Avery et l’équipe :

- **Parcours normal presque sans friction :** ouvrir le site → le groupe du jour de la semaine est déjà sélectionné → cocher seulement les noms des personnes absentes → désigner facultativement 1 à 3 priorités → lancer le tirage → voir l’ordre complet OU révéler un nom à la fois → enregistrer explicitement le résultat final réel. Pas d’assistant de configuration ni d’écran de réglages obligatoire.
- **Actions courantes explicites par elles-mêmes :** gros boutons clairement libellés, en français québécois naturel; lisibilité et contraste élevés; commandes confortables au touché; aucune connaissance technique ni formation nécessaire.
- **Complexité hors du chemin quotidien :** la gestion des listes, les statistiques historiques, les explications d’équité, les corrections aux journées plus anciennes et les options d’administration ne doivent pas encombrer l’écran principal. Elles restent accessibles au besoin.
- **Pas de travail répétitif inutile :** les listes par jour de semaine se répètent; les présences doivent être rapides à cocher; rouvrir la page doit retrouver le brouillon du jour ou le résultat confirmé, plutôt que de forcer une nouvelle séance. On ne fait pas reconstruire l’état de la journée à l’équipe après un rafraîchissement.
- **Fiabilité, ça fait partie de la facilité d’usage :** réponse rapide, statut clair (« brouillon » vs « enregistré »), prévention des retirages accidentels, et plan de reprise en cas d’échec. Une approche de connexion ou de synchronisation qui se met sans cesse en travers du chemin contredit le but.
- **Tester avec de vraies tâches :** idéalement, observer une collègue ou un collègue qui ne connaît pas le site l’utiliser sans accompagnement; comparer l’effort, la confusion et le temps avec la pratique actuelle des petits papiers. Si l’outil ajoute de la friction, simplifier avant la sortie.

### Garde-fou : la simplicité ne retire pas les exigences choisies

On n’élimine pas les exigences qu’Avery a délibérément choisies — les deux modes de révélation, les priorités facultatives, le résultat modifiable et l’enregistrement final explicite — au nom de la simplicité. La solution, c’est une **divulgation progressive et de meilleurs réglages par défaut**, pas la suppression d’un contrôle nécessaire.
