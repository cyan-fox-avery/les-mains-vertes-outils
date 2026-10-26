# Démonstration — Inventaire des produits

> **DÉMONSTRATION SEULEMENT — données fictives.**
>
> Cette page n’est pas l’inventaire officiel de l’atelier et ne le deviendra
> pas telle quelle : les produits, quantités et dates sont entièrement
> inventés, les modifications existent seulement dans la page, et rien
> n’est synchronisé entre appareils. Recharger la page ramène les données
> fictives de départ.

## Ouvrir la démo

Ouvrir simplement `index.html` dans un navigateur (téléphone, tablette ou
ordinateur). Aucune installation, aucune dépendance externe, aucune
compilation.

## Ce que la démo montre (spécifications V1, `docs/inventaire-produits.md`)

- Parcourir **Par type** (alimentaires / non alimentaires) ou **Par
  emplacement**, en cartes ou en liste compacte, avec recherche et filtres.
- **Dates proches** : raccourci visible qui trie par dates marquées les
  plus proches, dates dépassées d’abord.
- Détail d’un produit : total réel **calculé**, quantités par emplacement,
  lots avec les quatre états de dates distingués (Meilleur avant, Date
  d’expiration, Sans date d’expiration, Date inconnue).
- **Gérer le stock** : un seul point d’entrée pour Ajouter, Retirer,
  Déplacer et Corriger — avec suggestion du lot daté le plus ancien pour
  les retraits (dérogation possible), conservation des quantités lors des
  déplacements, et refus des retraits supérieurs au stock d’un emplacement.
- Historique léger des ajustements et bouton **Annuler** (dernier
  ajustement seulement).
- Archivage / réactivation d’un produit.
- Contenants recyclés facultatifs (dont pots de yogourt) et tailles
  approximatives; un simple nombre d’unités suffit toujours — jamais de
  ml/g obligatoires.

## Simplifications volontaires de la démo

- État **en mémoire seulement** : recharger réinitialise les données.
  Seule la préférence cartes / liste persiste (stockage local).
- **Aucun téléversement de photo** : emplacements neutres avec l’initiale
  du produit (un seul emplacement par produit, selon la spécification).
- Annulation à **un seul niveau** (dernier ajustement).
- Les sous-catégories et emplacements s’affichent comme des libellés /
  choix, sans écran d’administration complet pour les créer ou les
  renommer (volontairement petit, contre la dérive du périmètre).
- **Aucune authentification** : la question de l’accès partagé attend
  toujours l’approbation de Maxime et n’est pas simulée ici.

## Sécurité et honnêteté de la démo

- Une « Meilleur avant » dépassée est étiquetée « Meilleur avant dépassé »,
  avec la note calme qu’elle ne veut pas dire automatiquement que l’aliment
  est dangereux. Rien n’est supprimé, jeté ou déclaré dangereux
  automatiquement.
- Aucun prix, aucune vente, aucune alerte de stock faible, aucun
  code-barres, aucun tableau de bord.
