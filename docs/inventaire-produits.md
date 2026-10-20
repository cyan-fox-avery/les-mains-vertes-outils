# Utilitaire nº 2 : Inventaire des produits — Spécifications V1

> **Statut : spécifications convenues par Avery et Mira (2026-10-20).**
>
> Ce document versionne le mémoire de conception déposé par Mira sur la
> demande nº 9. Il décrit le **deuxième utilitaire** du site Les Mains
> Vertes : un inventaire de **produits finis physiques fabriqués à
> l’atelier**, pas une plateforme de vente et pas un catalogue de
> documents ou de sauvegardes.
>
> **Gel de périmètre V1 :** tout ce qui est listé à la section 12 est
> explicitement hors V1. Les ajouts futurs font l’objet d’une discussion
> distincte; on ne les glisse pas silencieusement dans V1.
>
> **Séparation stricte :** cet inventaire vit **à côté** du sélecteur
> d’ordre de passage, pas dedans. Il ne perturbe ni l’outil du tirage du
> matin, ni les demandes liées à l’équité. L’administration des données du
> sélecteur (historique des tirages, statistiques, sauvegardes) reste une
> discussion future distincte — elle ne fait pas partie de ce document.

## 1. But et simplicité non négociable

L’inventaire répond vite à trois questions :

1. Qu’est-ce qu’on a en ce moment, et en quelle quantité?
2. Où est-ce rangé physiquement?
3. Quelles dates marquées approchent?

**Avertissement d’Avery, à respecter :** pas de dérive du périmètre, pas
de forêt de boutons. L’outil doit être **plus facile qu’une feuille
d’inventaire papier**. Termes reconnaissables, actions rapides, grandes
zones tactiles sur téléphone et tablette, utilisation confortable sur
ordinateur.

Tout ce que le personnel voit est en **français québécois naturel**.

## 2. Périmètre, accès et séparation

- **V1 = produits finis seulement.** Les ingrédients, les emballages vides
  et les fournitures de production sont reportés. On laisse la place à une
  future extension « matières premières » sans la programmer maintenant.
- **Même accès d’équipe autorisée** que le reste du site : tout le
  personnel autorisé peut consulter et modifier le stock. On réutilise
  l’authentification protégée éventuelle du site; on ne crée **pas** un
  deuxième jeu de comptes.
- L’approche de connexion d’équipe partagée a **toujours besoin de
  l’approbation réelle de Maxime et d’une validation de sécurité** : on
  ne la déploie pas comme si elle était approuvée.
- La simplicité de l’interface n’excuse ni la perte de données, ni les
  modifications concurrentes dangereuses, ni les confirmations
  d’enregistrement trompeuses.

## 3. Catalogue et façons de parcourir

Chaque produit distinct a **une seule fiche produit**, peu importe le
nombre de lots, les types de contenants recyclés ou les formats.

Métadonnées d’une fiche :

- nom du produit (**obligatoire**);
- classe comestible / non comestible (**obligatoire**);
- sous-catégorie facultative et modifiable;
- **une seule photo représentative facultative** (voir §9);
- statut actif / archivé;
- total de stock **calculé** (jamais saisi à la main comme un total
  indépendant).

**Deux façons indépendantes de parcourir les mêmes fiches :**

- **Par type :** Produits alimentaires vs Produits non alimentaires;
  sous-catégories facultatives et modifiables (confitures, marinades,
  sauces, savons, détergents, déodorants, etc.).
- **Par emplacement :** parcours par lieux de rangement physiques
  configurables dans le bâtiment; un produit peut avoir du stock à
  plusieurs endroits, **sans double comptage**.

**Deux modes de présentation,** avec bascule facile : cartes visuelles
(photo facultative) et tableau / liste compact. Mémoriser la présentation
préférée de l’appareil localement, quand c’est pratiquement faisable.

- Tri par défaut : **alphabétique**.
- Raccourci **Dates proches** bien visible dans **les deux** vues, plus
  recherche de produit et filtres sensés : comestible / non comestible,
  sous-catégorie, emplacement, rupture de stock.
- Ne pas enterrer le tri par date dans les réglages.

## 4. Lots et état des dates

- On suit les **lots de production individuels**, même quand la plupart
  des produits ne sont fabriqués qu’un à la fois; on affiche un seul
  total combiné par produit.
- La **date de production** est l’identifiant principal lisible par un
  humain pour un lot; un **nom / description manuscrit facultatif** est
  permis.
- **Aucun code de lot public obligatoire** (pas de FRA-001 imposé). Des
  identifiants internes stables et discrets sont permis, et nécessaires.
- Chaque lot peut porter une **Meilleur avant**, une **Date
  d’expiration** quand c’est pertinent, **Sans date d’expiration**, ou
  une **date pas encore saisie / inconnue**. Les deux derniers cas
  doivent être **distinguables** l’un de l’autre.
- Un lot à contenants mélangés partage son propre dossier de production /
  dates, sans prétendre que tous les contenants ont la même taille.
- Alertes de dates **ajustables**, période d’avertissement par défaut de
  **30 jours**. Distinguer : normal, qui approche, date passée, sans
  expiration confirmée, date inconnue.
- **Une « Meilleur avant » passée ne veut PAS dire automatiquement que
  l’aliment est dangereux.** Étiqueter clairement ce que la date
  représente; ne jamais supprimer, jeter ou déclarer dangereux
  automatiquement.
- **Aucune alerte de stock faible en V1**; les quantités sont modestes.

## 5. Contenants recyclés et formats

L’atelier utilise les emballages recyclés disponibles : pots de yogourt,
bocaux, bouteilles, sacs, boîtes ou contenants inhabituels. Un seul lot
peut en mélanger plusieurs.

- Type de contenant **facultatif** (préréglages modifiables + « Autre »).
- Taille **approximative facultative** (par exemple : très petit, petit,
  moyen, grand, très grand).
- Capacité **exacte facultative**, si elle est réellement connue.
- Format **non précisé** possible.
- **Ne jamais exiger de mesures précises en ml / g** pour enregistrer du
  stock.
- Surtout : le personnel peut saisir **un simple nombre d’unités** sans
  remplir les détails de contenants.
- On compte les unités finies réelles et on garde des variantes
  sensées au besoin, plutôt que de fabriquer un volume exact.

## 6. Emplacements physiques configurables

- Exemples de départ — **pas des étiquettes réelles supposées** :
  Garde-manger alimentaire / Garde-manger non alimentaire / Réserve /
  Armoire. Le personnel crée, renomme et entretient les emplacements
  réels.
- Suivre les **quantités exactes à chaque emplacement**, même quand un
  seul lot s’étend sur plusieurs endroits. Exemple : un lot de
  20 contenants = 12 au garde-manger, 8 à la réserve.
- L’emplacement peut être **non précisé lors d’une saisie rapide** et
  rempli plus tard.
- **Conservation des quantités (règle d’or) :** le total d’un lot / produit
  égale la somme des quantités situées **plus** les quantités à
  emplacement non précisé. Jamais plusieurs totaux modifiables
  indépendamment.

## 7. Un seul point d’entrée évident : « Gérer le stock »

Pas de forêt de boutons. Les actions quotidiennes se regroupent sous une
seule commande claire, **Gérer le stock**, pour un produit. Un parcours
d’**ajout rapide** facile à trouver, avec des champs facultatifs qui ne
bloquent jamais l’utilisation.

### Ajouter

- Choisir un produit et un lot existants, ou créer un nouveau lot.
- Saisir la quantité en unités; date, emballage et emplacement facultatifs.
- Créer un tout nouveau produit **à partir du même parcours**, sans
  chercher dans des menus.

### Retirer

- Saisir la quantité retirée; **aucun motif obligatoire en V1**.
- Suggérer de prendre d’abord dans le **lot daté pertinent le plus
  ancien**, mais permettre de choisir un autre lot, parce que le personnel
  peut physiquement prendre un autre stock.
- Distinguer les lots sans expiration confirmée et les lots à date
  inconnue; ne pas sélectionner automatiquement un lot à date passée pour
  un usage ordinaire sans une décision claire du personnel.
- Respecter les variantes d’emplacement / contenant réellement
  disponibles; ne jamais soustraire silencieusement du mauvais rayon ni
  créer de quantités négatives. Gérer visiblement les cas qui s’étendent
  sur plusieurs lots.

### Déplacer

- Parcours de transfert dédié, d’un emplacement à un autre.
- La quantité est soustraite de la source et ajoutée à la destination
  **en une seule opération**, qui préserve le total; ce n’est pas un
  retrait suivi d’une nouvelle production.

### Corriger

- Réconciliation avec le comptage physique : le personnel saisit la
  quantité réellement sur l’étagère.
- Garder la quantité précédemment enregistrée et le périmètre modifié
  (lot, variante, emplacement) dans l’historique.

## 8. Historique, simultanéité et annulation

- Conserver automatiquement un historique léger des ajustements : quand,
  produit, lot, opération, quantités avant / après, emplacements touchés,
  toute correction / annulation. **Aucun motif écrit obligatoire**, et
  aucune fausse affirmation d’identité individuelle sous un justificatif
  partagé.
- Offrir une commande **Annuler** immédiate après un ajustement, et un
  moyen de corriger des erreurs plus anciennes sans effacer le dossier.
- **Sécurité en simultané :** une annulation ne peut inverser en sécurité
  qu’une modification admissible; elle ne doit jamais écraser
  silencieusement une modification plus récente faite par une autre
  personne. Tout conflit doit être expliqué clairement.
- Un prototype peut utiliser des données de démonstration isolées; ne pas
  présenter un stockage local à un seul appareil comme un inventaire
  officiel multi-appareils.

## 9. Photos

- **Une seule photo représentative facultative PAR PRODUIT**, pas par lot,
  emplacement ou contenant.
- Remplacer la photo précédente quand elle change, plutôt que d’en
  accumuler des centaines.
- Redimensionner / compresser les téléversements et protéger le
  stockage; utiliser un espace réservé neutre et accessible quand il n’y
  a pas de photo.
- La photo n’est pas requise pour une saisie rapide de stock.

## 10. Archivage

- Archiver les produits abandonnés / saisonniers plutôt que de les
  supprimer définitivement.
- Cacher les produits archivés de la navigation normale; permettre la
  restauration / réactivation.
- Conserver l’historique sous réserve d’une politique approuvée à venir.
- **Une rupture de stock seule n’archive PAS automatiquement un produit.**

## 11. Tests d’acceptation UX de V1

Une personne qui ne connaît pas le code doit pouvoir, confortablement sur
téléphone ou tablette :

1. Chercher un produit et voir son **total réel**.
2. Voir exactement **quels emplacements physiques** détiennent son stock,
   et en quelles quantités.
3. Parcourir **Par type** ou **Par emplacement**, et basculer entre
   cartes et tableau.
4. Trouver les dates marquées les plus proches grâce à un tri **Dates
   proches** évident, et distinguer correctement sans-expiration et date
   inconnue.
5. Ajouter un nouveau lot d’un produit connu **rapidement**, même avec
   des contenants mélangés ou de taille inconnue.
6. Créer un nouveau produit rapidement quand il n’est pas au catalogue.
7. Retirer un petit nombre d’unités avec une suggestion sensée du lot le
   plus ancien et une dérogation claire.
8. Transférer du stock entre emplacements **sans modifier les totaux**.
9. Corriger un comptage physique et annuler une erreur en sécurité.
10. Archiver et réactiver un produit sans perdre son dossier.

Utiliser des **noms de produits et des quantités fictifs** dans les
exemples et la démonstration, pas de vrais dossiers privés de l’atelier.

## 12. Explicitement HORS V1

- Ingrédients / matières premières; stock d’emballages; recettes et
  procédés de fabrication.
- Ventes, prix, revenus, dons et suivi obligatoire des motifs de retrait.
- Alertes de stock faible et tableaux de bord / rapports arbitraires.
- Plusieurs photos par lot / contenant.
- Numérotation formelle obligatoire des lots.
- Lecteurs de codes-barres.
- Analytique prédictive et notifications externes.
- Toute navigation ou bouton d’administration supplémentaire ajouté juste
  parce que la mise en œuvre semble facile.

## 13. Séquence de construction et de relecture

1. **D’abord :** corriger le périmètre de cette demande et versionner ces
   spécifications, y compris le gel V1 (le présent document).
2. **Ensuite :** une **démonstration minimale cliquable, pensée
   téléphone d’abord**, avec du stock fictif, les deux modes de parcours,
   les vues cartes / tableau, un tri de dates clair, et des parcours
   simples de produit / lot et d’ajustement rapide.
3. **Ensuite :** les opérations d’inventaire, lots / variantes,
   conservation par emplacement, historique des modifications / annulation
   sécuritaire, archivage, persistance en environnement de test.
4. **Plus tard, pour la production :** accès sécurisé partagé,
   synchronisation multi-appareils à l’épreuve des conflits,
   sauvegarde / récupération, décisions pratiques de conservation,
   autorisation de Maxime, tests avec la vraie équipe.

Ne pas attendre les coefficients numériques finaux de l’algorithme
d’équité pour commencer un prototype d’inventaire séparé; ne pas livrer
une maquette locale comme une base de données synchronisée prête pour le
travail.

**Critère de réussite :** un membre du personnel des Mains Vertes peut
trouver et mettre à jour le stock physique avec peu ou pas de formation,
sans naviguer dans un mur de boutons.
