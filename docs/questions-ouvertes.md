# Questions ouvertes

> **Lisez-moi d’abord.**
>
> Ce fichier liste les décisions qui **ne sont pas encore prises**. Rien ici ne doit être lu comme déjà décidé, ni programmé comme si c’était réglé.
>
> Quand une question est tranchée, on la déplace dans `regles-selecteur.md` avec la décision et sa date, et on la marque ici **RÉSOLU** avec un renvoi. La numérotation est conservée (les autres documents y font référence), même pour les questions résolues.

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

## 3. Fenêtre d’historique (partiellement résolue)

**Décision confirmée 2026-10-14 (Avery) :** fenêtre = **six dernières sélections comptabilisées dans l’historique d’équité de cette personne**, par groupe du jour. Six sélections comptabilisées, pas nécessairement six semaines civiles : seules les sélections ordinaires participées comptent; une absence, une sélection d’anniversaire (pour la personne fêtée) et une séance à une seule personne ne font pas avancer la fenêtre. Les personnes nouvelles commencent avec un poids neutre. Voir `regles-selecteur.md` §5.2.

**Ce qu’il reste à décider :**

- Est-ce que les tirages récents comptent plus que les plus anciens, ou est-ce que chaque tirage de la fenêtre compte également?
- Traitement des très courts historiques (à partir de combien de tirages l’historique compte-t-il « pleinement »? faut-il lisser les premiers tirages?).

## 4. « Consécutive » : que veut dire deux sélections de suite?

**RÉSOLU 2026-10-14 (décision d’Avery) — voir `regles-selecteur.md` §5.1 et §3.3.**

**Décision :** on compare les **deux dernières sélections comptabilisées** de la personne, dans le groupe du jour. Une absence ne réinitialise ni ne fait avancer la séquence de la personne et ne fournit aucune position. Les absences sont une pause.

**Exemple :** Léa est première le mardi 6 octobre. Elle est absente le mardi 13 octobre. Le 6 et le 20 octobre sont consécutifs **pour Léa** (elle n’a participé à aucun tirage entre les deux) : elle **ne peut pas** être première le 20 octobre en vertu de la règle ordinaire (sauf exception d’anniversaire, voir §6.3 des règles, ou dérogation manuelle confirmée).

## 5. Ordre de priorité quand les règles entrent en conflit (partiellement résolue)

**Décision confirmée 2026-10-14 (Avery) :** une séance à une seule personne peut être enregistrée comme événement, mais sa première/dernière place inévitable est **exclue de la pondération d’équité et de la contrainte des extrêmes consécutifs**. Voir `regles-selecteur.md` §5.4.

**Question restante :** Quand il est impossible de respecter toutes les règles d’équité en même temps, laquelle on relâche en premier?

**Pourquoi ça compte :** Dans le cas ordinaire à 2 personnes, les deux règles peuvent être respectées en même temps en inversant l’ordre précédent. L’impossibilité survient plutôt dans des cas particuliers — par exemple, des priorités manuelles qui entrent en conflit avec les règles de non-répétition, ou un cas lié aux absences : si les deux personnes admissibles aujourd’hui ont toutes les deux été premières à leur dernier tirage comptabilisé respectif, aucune des deux n’est admissible à la première place sous la contrainte stricte. Il faut une règle de repli explicite pour ces cas-là, sinon le comportement sera arbitraire.

**Pistes à évaluer (sans en choisir une) :**

- Relâcher d’abord la règle de la dernière place, garder celle de la première.
- Relâcher d’abord la règle de la première place, garder celle de la dernière.
- Relâcher les deux et se fier seulement à la pondération.
- Tirer au hasard parmi les ordres qui violent le moins de règles.

**Ce qu’il faudra décider :** la hiérarchie de repli, et le message affiché à l’équipe quand une règle n’a pas pu être respectée.

## 6. Régénération d’un brouillon non terminé

**RÉSOLU 2026-10-14 (décision d’Avery) — voir `regles-selecteur.md` §4.4.**

**Décision :** on peut recommencer un tirage provisoire, avec une **confirmation obligatoire « Êtes-vous sûr(e)? »**. Avant la révélation, l’équipe peut recommencer après confirmation; après le début de la sélection, on utilise des corrections manuelles explicites plutôt que de remplacer secrètement des noms déjà révélés. Les propositions écartées **n’entrent jamais** dans l’historique d’équité. Le parcours distingue « nouveau brouillon », « tirage écarté » et « résultat final enregistré ». Conserver ou non une trace d’audit minimale des tentatives annulées est un détail d’implémentation.

## 7. Corrections aux résultats enregistrés (partiellement résolue)

**Décisions confirmées 2026-10-14 (Avery) — voir `regles-selecteur.md` §7.4 :** les résultats enregistrés **peuvent être corrigés**. On **conserve la version antérieure** et on **enregistre la correction** (au moins que le changement a eu lieu, quand, et ce qui a changé; l’auteur, si le modèle d’accès le permet). L’**ordre corrigé** sert aux calculs futurs. On ne fait **pas** de nouveau tirage rétroactif des séances passées.

**Ce qu’il reste à décider :**

- Qui peut corriger un résultat enregistré?
- Jusqu’à quand (le jour même? tant que le tirage suivant n’a pas eu lieu? toujours?)?
- Est-ce que la correction elle-même est enregistrée avec une raison?

## 8. Réorganisation manuelle qui crée une répétition de première ou de dernière place

**RÉSOLU 2026-10-14 (décision d’Avery) — voir `regles-selecteur.md` §7.2.**

**Décision :** si une réorganisation manuelle crée une répétition de première ou de dernière place, l’application **avertit et exige une confirmation intentionnelle**, puis conserve le résultat comme **exception manuelle**, tandis que le résultat réel compte quand même. L’ordre final réel fait autorité. L’application ne doit pas traiter silencieusement une exception manuelle comme un résultat aléatoire conforme.

## 9. Simulations d’équité

**Question :** Comment va-t-on tester que la pondération fonctionne comme prévu?

**Ce qu’il faudra décider :**

- Quelles mesures on suit (par exemple : distribution des places sur 500 tirages simulés, taux de répétition première/dernière, temps moyen avant qu’une personne « due » obtienne une bonne place, écart entre la personne la plus avantagée et la plus désavantagée).
- Quels scénarios on simule (groupes de 10–15, petits groupes, absences fréquentes, priorités fréquentes, nouvelle personne qui arrive).
- Quel seuil de performance on exige avant de considérer l’algorithme acceptable.
- **Nouveaux scénarios à simuler (décisions 2026-10-14) :** exceptions d’anniversaire — (a) la personne fêtée est placée première; (b) sa place d’anniversaire ne modifie pas son poids futur ni sa séquence des extrêmes; (c) les positions réelles des autres continuent de compter; (d) un re-tirage / une annulation ne crée pas d’historique fantôme. Brouillons non enregistrés : jamais comptés. Ajustements manuels des chances : effet le jour même seulement, par défaut, réinitialisation le lendemain, ajustement identifiable comme manuel, pas de persistance silencieuse. Corrections de résultats enregistrés : version antérieure conservée, ordre corrigé utilisé pour la suite, aucune réécriture rétroactive des séances passées.

Tant que les simulations ne sont pas faites, la pondération reste une hypothèse, pas une garantie.

## 10. Architecture de stockage partagé et hébergement (partiellement résolue)

**Direction convenue 2026-10-14 (Avery) :** architecture partagée et synchronisée, **option A** (site statique + base de données hébergée, éventuellement avec fonctions serveur gérées), **sous réserve** d’une évaluation réaliste de l’hébergement, de la confidentialité, de l’accès, des sauvegardes / exportations et de la protection contre les écrasements concurrents. **Préférence initiale :** accès d’équipe protégé simple plutôt que beaucoup de comptes individuels — **sous réserve de l’approbation opérationnelle / confidentialité de Max**. Friction de connexion quotidienne minimale (idéalement, session protégée persistante sur les appareils de confiance de l’équipe). Voir `regles-selecteur.md` §10.

**Ce qu’il reste à décider (aucun choix fait — ne pas présenter comme décidés) :**

- Base de données ou autre mécanisme de stockage.
- Fournisseur d’authentification / schéma d’authentification.
- Plateforme d’hébergement et région d’hébergement.
- Modèle d’accès définitif et approbation de Max.
- Où les données sont hébergées et qui y a accès.
- Sauvegarde et récupération en cas de problème.

## 11. Accès simultané et modifications à partir de plusieurs appareils

**Question :** Que se passe-t-il si deux membres de l’équipe modifient le même tirage en même temps?

**À évaluer dans le cadre de la direction convenue (option A) :** la protection contre les écrasements concurrents fait partie des conditions d’évaluation avant de s’engager.

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

**RÉSOLU 2026-10-14 (décision d’Avery) — voir `regles-selecteur.md` §6.1 : « tout compte pareil ».**

**Décision :** toute place prioritaire compte pleinement dans l’historique d’équité, avec sa provenance manuelle enregistrée. La suggestion de créer une exemption d’équité spéciale pour les priorités d’accommodement a été explicitement rejetée : les accommodements se vivent **dans les tâches, pas dans le processus de sélection de l’ordre**; le sélecteur est censé être réellement égal. **Ne pas mettre en place** de catégories d’accommodement, de champs de raison médicale, ni d’exclusions spéciales de priorité.

## 15. Ordre généré vs ordre final : que garde-t-on?

**Question :** Quand l’équipe modifie manuellement un ordre, garde-t-on aussi l’ordre généré au départ?

**Règle convenue :** seul le résultat final compte pour l’équité future. Les brouillons écartés et les tirages annulés n’entrent jamais dans l’historique d’équité (décision 2026-10-14).

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

## 18. Ajustements manuels des chances : mécanique exacte

**Décision confirmée 2026-10-14 (Avery) :** l’équipe peut ajuster manuellement les chances quand c’est nécessaire, par une option avancée « Ajuster les chances », hors de l’écran quotidien ordinaire. **Par défaut, aujourd’hui seulement** : l’ajustement affecte la sélection du jour courant et se réinitialise pour les jours suivants. Un ajustement change les chances, il n’attribue pas de place garantie — ce n’est pas une priorité. La modification du jour doit être compréhensible et identifiable comme manuelle; elle ne réécrit pas les positions historiques. Voir `regles-selecteur.md` §5.5.

**Ce qu’il reste à décider (sous-décisions ouvertes, avec garde-fous de sécurité / traçabilité) :**

- Ajustement individuel (une personne) ou de groupe, ou les deux?
- Multiplicateur / plage exacts et direction (augmenter ou diminuer les chances de qui?).
- Avertissement / confirmation avant d’appliquer.
- Affichage de vérification (comment l’équipe voit que l’ajustement est actif et ce qu’il change).
- Permission : qui peut ajuster?
- Réinitialisation : automatique le lendemain, manuelle, ou les deux?
- Effet sur les simulations (les scénarios de test doivent couvrir les ajustements).
- Existence éventuelle d’une variante explicitement persistante — jamais de persistance silencieuse. **Aucun biais permanent caché** du système d’équité.

## 19. Mode anniversaire : interactions ouvertes

**Décisions confirmées 2026-10-14 (Avery) — voir `regles-selecteur.md` §6.3 :** le mode anniversaire est une exception célébratoire explicitement activée. La personne fêtée obtient la première place, sa sélection est une pause pour sa propre histoire d’équité (fenêtre de six sélections comptabilisées + séquence des extrêmes), sa position réelle reste dans l’ordre final enregistré, marquée comme exception d’anniversaire. Les autres personnes comptent normalement. Deux anniversaires le même jour : les deux premières places, ordre aléatoire entre les deux, les deux en pause. Activation manuelle le jour même, sans base de données de dates de naissance (recommandation UX, pas une exigence confirmée).

**Interactions ouvertes — à trancher avec Avery (pas des décisions) :**

- **Anniversaire + priorités ordinaires :** conflit à exposer, sans hiérarchie choisie. La règle d’Avery dit que les anniversaires passent devant, et la règle des priorités les limite à trois places (1, 2, 3). Avec deux anniversaires et trois priorités, cinq places de tête seraient revendiquées. Aucune hiérarchie n’est choisie ici : il faut demander à Avery comment ces règles se combinent.
- **Personne marquée anniversaire absente au tirage :** *proposition :* l’exception ne s’applique pas ce jour-là (personne enregistrée comme `absente au tirage`; aucune première place d’anniversaire attribuée à quelqu’un d’autre; bascule du jour effacée).
- **Réorganisation manuelle après un tirage en mode anniversaire :** la règle doit porter sur les **positions d’anniversaire attribuées** (places 1–2 si deux anniversaires), pas seulement sur la première place. Si l’équipe déplace manuellement une personne fêtée hors de sa position d’anniversaire attribuée, il reste à trancher avec Avery si l’exception est **annulée** (sa position finale réelle compte normalement) ou **conservée**.
