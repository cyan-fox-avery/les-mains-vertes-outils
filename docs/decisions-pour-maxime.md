# Décisions pour Maxime — Sélecteur d’ordre de passage

**À l’attention de Maxime, pour approbation.** Ce résumé présente les points qu’Avery vous soumet avant la mise en œuvre. Rien ici n’est présenté comme approuvé par vous. Les règles déjà décidées par Avery sont dans `regles-selecteur.md`; les questions ouvertes sont dans `questions-ouvertes.md`.

## 1. Modèle d’accès : connexion d’équipe partagée (proposition)

**Proposition :** une **connexion d’équipe partagée protégée** pour le personnel autorisé à utiliser le sélecteur; les sessions restent ouvertes sur des **appareils de confiance désignés**, pour éviter les connexions quotidiennes répétées. Pas de compte / mot de passe par employé.

**Ce que cela veut dire :** avec des justificatifs partagés, on ne peut **pas** établir de façon fiable quelle personne a fait une action donnée (correction, coup de pouce, priorité, enregistrement). Les journaux conserveront les faits (action, date / heure, avant / après, versions), en étiquetant l’attribution comme une **action d’équipe** quand l’identité ne peut pas être déterminée.

**Ce que vous devez approuver :** qui peut accéder au système, quels appareils sont de confiance, et l’arrangement pratique de sécurité (expiration et révocation des sessions, rotation des justificatifs, protection des données). Si l’examen de sécurité juge la connexion partagée inappropriée, la question reviendra pour une décision éclairée — on ne substituera pas silencieusement un autre design.

## 2. Conservation des dossiers : proposition de six mois + une tension à trancher

**Proposition de travail :** **six mois** comme période de conservation initiale proposée pour les dossiers historiques de sélection. Ce n’est **pas** une politique approuvée ni immuable; vous pouvez la modifier après avoir examiné les besoins opérationnels, la confidentialité, les sauvegardes / exportations et les coûts. Rien ne sera supprimé en production sans votre confirmation.

**Tension à trancher avant toute suppression :** d’un côté, on veut purger les dossiers après six mois; de l’autre, l’équité exige de reprendre l’historique d’une personne qui revient après une longue absence, avec ses six dernières sélections comptabilisées, même si le temps civil dépasse six mois. Il faut trancher entre :
- conserver les dossiers détaillés et de vérification pendant six mois, plus un **état minimal strictement nécessaire** (six dernières sélections comptabilisées + dernière position extrême par personne et par groupe) pour l’équité / les retours — en identifiant si cet état est lui-même couvert par la limite;
- ou une autre règle de conservation respectueuse de la minimisation.

À traiter aussi : la conservation des sauvegardes et des exportations (une exportation téléchargée ne peut pas être rappelée à distance).

## 3. Sauvegardes et exportation (exigence déjà décidée par Avery)

Le système aura des **sauvegardes automatiques régulières** et une **exportation sur demande** de l’historique, pour le personnel autorisé. Votre approbation porte sur les modalités pratiques : fréquence, fournisseur, format, coûts et procédure de restauration (à vérifier en test).

## 4. Accès simultané et hors connexion (exigences déjà décidées par Avery)

- **Un seul éditeur à la fois** par sélection; les autres peuvent consulter. Reprise sécuritaire si l’éditeur se déconnecte.
- **Poursuite hors connexion** d’un tirage déjà ouvert, avec état « Hors connexion — résultat non encore synchronisé » et réconciliation attentive aux conflits.

## Ce qui n’est PAS à approuver ici

- Les règles d’équité, le mode anniversaire, les coups de pouce, les corrections et les autres comportements sont déjà décidés par Avery (voir `regles-selecteur.md`).
- Les coefficients mathématiques, le fournisseur d’hébergement et la conception technique du verrouillage restent à valider par simulations / examen technique.

---

*Document de travail — version documentation, avant programmation. Si quelque chose n’est pas clair, dites-le : c’est le moment de corriger, avant que l’outil soit programmé.*
