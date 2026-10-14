# Les Mains Vertes — Outils

Outils internes de l’Atelier Les Mains Vertes.

Ce dépôt va héberger, à terme, plusieurs petits outils de travail pour l’atelier. Le premier outil, c’est le **sélecteur d’ordre de passage** : un tirage au sort juste et transparent qui détermine l’ordre dans lequel les personnes participantes choisissent leur tâche du jour.

> **État actuel : documentation seulement.**
>
> Ce dépôt ne contient pour l’instant aucune application. La première demande de tirage (*pull request* nº 1) documente les règles convenues, avant toute programmation. On établit les règles d’abord, on choisit l’architecture ensuite, on programme après.

## Pourquoi on fait ça

En ce moment, l’ordre de choix des tâches est tiré avec des petits papiers dans un contenant de yogourt réutilisé.

Le tirage est au hasard, mais le hasard pur crée des injustices : une personne peut passer première plusieurs fois, pendant qu’une autre se retrouve souvent à choisir parmi les dernières tâches qui restent. Les membres de l’équipe corrigent parfois les résultats à la main pour éviter ça.

Le but, c’est de remplacer le contenant de yogourt par un système numérique simple et transparent qui garde le hasard, mais qui améliore l’équité au fil du temps.

## Ce que l’outil fait — et ce qu’il ne fait pas

**Il fait :**

- Il détermine **l’ordre** dans lequel les personnes choisissent leur tâche.
- Il tient compte des tirages passés pour réduire les désavantages répétés.
- Il permet de noter les présences, les priorités et le résultat final.

**Il ne fait pas :**

- Il n’attribue pas les tâches lui-même. Chaque personne choisit sa tâche quand son tour arrive.
- Il ne décide pas qui doit faire quoi.
- Il ne remplace pas le jugement de l’équipe : l’équipe peut modifier l’ordre et doit enregistrer le résultat final.

Les premières places sont avantageuses, parce qu’il reste plus de tâches à choisir. C’est pour ça que l’équité de l’ordre compte autant.

## Premier outil : le sélecteur d’ordre de passage

### En bref

1. On choisit le groupe du jour (lundi, mardi, mercredi ou jeudi).
2. On coche les présences du jour.
3. On indique les priorités de passage, s’il y en a (maximum de trois).
4. On lance le tirage au sort.
5. On affiche l’ordre complet, ou on révèle les noms un à un.
6. On modifie l’ordre au besoin pour refléter ce qui s’est vraiment passé.
7. On enregistre le résultat final. C’est ce résultat final qui compte pour les tirages suivants.

### Principes

- **Hasard + mémoire.** Le tirage reste aléatoire, mais il tient compte des résultats précédents pour éviter que les mêmes personnes passent toujours en dernier.
- **Transparence.** L’équipe voit l’ordre, peut le modifier et doit le confirmer. On garde une trace de ce qui s’est vraiment passé, pas seulement de ce que l’outil avait proposé au départ.
- **Simplicité.** L’outil doit être utilisable avec un minimum de formation, sur téléphone, tablette et ordinateur.
- **Accessibilité.** Libellés clairs, texte lisible, grosses zones de touché, navigation simple.
- **Respect de la vie privée.** On ne conserve que les prénoms. Les données des personnes participantes et l’historique des présences restent en dehors du code source public, avec une protection d’accès raisonnable.

## Documentation

Tout le contenu destiné aux personnes qui utilisent l’outil est écrit en français québécois naturel.

| Fichier | Contenu |
| --- | --- |
| `docs/regles-selecteur.md` | Règles fonctionnelles détaillées et comportements convenus. C’est le document de référence pour programmer et tester l’outil. |
| `docs/questions-ouvertes.md` | Décisions qui restent à prendre. Ces questions sont volontairement séparées des règles convenues. Rien dans ce fichier ne doit être lu comme déjà décidé. |
| `docs/guide-equipe.md` | Guide court (une à deux pages) pour Max et l’équipe : ce que l’outil fait, comment l’utiliser, et comment le tirage reste juste. Sans jargon technique. |

## Logo

Le logo officiel de l’Atelier Les Mains Vertes apparaîtra dans l’en-tête ou dans un coin de l’outil. Avery fournira le logo. Aucun logo de remplacement ne sera généré ni inventé.

## Stockage partagé (orientation, sans engagement)

Avery souhaite un système partagé et synchronisé, accessible par plusieurs membres de l’équipe à partir de différents appareils.

Une solution sur un seul appareil resterait acceptable si le stockage partagé ajoute une complexité disproportionnée, mais le stockage partagé est la direction privilégiée.

Aucune base de données, aucun fournisseur d’authentification ni aucune plateforme d’hébergement n’est choisie pour l’instant. Les options techniques seront documentées sans engagement lors de la prochaine étape (architecture).

## Prochaines étapes

1. Relire et corriger la documentation de la demande de tirage nº 1.
2. Trancher les questions ouvertes qui bloquent l’architecture ou l’algorithme d’équité.
3. Documenter les options d’architecture (stockage partagé, accès, appareils multiples) sans s’engager trop tôt.
4. Programmer ensuite, en commençant par un prototype simple.

## Contribuer

Pour l’instant, le travail passe par les demandes de tirage (*pull requests*) sur ce dépôt, avec relecture par Avery avant toute fusion. On ne programme pas dans la demande de documentation nº 1 : on s’entend d’abord sur les règles.
