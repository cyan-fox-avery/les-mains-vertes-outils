# Options d’architecture — Document de discussion

> **Statut : proposition à discuter. Direction convenue, détails techniques ouverts.**
>
> Ce document présente des options pour l’architecture du sélecteur d’ordre de passage, pour que Avery et Mira puissent en discuter. **Direction convenue 2026-10-14 (Avery) : option A** — site statique + base de données hébergée, éventuellement avec fonctions serveur gérées — sous réserve d’une évaluation réaliste de l’hébergement, de la confidentialité, de l’accès, des sauvegardes / exportations et de la protection contre les écrasements concurrents. **Aucun fournisseur, aucune base de données, aucun schéma d’authentification ni aucune région d’hébergement n’est choisi.** Les règles convenues sont dans `regles-selecteur.md`; les questions ouvertes sont dans `questions-ouvertes.md` (en particulier les questions 10 et 11 : architecture et accès simultané).

## 1. Rappel des besoins

Ce que l’architecture doit permettre (d’après les règles convenues) :

- **Accès partagé (direction privilégiée) :** plusieurs membres de l’équipe, à partir de différents appareils (téléphone, tablette, ordinateur).
- **Solution mono-appareil acceptable en repli**, si le stockage partagé ajoute une complexité disproportionnée.
- **Données :** prénoms seulement, mais historiques de présences et de tirages conservés — ces données restent en dehors du code source, avec une protection d’accès raisonnable.
- **Un seul dossier officiel par tirage :** brouillon → ordre final enregistré. Le résultat final est ce qui compte pour l’équité future.
- **Brouillon qui survit à un rafraîchissement** de la page, quand c’est pratiquement faisable.
- **Historique séparé par groupe** (lundi, mardi, mercredi, jeudi).
- **Traçabilité des décisions manuelles :** priorités, modifications manuelles, dérogations, corrections éventuelles — on doit savoir que c’était manuel, pas du hasard.
- **Accessibilité :** interface simple, grandes zones tactiles, texte lisible, en français québécois.
- **Critère d’acceptation non négociable :** l’outil doit être réellement **plus facile et plus intuitif à utiliser que les petits papiers dans le contenant de yogourt** qu’il remplace. Ce critère gouverne l’interface *et* l’architecture : une approche d’authentification ou de synchronisation qui se met sans cesse en travers du chemin contredit son but. Règle complète dans `regles-selecteur.md` §13 (proposée dans la demande nº 3). On ne simplifie pas en retirant des exigences choisies (deux modes de révélation, priorités facultatives, résultat modifiable, enregistrement final explicite) — on simplifie par une divulgation progressive et de meilleurs réglages par défaut.

## 2. Options

### Option A — Site statique + base de données hébergée (service tout-en-un) — DIRECTION CONVENUE, SOUS RÉSERVE D’ÉVALUATION

**Principe :** l’interface est un site statique (HTML, CSS, JavaScript). Les données vivent dans un service de base de données hébergée qui offre aussi l’authentification et la synchronisation.

**Conditions de la direction convenue :** évaluer de façon réaliste l’hébergement, la confidentialité, l’accès, les sauvegardes / exportations et la protection contre les écrasements concurrents avant de s’engager. Friction de connexion quotidienne minimale — idéalement, une session protégée persistante sur les appareils de confiance de l’équipe.

**Avantages :**

- Peu de code serveur à écrire et à maintenir.
- Synchronisation entre appareils incluse dans le service.
- Accès multi-appareils naturel.

**Inconvénients / risques :**

- Dépendance à un fournisseur : ses conditions, ses prix et l’endroit où les données sont hébergées.
- L’authentification et les permissions doivent être configurées avec soin — un mauvais réglage peut exposer les données.
- La logique du tirage (pondération, contraintes) tourne dans le navigateur, sauf si on ajoute une vérification côté serveur. Il faut décider si c’est acceptable. Précision : un site statique ne se limite pas forcément à une logique dans le navigateur — il peut aussi s’appuyer sur des fonctions serveur gérées (hybride) pour faire tourner le tirage côté serveur. Aucun fournisseur n’est choisi ici.

**Questions que cette option soulève :** quel fournisseur? Où sont hébergées les données? Quel plan (gratuit/payant)? Qui administre les accès?

### Option B — Petite application avec backend léger (non retenue comme direction)

**Principe :** l’interface communique avec un petit backend dédié (serveur léger ou fonctions à la demande) et une base de données gérée. Le tirage et l’enregistrement passent par le backend.

**Avantages :**

- Contrôle complet sur la logique : le tirage, les contraintes et l’enregistrement du résultat final sont vérifiés côté serveur, pas seulement dans le navigateur.
- Authentification et permissions sur mesure (par exemple, qui peut corriger un résultat enregistré).
- Gestion des conflits plus explicite (voir section 4).

**Inconvénients / risques :**

- Plus de code à écrire, à tester et à maintenir.
- Hébergement à choisir et à surveiller (même si c’est petit).
- Coût et complexité plus élevés que l’option A pour un premier outil.

**Questions que cette option soulève :** quel langage / cadre? Où héberger le backend? Qui le maintient si quelque chose brise?

### Option C — Mono-appareil d’abord (repli déjà prévu, non retenue comme direction)

**Principe :** l’application fonctionne sur un seul appareil (par exemple, la tablette de l’atelier). Les données sont conservées localement sur l’appareil, avec export / sauvegarde manuelle.

**Avantages :**

- Le plus simple à construire et à expliquer.
- Pas de serveur, pas de compte fournisseur, pas de coût d’hébergement.
- Fonctionne sans connexion internet.
- Les données restent physiquement à l’atelier.

**Inconvénients / risques :**

- Pas de synchronisation : si quelqu’un veut consulter l’historique d’un autre appareil, ce n’est pas possible.
- Risque de perte si l’appareil brise ou est réinitialisé sans sauvegarde.
- Un seul brouillon actif à la fois, sur un seul appareil — si deux personnes veulent travailler en même temps, il faut s’organiser autrement.
- Le brouillon qui survit à un rafraîchissement est faisable en local, mais le partage reste manuel.

**Questions que cette option soulève :** quel appareil? Qui fait les sauvegardes, et à quelle fréquence? Comment exporter l’historique?

### Ce que ce document ne recommande plus comme ouvert

La direction est convenue (option A, sous réserve d’évaluation). Restent ouverts : le fournisseur, la base de données, le schéma d’authentification, la région d’hébergement, et l’approbation de Max pour l’accès d’équipe (voir §3 et §6).

## 3. Modèles d’accès (préférence initiale, sous réserve de l’approbation de Max)

L’architecture ne choisit pas seulement où vivent les données, mais **qui peut ouvrir l’outil et faire quoi**. Préférence initiale (pas une décision définitive) : **accès d’équipe protégé simple** plutôt que beaucoup de comptes individuels — **sous réserve de l’approbation opérationnelle / confidentialité de Max**. La friction de connexion quotidienne doit rester minimale (idéalement, session protégée persistante sur les appareils de confiance de l’équipe).

- **Accès partagé protégé (un seul mot de passe ou code pour l’équipe) :** simple, mais on ne sait pas qui a fait quelle modification. La traçabilité des corrections et des dérogations devient difficile (« quelqu’un de l’équipe », sans nom). Pour les corrections, on enregistre au moins que le changement a eu lieu, quand, et ce qui a changé; l’auteur seulement si le modèle d’accès le permet.
- **Comptes individuels (chaque membre de l’équipe a son accès) :** on sait qui a enregistré, modifié ou corrigé quoi. Plus de gestion (créer / retirer des comptes), mais meilleure traçabilité.
- **Lien protégé / code d’accès :** intermédiaire — plus simple que des comptes, mais la protection dépend du secret du lien ou du code, et il faut pouvoir le changer si le code circule.

**Point à trancher :** la traçabilité des corrections et des dérogations exige-t-elle de savoir *qui* a agi, ou suffit-il de savoir *que* c’était manuel? La réponse change le modèle d’accès.

## 4. Accès simultané (question ouverte 11)

Si deux membres de l’équipe modifient le même tirage en même temps, à partir de deux appareils, que se passe-t-il? Options à discuter, sans en choisir une :

- **Un seul brouillon actif par groupe et par jour :** la première personne qui ouvre le tirage le « réserve »; les autres voient qu’il est en cours de modification.
- **Verrouillage pendant la modification :** l’outil empêche deux modifications en même temps.
- **Dernière modification gagne :** simple, mais une modification peut écraser l’autre sans avertissement.
- **Signalement de conflit :** l’outil prévient que le tirage a changé entre-temps et demande de vérifier avant d’enregistrer.

Dans la pratique quotidienne (un tirage par groupe et par jour, fait par une personne à la fois), les conflits devraient être rares. Mais il faut un comportement défini, sinon le premier conflit réel produira deux versions du « résultat officiel ».

## 5. Autres points à trancher avec l’architecture

- **Sauvegarde et récupération :** comment on sauvegarde l’historique, et comment on le récupère si quelque chose brise? À quelle fréquence?
- **Exportation :** l’équipe peut-elle exporter l’historique (par exemple, pour Max ou pour archives)? Dans quel format?
- **Suppression et conservation :** combien de temps garde-t-on l’historique? Que se passe-t-il quand une personne quitte l’atelier — garde-t-on ses anciens tirages (oui, en principe, pour l’historique), et retire-t-on son nom des tirages futurs?
- **Fonctionnement sans connexion :** si le wifi coupe pendant un tirage, que se passe-t-il? Le brouillon est-il conservé localement en attendant?
- **Coût et maintenance :** qui paie (s’il y a un coût)? Qui est prévenu si le service tombe? Qui corrige si quelque chose brise?
- **Protection des données :** où sont hébergées les données (pays)? Qui a accès au service d’hébergement, en plus de l’équipe? Les prénoms seuls réduisent le risque, mais l’historique des présences reste une donnée sensible à protéger.
- **Journal d’audit :** quelles actions consigne-t-on (priorités, modifications, dérogations, corrections)? Pour chaque action, consigne-t-on la date, l’heure et, selon le modèle d’accès, la personne?

## 6. Liste des décisions : tranchées vs à prendre (pour la discussion)

**Tranchée :** option d’architecture = **A** (site statique + base de données hébergée, éventuellement fonctions serveur gérées), sous réserve d’une évaluation réaliste de l’hébergement, de la confidentialité, de l’accès, des sauvegardes / exportations et de la protection contre les écrasements concurrents.

**À prendre :**

1. Fournisseur, base de données, schéma d’authentification, région d’hébergement — aucun choix fait.
2. Modèle d’accès définitif — préférence initiale : accès d’équipe protégé simple, **sous réserve de l’approbation opérationnelle / confidentialité de Max** — et ce que ça implique pour la traçabilité (auteur des corrections seulement si le modèle le permet).
3. Comportement en cas d’accès simultané + protection contre les écrasements concurrents (à évaluer).
4. Sauvegarde, exportation, conservation, suppression.
5. Fonctionnement sans connexion.
6. Coût, hébergement, maintenance, et qui est responsable de chaque point.
7. Protection des données : hébergement, accès au service, journal d’audit.
8. Respect du critère « plus facile que le contenant de yogourt » : l’option choisie permet-elle un parcours quotidien presque sans friction (groupe du jour déjà sélectionné, présences rapides à cocher, brouillon retrouvé après rafraîchissement, statut « brouillon » vs « enregistré » clair, pas de ré-authentification répétée qui bloque)?

Tant que ces décisions ne sont pas prises, on ne programme pas l’application. La proposition d’algorithme d’équité (`proposition-algorithme-equite.md`) est indépendante de l’option choisie : elle décrit le calcul, pas où il tourne.
