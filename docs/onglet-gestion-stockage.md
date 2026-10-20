# Deuxième onglet (proposé) : Gestion du stockage

> **Statut : PROPOSITION — pas des règles décidées.**
>
> Ce document propose un deuxième onglet pour l’application, à côté du
> sélecteur d’ordre de passage. Il ne fait que **rassembler, en un seul
> endroit, des fonctions déjà décidées** ailleurs dans les règles, et poser
> les questions nouvelles que ce regroupement soulève.
>
> Rien ici ne doit être lu comme déjà décidé, ni programmé comme si c’était
> réglé. Les renvois vers `regles-selecteur.md` désignent les décisions
> existantes; tout le reste est une proposition en attente de relecture par
> Mira et de décision par Avery (et, pour l’accès et la conservation, par
> Maxime).
>
> Libellé de travail de l’onglet : **« Gestion du stockage »**, à valider
> avec l’équipe. Si ce libellé sonne trop technique pour le personnel, un
> libellé comme « Données et sauvegardes » serait plus clair — à trancher
> (voir question 23).

## 1. Pourquoi un deuxième onglet

Le parcours quotidien doit rester presque sans friction : ouvrir le site,
cocher les absences, lancer le tirage, enregistrer le résultat final
(`regles-selecteur.md` §13 — plus facile que le contenant de yogourt).

Plusieurs fonctions déjà décidées doivent pourtant exister quelque part,
**loin du parcours quotidien ordinaire** (`regles-selecteur.md` §9.2) :

- consulter les résultats enregistrés passés;
- corriger un résultat enregistré;
- consulter les statistiques d’équité;
- gérer les listes de personnes;
- exporter l’historique et vérifier les sauvegardes;
- comprendre ce qui est conservé, et pour combien de temps.

Aujourd’hui, ces fonctions sont décrites aux quatre coins des règles. La
proposition, c’est de les réunir dans un seul onglet, **« Gestion du
stockage »**, à côté de l’onglet du sélecteur. Le personnel sait où aller
quand il ne fait pas le tirage du jour, et le tirage du jour reste simple.

Cet onglet n’est **pas** un deuxième outil : il fait partie de la même
application. Il ne tire pas au sort et n’attribue pas de tâches.

## 2. Ce que l’onglet contient (proposé)

Chaque rubrique ci-dessous reprend une exigence déjà décidée; l’onglet ne
fait que lui donner une place. Les détails nouveaux sont signalés comme
propositions.

### 2.1 Historique des résultats

- Consulter les résultats enregistrés passés, par groupe du jour
  (`regles-selecteur.md` §8.2).
- Dans le détail d’un résultat passé, voir ensemble **l’ordre généré
  d’origine et l’ordre final enregistré**, avec une indication
  compréhensible de ce qui a changé (§7.3). Seul l’ordre final sert à
  l’équité future; le brouillon d’origine sert à la transparence.
- Les propositions écartées ou les brouillons non enregistrés ne sont **pas**
  des résultats officiels et ne doivent jamais apparaître comme tels.

### 2.2 Statistiques d’équité

- La page facultative de statistiques / aperçu de l’historique d’équité,
  déjà approuvée (§8.3), vit dans cet onglet, loin du sélecteur quotidien.
- Elle montre comment les occasions ont été réparties (par exemple, des
  comptes de places en première moitié vs en deuxième moitié), à partir
  des résultats réellement enregistrés.
- Elle ne doit **pas** ressembler à une évaluation du rendement ni classer
  les personnes par mérite. Elle distingue correctement les absences, les
  pauses d’anniversaire, les séances uniques exclues et les priorités /
  modifications manuelles enregistrées.

### 2.3 Listes de personnes

- Ajouter, renommer, retirer et réactiver des personnes, par groupe du jour
  (§2.3).
- Retirer quelqu’un de la liste active la rend inactive pour les tirages
  futurs; cela ne supprime ni ses dossiers enregistrés ni son identité.
  Une personne qui revient dans le **même** groupe retrouve son historique
  d’équité existant, grâce à un identifiant interne stable.
- Corriger un nom ne doit jamais créer une nouvelle identité ni orpheliner
  l’historique antérieur.
- Prénoms identiques : utiliser le nom usuel préféré; seulement quand deux
  noms d’affichage seraient identiques dans le même groupe, distinguer par
  une initiale inscrite / confirmée par l’équipe (jamais devinée, jamais
  « Alex 1 » / « Alex 2 »). Aucun nom de famille ni autre détail personnel
  au-delà de ce qui est nécessaire pour les initiales de distinction.

### 2.4 Corrections des résultats enregistrés

- Corriger un résultat final déjà enregistré (§7.4), avec conservation de
  **toutes** les versions antérieures, de la date / heure de chaque
  correction et de ce qui a changé.
- Raison écrite **facultative**, jamais une condition préalable.
  **Aucune limite de temps** fondée sur l’âge du dossier (sous réserve de
  la résolution de la tension de conservation, voir §2.6).
- Tout membre autorisé de l’équipe peut corriger; aucune permission
  réservée à Maxime pour la seule correction (sous réserve de
  l’approbation de Maxime pour l’accès au sélecteur en général).
- L’ordre corrigé sert aux calculs futurs. On ne fait **pas** de nouveau
  tirage rétroactif des séances passées.
- Avec des justificatifs d’équipe partagés, ne pas prétendre à une
  attribution individuelle : enregistrer au moins l’événement, l’horodatage
  et les détails avant / après, et étiqueter l’action comme une
  **action d’équipe** là où l’identité ne peut pas être déterminée.

### 2.5 Sauvegardes et exportation

- L’onglet est l’endroit où l’équipe autorisée trouve l’**exportation sur
  demande** de l’historique enregistré (§10.3) — hors du parcours
  quotidien, sans effet sur l’équité ni sur l’état enregistré.
- **Proposition :** l’onglet affiche aussi l’état des sauvegardes
  automatiques, par exemple la date de la dernière sauvegarde automatique
  réussie, pour que l’équipe n’ait pas à « croire » que ça fonctionne.
  La fréquence exacte, le fournisseur et l’outillage restent ouverts
  (voir question 21).
- Les sauvegardes couvrent l’état opérationnel réel : listes et
  identifiants stables, ordres finaux confirmés + ordres générés d’origine,
  présences, exemptions d’anniversaire, coups de pouce / priorités,
  corrections avec versions et horodatages, réglages (§10.3).
- Les sauvegardes doivent être **restaurables** (procédure de récupération
  + vérification en test), pas seulement créées.
- **Garde-fou :** les sauvegardes ne doivent jamais promouvoir des
  brouillons locaux en attente non synchronisés en dossiers officiels
  enregistrés.
- **Sécurité :** accès restreint au personnel autorisé; aucun nom, présence
  ou historique publié ou validé dans GitHub / le code source; format
  d’exportation portable et intelligible, documenté.

### 2.6 Conservation des dossiers

- **Proposition :** l’onglet indique, en langage simple, ce qui est
  conservé et la proposition actuelle (six mois, **provisoire, en attente
  de Maxime** — §10.5). Il ne présente pas six mois comme une politique
  approuvée immuable.
- **Tension ouverte, rappelée dans l’onglet :** « corriger à tout moment »
  doit être réconcilié avec une purge éventuelle à six mois; les
  historiques doivent reprendre pour les personnes qui reviennent après de
  longues absences, avec leurs six derniers tirages **comptabilisés**, même
  si le temps civil dépasse six mois.
- **Aucune action destructive** (suppression, purge) ne doit être offerte
  ou exécutée dans l’onglet avant une résolution transparente de cette
  tension, avec confirmation de Maxime. Une exportation téléchargée ne peut
  pas être rappelée à distance : l’onglet doit le dire simplement quand il
  propose une exportation.
- Voir questions 22 et 26.

### 2.7 État de synchronisation

- Quand une sélection est en attente de synchronisation, l’onglet doit
  refléter le même état que l’écran quotidien, sans équivoque : par
  exemple « Hors connexion — résultat non encore synchronisé » (§10.2).
- **Ne JAMAIS prétendre qu’un résultat est officiellement enregistré**
  tant que le serveur n’a pas accusé réception et validé le dossier final.
- En cas de conflit à la reconnexion, conserver les deux copies, expliquer
  en français québécois simple, et exiger une décision intentionnelle.
  **Pas deux résultats finaux officiels** pour le même jour / date.

## 3. Accès à l’onglet (proposé, sous réserve de Maxime)

- **Proposition :** l’onglet est accessible à tout membre autorisé de
  l’équipe qui est autorisé à faire fonctionner le sélecteur. Il ne crée
  **aucun** privilège supplémentaire par lui-même — sauf si Maxime décide
  autrement pour certaines actions (voir question 24).
- Le modèle d’accès proposé pour l’ensemble de l’application — une
  connexion d’équipe partagée protégée, sessions pouvant rester ouvertes
  sur des appareils de confiance désignés — reste une **proposition à
  Maxime, pas une autorisation définitive** (§10.4).
- La règle **un seul éditeur, plusieurs spectateurs** (§10.1) s’applique
  aussi aux modifications faites depuis cet onglet : si un autre appareil
  modifie déjà une sélection, l’onglet l’indique simplement, par exemple
  « Tirage en cours sur un autre appareil », et n’autorise pas
  d’écrasement silencieux.
- Comme pour le reste de l’application : **on ne conserve que les
  prénoms**, et les données restent en dehors du code source, avec une
  protection d’accès raisonnable.

## 4. Ce que l’onglet ne fait pas

- Il ne lance pas le tirage du jour et ne remplace pas l’onglet du
  sélecteur.
- Il n’attribue pas les tâches et ne décide pas qui doit faire quoi.
- Il ne classe pas les personnes selon leur rendement.
- Il ne publie rien à l’extérieur de l’atelier.
- Il ne supprime rien silencieusement : aucune purge, aucun effacement
  d’historique sans décision explicite, traçable, et conforme à la politique
  de conservation une fois résolue.
- Il n’ajoute aucune friction au parcours quotidien : tout ce qui vit ici
  reste **hors du chemin du tirage du matin** (§13).

## 5. Cohérence avec le critère du contenant de yogourt

L’onglet de gestion ne doit pas servir d’excuse pour compliquer le
sélecteur. La règle reste la même : le tirage du matin doit être plus
facile et plus intuitif que les petits papiers. Regrouper l’administration
ici, c’est précisément ce qui permet de garder l’écran quotidien épuré :
la complexité vit dans cet onglet, accessible au besoin, jamais imposée
au quotidien.

Comme pour le reste de l’application : tout ce que le personnel voit est
en français québécois naturel, avec des libellés clairs, une typographie
lisible et de grandes zones tactiles. L’onglet doit être confortable sur
téléphone, tablette et ordinateur.

## 6. Questions nouvelles soulevées par cet onglet

Voir `questions-ouvertes.md`, questions 23 à 26 :

- **Q23 :** contenu exact et libellé de l’onglet (« Gestion du stockage »
  ou autre chose?).
- **Q24 :** qui peut utiliser l’onglet — même accès que le sélecteur, ou
  accès restreint pour certaines actions?
- **Q25 :** que montre l’aperçu du stockage (comptes, dates, état des
  sauvegardes) sans exposer inutilement des données?
- **Q26 :** qui peut supprimer un dossier, avec quelle confirmation, et
  seulement après quelle résolution de la conservation?
