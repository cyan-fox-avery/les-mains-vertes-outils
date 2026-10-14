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

## 3. Modèles d’accès (modèle proposé, en attente de Maxime et d’un examen de sécurité)

L’architecture ne choisit pas seulement où vivent les données, mais **qui peut ouvrir l’outil et faire quoi**. **Modèle proposé (approuvé comme proposition à Maxime, pas comme autorisation définitive) :** **une connexion d’équipe partagée protégée** pour le personnel autorisé à utiliser le sélecteur; les sessions peuvent rester ouvertes sur des **appareils de confiance désignés**, minimisant les connexions quotidiennes répétées. Pas besoin que chaque employé autorisé gère son propre compte ou mot de passe. La friction de connexion quotidienne doit rester minimale.

- **Accès partagé protégé (connexion d’équipe partagée) :** simple, mais on ne sait pas qui a fait quelle modification. **Compromis explicitement accepté :** des justificatifs partagés ne peuvent pas établir de façon fiable quelle personne a fait une correction, un coup de pouce, une dérogation ou un enregistrement final. Ne pas prétendre le contraire. Les journaux conservent les renseignements fiables (action, date / heure, avant / après, versions du résultat final, métadonnées de source / appareil / session le cas échéant) et étiquettent l’attribution comme une **action d’équipe** là où l’identité ne peut pas être déterminée. **Garanties / évaluation requises :** sécurité auth / session, expiration et révocation (appareil perdu, changement d’accès), rotation des justificatifs, HTTPS et protection du stockage / accès, séparation de l’autorisation de la simple connaissance de l’URL, aucun justificatif dans GitHub, protection de l’exportation et des sauvegardes, cohérence avec un éditeur / plusieurs spectateurs et le traitement des conflits hors connexion. **Maxime doit approuver** qui peut accéder, quels appareils sont de confiance et l’arrangement pratique. Si l’examen de sécurité juge la connexion partagée inappropriée, ramener la question pour une décision éclairée plutôt que de substituer silencieusement un autre design. Voir `regles-selecteur.md` §10.4 et `docs/decisions-pour-maxime.md`.
- **Décisions confirmées :** tout membre autorisé peut corriger un résultat enregistré et donner un coup de pouce — **aucun privilège supplémentaire** (pas de permission réservée à Maxime, pas de code administrateur) pour ces actions. Raison écrite facultative pour les corrections; vérification automatique obligatoire (toutes les versions, horodatage, avant / après). Corrections à tout moment, sans limite de temps. Sous réserve de l’approbation de Maxime pour qui est autorisé à utiliser le sélecteur en général.
- **Comptes individuels (chaque membre de l’équipe a son accès) :** on sait qui a enregistré, modifié ou corrigé quoi. Plus de gestion (créer / retirer des comptes), mais meilleure traçabilité.
- **Lien protégé / code d’accès :** intermédiaire — plus simple que des comptes, mais la protection dépend du secret du lien ou du code, et il faut pouvoir le changer si le code circule.

**Point à trancher :** la traçabilité des corrections et des dérogations exige-t-elle de savoir *qui* a agi, ou suffit-il de savoir *que* c’était manuel? La réponse change le modèle d’accès.

## 4. Accès simultané — un seul éditeur, plusieurs spectateurs + reprise sécuritaire (politique confirmée, question 11 partiellement résolue)

**Décision confirmée :** seul **UN** membre / appareil peut modifier activement une sélection donnée (jour de semaine / date) à la fois. Les autres appareils autorisés peuvent consulter son état et ses résultats, mais ne doivent pas modifier, écraser, régénérer, corriger ni finaliser cette même sélection en cours. Indiquer clairement aux spectateurs que la modification est déjà en cours (« Tirage en cours sur un autre appareil » si l’identité n’est pas disponible). Empêcher les écrasements silencieux du type « dernière écriture gagne » et les doubles enregistrements finaux. **Reprise sécuritaire obligatoire :** un navigateur fermé, déconnecté ou abandonné ne doit pas bloquer définitivement le tirage du jour — un autre membre autorisé doit pouvoir reprendre le contrôle en sécurité (par exemple, bail à expiration géré par le serveur + reprise contrôlée, vérifications de version). Valider à nouveau l’autorité à l’enregistrement final; empêcher un éditeur d’origine périmé d’écraser le travail après une reprise. Aucune cérémonie quotidienne obligatoire de verrouillage / déverrouillage. S’il existe un dossier final terminé pour le jour, un autre appareil affiche ce dossier, pas un deuxième résultat officiel en conflit. Les corrections de l’historique enregistré ont aussi besoin d’une protection contre les conflits / versions.

**Reste ouvert :** la conception technique exacte du verrouillage / de la reprise et le délai d’expiration (choix d’ingénierie à tester; aucune valeur de temporisation approuvée).

**Poursuite hors connexion (exigence confirmée, question 20) :** si la connexion coupe pendant qu’un tirage est déjà ouvert, l’équipe continue cette sélection hors connexion (révélation de l’ordre pré-généré + corrections manuelles), avec brouillon et modifications conservés localement. État sans équivoque : « Hors connexion — résultat non encore synchronisé ». Ne jamais prétendre un enregistrement officiel tant que le serveur n’a pas accusé réception et validé le dossier final. À la reconnexion : validation de version / bail + synchronisation attentive aux conflits; conserver les deux copies en cas de conflit, expliquer en français simple, exiger une décision intentionnelle. **Pas deux résultats finaux officiels** pour le même jour / date. Portée : tirage déjà ouvert seulement. Reste ouvert : fournisseur de mise en cache / synchronisation, stratégie technique de résolution des conflits, examen de faisabilité.

## 5. Autres points à trancher avec l’architecture

- **Sauvegarde et récupération (exigence confirmée, question 21) :** sauvegardes AUTOMATIQUES régulières + exportation sur demande de l’historique enregistré pour le personnel autorisé; historique récupérable si l’hébergement tombe, portable en cas de changement de fournisseur. Couverture : listes, identifiants stables, ordres finaux + générés d’origine, présences, exemptions d’anniversaire, coups de pouce / priorités, corrections avec versions et horodatages, réglages. Sauvegardes **restaurables** (procédure + vérification en test). Exportation en format portable et intelligible documenté, hors du parcours quotidien, sans effet sur l’équité. Ne jamais promouvoir des brouillons locaux en attente en dossiers officiels. Reste ouvert : fréquence, fournisseur, format, outillage de restauration (faisabilité / coût + approbation de Maxime).
- **Suppression et conservation :** **Décidé :** une personne qui quitte puis revient dans le même groupe conserve son historique (identifiant interne stable); les anciens tirages restent. **Décidé :** conserver l’ordre généré d’origine + l’ordre final pour chaque sélection terminée. **Provisoire, en attente de Maxime (question 22) :** six mois proposés pour les dossiers historiques. **Tension OUVERTE :** purger à six mois vs reprendre l’historique d’une personne qui revient après une longue absence (six derniers tirages comptabilisés). Recommandation respectueuse de la minimisation requise, distinguant dossiers détaillés / vérification et état minimal de continuité, plus conservation des sauvegardes / exportations. **Aucune suppression en production sans confirmation de Maxime.** Voir `regles-selecteur.md` §10.5 et `docs/decisions-pour-maxime.md`.
- **Fonctionnement sans connexion :** voir §4 (poursuite hors connexion, exigence confirmée).
- **Coût et maintenance :** qui paie (s’il y a un coût)? Qui est prévenu si le service tombe? Qui corrige si quelque chose brise?
- **Protection des données :** où sont hébergées les données (pays)? Qui a accès au service d’hébergement, en plus de l’équipe? Les prénoms seuls réduisent le risque, mais l’historique des présences reste une donnée sensible à protéger.
- **Journal d’audit :** quelles actions consigne-t-on (priorités, modifications, dérogations, corrections)? Pour chaque action, consigne-t-on la date, l’heure et, selon le modèle d’accès, la personne? **Décidé :** les corrections conservent toutes les versions, l’horodatage et les détails avant / après (raison écrite facultative); les coups de pouce réellement actifs sont enregistrés (à qui, pour quel tirage); l’auteur seulement si le modèle d’accès le permet vraiment.

## 6. Liste des décisions : tranchées vs à prendre (pour la discussion)

**Tranchée :** option d’architecture = **A** (site statique + base de données hébergée, éventuellement fonctions serveur gérées), sous réserve d’une évaluation réaliste de l’hébergement, de la confidentialité, de l’accès, des sauvegardes / exportations et de la protection contre les écrasements concurrents.

**Tranchées (suite) :**

- Accès simultané : un seul éditeur, plusieurs spectateurs + reprise sécuritaire (question 11, politique réglée; conception technique / délai ouverts).
- Corrections : tout membre autorisé; raison écrite facultative; aucune limite de temps; toutes les versions conservées, vérification automatique (question 7, résolue).
- Coups de pouce : tout membre autorisé, sans privilège supplémentaire; raison non applicable (question 18, permission réglée).
- Conservation : ordre généré d’origine + ordre final conservés (question 15, résolue); identifiant interne stable par personne (question 16, résolue); nom usuel + initiale si collision (question 13, résolue).
- Accès : connexion d’équipe partagée proposée, en attente de Maxime / examen de sécurité (question 10, proposition approuvée).
- Poursuite hors connexion d’un tirage déjà ouvert (question 20, exigence réglée; détails techniques ouverts).
- Sauvegardes automatiques + exportation sur demande (question 21, exigence réglée; détails opérationnels ouverts).
- Conservation : six mois proposés, en attente de Maxime; tension conservation / continuité OUVERTE (question 22, provisoire).
- « Comment ça fonctionne? » : 1–2 pages + page distincte « L’essentiel en bref » (question 17, résolue).
- Page de statistiques d’équité facultative approuvée (question 12, résolue).

**À prendre :**

1. Fournisseur, base de données, schéma d’authentification, région d’hébergement — aucun choix fait.
2. Modèle d’accès définitif — proposition approuvée : connexion d’équipe partagée, **en attente de Maxime / examen de sécurité** — et ce que ça implique pour la traçabilité (attribution « action d’équipe » là où l’identité ne peut pas être déterminée).
3. Conception technique du verrouillage / de la reprise + délai d’expiration (à tester).
4. Sauvegarde, exportation : fréquence, fournisseur, format, outillage de restauration. Conservation : réconciliation conservation / continuité + approbation de Maxime (question 22).
5. Fonctionnement sans connexion : stratégie technique de synchronisation + fournisseur de mise en cache (question 20).
6. Coût, hébergement, maintenance, et qui est responsable de chaque point.
7. Protection des données : hébergement, accès au service, journal d’audit.
8. Respect du critère « plus facile que le contenant de yogourt » : l’option choisie permet-elle un parcours quotidien presque sans friction (groupe du jour déjà sélectionné, présences rapides à cocher, brouillon retrouvé après rafraîchissement, statut « brouillon » vs « enregistré » clair, pas de ré-authentification répétée qui bloque)?

Tant que ces décisions ne sont pas prises, on ne programme pas l’application. La proposition d’algorithme d’équité (`proposition-algorithme-equite.md`) est indépendante de l’option choisie : elle décrit le calcul, pas où il tourne.
