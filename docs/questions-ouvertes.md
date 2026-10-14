# Questions ouvertes

> **Lisez-moi d’abord.**
>
> Ce fichier liste les décisions qui **ne sont pas encore prises**. Rien ici ne doit être lu comme déjà décidé, ni programmé comme si c’était réglé.
>
> Quand une question est tranchée, on la déplace dans `regles-selecteur.md` avec la décision et sa date, et on retire la question d’ici.

## 1. Formule de pondération exacte

**Question :** Quelle formule de pondération utiliser, et avec quelle force compenser les places tardives passées?

**Pourquoi ça compte :** C’est le cœur de l’outil. Une compensation trop faible ne change presque rien; une compensation trop forte transforme le tirage en rotation prévisible et détruit le hasard.

**Pistes à évaluer (sans en choisir une) :**

- Pondération linéaire sur la position moyenne normalisée des derniers tirages.
- Pondération exponentielle (les écarts comptent plus que proportionnellement).
- Plafond du ratio entre la plus forte et la plus faible pondération (par exemple, personne ne peut avoir plus de 2 ou 3 fois les chances d’une autre), pour préserver le hasard.
- Pondération différente selon que la personne a été très souvent en fin de liste vs légèrement en dessous de la moyenne.

**Ce qu’il faudra décider :** la formule, la force, le plafond éventuel, et la façon de la tester par simulations (voir question 9).

## 2. Normalisation des positions historiques

**Question :** Comment normaliser une position quand la taille du groupe varie d’un tirage à l’autre?

**Pourquoi ça compte :** Être 10e sur 10 n’est pas la même chose qu’être 10e sur 14. Si on compare des positions brutes sans normaliser, les petits groupes faussent le calcul.

**Pistes à évaluer (sans en choisir une) :**

- Position normalisée = (place − 1) / (nombre de personnes présentes − 1), ce qui donne 0 pour la première place et 1 pour la dernière.
- Percentile ou rang relatif.
- Ajustement différent pour les très petits groupes.

**Ce qu’il faudra décider :** la formule de normalisation et son comportement quand le groupe est très petit (1 ou 2 personnes).

## 3. Fenêtre d’historique

**Question :** Sur combien de tirages passés calcule-t-on l’équité? Et que veut dire « derniers tirages » quand une personne s’est absentée?

**Point de départ discuté (proposition seulement) :** environ les six derniers tirages auxquels la personne a assisté.

**Ce qu’il faudra décider :**

- Le nombre exact (6? autre chose?).
- Est-ce qu’on compte les six derniers tirages **du groupe** (avec des trous quand la personne était absente) ou les six derniers tirages **où la personne était présente**?
- Est-ce que les tirages récents comptent plus que les plus anciens, ou est-ce que chaque tirage de la fenêtre compte également?
- Que fait-on pour une personne nouvelle qui n’a pas encore d’historique (pas de désavantage, pas d’avantage indu)?

## 4. « Consécutive » : que veut dire deux sélections de suite?

**Question :** Comment interpréter les règles « pas deux fois première de suite » et « pas deux fois dernière de suite » quand quelqu’un manque une ou plusieurs semaines?

**Exemple :** Léa est première le mardi 6 octobre. Elle est absente le mardi 13 octobre. Peut-elle être première le mardi 20 octobre?

**Interprétations possibles (sans en choisir une) :**

- **A — Tirages du groupe :** on regarde les deux derniers tirages du groupe, peu importe si la personne était présente. Le tirage du 13 octobre a eu lieu entre les deux, même sans Léa : le 6 et le 20 ne sont donc pas deux tirages consécutifs du groupe. Léa **pourrait** être première le 20 sous cette interprétation.
- **B — Tirages où la personne était présente :** on regarde les deux derniers tirages où la personne a participé. Le 6 et le 20 sont consécutifs **pour Léa** (elle n’a participé à aucun tirage entre les deux). Léa **ne pourrait pas** être première le 20 sous cette interprétation.
- **C — Semaines civiles consécutives :** seules deux semaines de suite, sans absence entre les deux, comptent comme consécutives. Une absence « brise » la séquence.

**Ce qu’il faudra décider :** une seule définition, appliquée partout de la même façon, pour la première et la dernière place.

## 5. Ordre de priorité quand les règles entrent en conflit

**Question :** Quand il est impossible de respecter toutes les règles d’équité en même temps, laquelle on relâche en premier?

**Pourquoi ça compte :** Dans le cas ordinaire à 2 personnes, les deux règles peuvent être respectées en même temps en inversant l’ordre précédent. L’impossibilité survient plutôt dans des cas particuliers — par exemple, une séance précédente avec une seule personne (qui était à la fois première et dernière), ou des priorités manuelles qui entrent en conflit avec les règles. Il faut une règle de repli explicite pour ces cas-là, sinon le comportement sera arbitraire.

**Pistes à évaluer (sans en choisir une) :**

- Relâcher d’abord la règle de la dernière place, garder celle de la première.
- Relâcher d’abord la règle de la première place, garder celle de la dernière.
- Relâcher les deux et se fier seulement à la pondération.
- Tirer au hasard parmi les ordres qui violent le moins de règles.

**Ce qu’il faudra décider :** la hiérarchie de repli, et le message affiché à l’équipe quand une règle n’a pas pu être respectée.

## 6. Régénération d’un brouillon non terminé

**Question :** Est-ce que l’équipe peut régénérer un brouillon non terminé? Dans quelles circonstances?

**Pourquoi ça compte :** Si on peut régénérer sans limite jusqu’à obtenir un ordre qui « plaît », le tirage n’est plus un tirage : c’est un choix déguisé. Si on ne peut jamais régénérer, une erreur de manipulation (mauvais groupe, mauvaise présence) devient difficile à corriger.

**Pistes à évaluer (sans en choisir une) :**

- Aucune régénération : on modifie manuellement le brouillon.
- Régénération permise seulement avant la première révélation / avant toute modification manuelle.
- Régénération permise, mais chaque tentative est journalisée.
- Régénération permise seulement si les présences ou les priorités changent.

**Ce qu’il faudra décider :** la règle, et ce qui est journalisé.

## 7. Corrections aux résultats enregistrés

**Question :** Comment corriger un résultat déjà enregistré, et comment suivre ces corrections?

**Pourquoi ça compte :** Une erreur peut être découverte après l’enregistrement (mauvais nom, mauvaise date, ordre mal noté). Mais si on peut réécrire l’historique sans trace, la confiance dans l’équité s’effrite.

**Ce qu’il faudra décider :**

- Qui peut corriger un résultat enregistré?
- Jusqu’à quand (le jour même? tant que le tirage suivant n’a pas eu lieu? toujours?)?
- Est-ce qu’on garde l’ancienne version (historique de vérification) ou est-ce qu’on écrase?
- Est-ce qu’une correction recalcule l’équité des tirages suivants qui ont déjà eu lieu? (En principe, non : on ne réécrit pas le passé. Mais il faut le dire explicitement.)
- Est-ce que la correction elle-même est enregistrée comme une décision manuelle, avec la raison?

## 8. Réorganisation manuelle qui crée une répétition de première ou de dernière place

**Question :** Que fait l’application quand une réorganisation manuelle produit un ordre final où la même personne est première (ou dernière) pour une deuxième fois consécutive?

**Règle convenue :** l’ordre final réel est l’ordre qui fait foi, même si l’équipe l’a modifié. Le résultat final enregistré est ce qui compte pour l’équité future.

**Pourquoi ça compte :** le tirage généré respecte les règles de non-répétition, mais l’équipe peut ensuite déplacer les noms. Si ce déplacement crée une répétition de première ou de dernière place, l’application ne doit pas traiter silencieusement cette exception manuelle comme un résultat aléatoire conforme.

**Pistes à évaluer (sans en choisir une) :**

- Afficher un avertissement, demander une confirmation explicite, et enregistrer l’exception comme une décision manuelle — par analogie avec les dérogations pour les priorités de première place.
- Enregistrer l’exception sans avertissement, mais la signaler dans l’historique.
- Autre traitement convenu avec l’équipe.

**Ce qu’il faudra décider :** avertissement ou non, confirmation ou non, et comment l’exception est enregistrée. Aucune politique n’est choisie ici.

## 9. Simulations d’équité

**Question :** Comment va-t-on tester que la pondération fonctionne comme prévu?

**Ce qu’il faudra décider :**

- Quelles mesures on suit (par exemple : distribution des places sur 500 tirages simulés, taux de répétition première/dernière, temps moyen avant qu’une personne « due » obtienne une bonne place, écart entre la personne la plus avantagée et la plus désavantagée).
- Quels scénarios on simule (groupes de 10–15, petits groupes, absences fréquentes, priorités fréquentes, nouvelle personne qui arrive).
- Quel seuil de performance on exige avant de considérer l’algorithme acceptable.

Tant que les simulations ne sont pas faites, la pondération reste une hypothèse, pas une garantie.

## 10. Architecture de stockage partagé et hébergement

**Question :** Quelle architecture pour le stockage partagé?

**Direction privilégiée :** système partagé et synchronisé, accessible par plusieurs membres de l’équipe à partir de différents appareils. Solution de repli acceptable : un seul appareil.

**Ce qu’il faudra décider (sans s’engager pour l’instant) :**

- Base de données ou autre mécanisme de stockage (aucun choix fait).
- Fournisseur d’authentification, si authentification il y a (aucun choix fait).
- Plateforme d’hébergement (aucun choix fait).
- Comment l’équipe se connecte (compte partagé? comptes individuels? lien protégé? code?).
- Où les données sont hébergées et qui y a accès.
- Sauvegarde et récupération en cas de problème.

## 11. Accès simultané et modifications à partir de plusieurs appareils

**Question :** Que se passe-t-il si deux membres de l’équipe modifient le même tirage en même temps?

**Ce qu’il faudra décider :**

- Est-ce qu’un seul brouillon actif par groupe et par jour est permis?
- Est-ce qu’on verrouille le tirage pendant qu’une personne le modifie?
- Est-ce que la dernière modification écrase la précédente, ou est-ce qu’on signale un conflit?
- Est-ce qu’on affiche « quelqu’un d’autre est en train de modifier ce tirage »?

## 12. Vue « Équité des tirages »

**Question :** Est-ce qu’une vue détaillée de statistiques d’équité vaut la peine?

**Ce qu’il faudra décider :**

- Est-ce que l’équipe la consulterait vraiment, ou est-ce que ça ajoute de la complexité pour peu de bénéfice?
- Si oui, qu’est-ce qu’on y montre (sans jargon, sans équations) : par exemple, combien de fois chaque personne a été dans la première moitié vs la deuxième moitié, sur les dernières semaines?
- Est-ce que cette vue pourrait créer des malentendus (« pourquoi j’ai eu plus de mauvaises places? ») et comment on l’explique?

## 13. Prénoms identiques

**Question :** Comment distinguer deux personnes qui ont le même prénom dans un même groupe?

**Pourquoi ça compte :** On ne conserve que les prénoms. Deux « Alex » dans le même groupe rendraient l’ordre ambigu, autant à l’écran que dans l’historique.

**Pistes à évaluer (sans en choisir une) :**

- Ajouter une initiale ou un qualificatif visible seulement à l’écran (sans conserver de nom de famille).
- Utiliser un surnom choisi par la personne.
- Autre mécanisme d’identification convenu avec l’équipe.

**Ce qu’il faudra décider :** le mécanisme, en respectant le principe « prénoms seulement ».

## 14. Priorités récurrentes et accommodements

**Question :** Si une personne reçoit souvent des priorités pour un accommodement récurrent, est-ce que ses places prioritaires doivent compter exactement comme les autres dans l’historique d’équité?

**Règle convenue :** les places réellement obtenues comptent pour l’équité future.

**Tension à trancher :** si une personne obtient souvent la place 1 par priorité (accommodement), l’algorithme d’équité va ensuite la pousser vers des places tardives les jours sans priorité, pour « compenser ». Ça pourrait punir l’accommodement lui-même.

**Pistes à évaluer (sans en choisir une) :**

- Garder la règle telle quelle : tout compte pareil.
- Signaler les tirages avec priorité dans l’historique, et les traiter différemment dans le calcul d’équité (par exemple, les exclure du calcul, ou les pondérer moins).
- Autre traitement convenu avec Max et l’équipe.

Cette question doit être tranchée avec Max et l’équipe avant de programmer l’algorithme, parce qu’elle change le calcul.

## 15. Ordre généré vs ordre final : que garde-t-on?

**Question :** Quand l’équipe modifie manuellement un ordre, garde-t-on aussi l’ordre généré au départ?

**Règle convenue :** seul le résultat final compte pour l’équité future.

**Ce qui reste à décider :** est-ce qu’on conserve l’ordre généré au départ à des fins de transparence (pour voir que l’équipe a modifié l’ordre, et comment), ou est-ce qu’on ne conserve que le résultat final? Conserver les deux aide la vérification, mais ajoute une donnée à expliquer.

## 16. Personne renommée ou retirée : que devient son historique?

**Question :** Si on renomme une personne dans un groupe, ou si on la retire, que devient son historique?

**Ce qu’il faudra décider :**

- Est-ce que l’historique suit le nouveau nom?
- Est-ce qu’on garde l’historique d’une personne retirée pour les tirages déjà enregistrés (oui, en principe), mais est-ce qu’on la retire des calculs futurs?
- Est-ce qu’une personne qui revient après un retrait repart avec son ancien historique ou avec un historique vide?

## 17. « Comment ça fonctionne? » : niveau de détail

**Question :** Jusqu’où va l’explication de l’équité dans l’outil lui-même?

La page « Comment ça fonctionne? » doit expliquer le principe sans jargon ni équations. Il faudra décider si on y montre des exemples concrets, et si on y mentionne les règles de non-répétition et la compensation douce, ou si on reste à un niveau très général (« le tirage tient compte des tirages passés »).
