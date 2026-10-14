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

**Récence (décision confirmée) :** les sélections comptabilisées plus récentes ont une influence légèrement plus grande que les plus anciennes dans l’historique glissant de six sélections. Décroissance douce : les six contribuent. La récence reflète l’ordre des six dernières sélections comptabilisées, pas les semaines civiles écoulées pendant les pauses.

**Courts historiques (décision confirmée) :** une nouvelle personne commence neutre, puis l’influence de son propre historique comptabilisé augmente graduellement à mesure qu’il s’accumule. Une seule première ou dernière place ne produit pas un ajustement à pleine force. Les règles strictes de non-répétition s’appliquent quand même dès la première sélection comptabilisée, quand c’est possible, sous réserve du repli convenu. Le lissage ne vise que l’équilibrage probabiliste doux. Une personne qui revient n’est pas réinitialisée comme « nouvelle » (voir question 16).

**Ce qu’il reste à décider :**

- Poids relatifs / courbe exacts de la récence (à calibrer / valider par simulations).
- Fonction / échelle exactes de lissage des courts historiques (simulations).
- Seuils d’acceptation des simulations pour la récence + le lissage ensemble (tirage malchanceux unique, tirage chanceux unique, absences).

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

**Hiérarchie de repli (décision confirmée 2026-10-14, Avery) :** quand il est mathématiquement impossible de respecter les deux règles de non-répétition à la fois, protéger en priorité le fait de ne pas placer quelqu’un en **DERNIÈRE** place deux fois de suite. D’abord essayer de respecter les deux règles; seulement quand les deux sont conjointement impossibles, protéger la non-répétition de la dernière place si un ordre valide la respectant existe, même si cela veut dire permettre une répétition de la première place. Si même la non-répétition de la dernière place ne peut pas être respectée, produire un ordre valide au moyen d’un repli secondaire clairement documenté (encore à concevoir / tester), avec un avis clair. Voir `regles-selecteur.md` §5.4.

**Ce qu’il reste à décider :** la méthode technique exacte d’échantillonnage contraint / repli, le départage entre ordres également admissibles, et le message affiché à l’équipe quand une règle n’a pas pu être respectée.

## 6. Régénération d’un brouillon non terminé

**RÉSOLU 2026-10-14 (décision d’Avery) — voir `regles-selecteur.md` §4.4.**

**Décision :** on peut recommencer un tirage provisoire, avec une **confirmation obligatoire « Êtes-vous sûr(e)? »**. Avant la révélation, l’équipe peut recommencer après confirmation; après le début de la sélection, on utilise des corrections manuelles explicites plutôt que de remplacer secrètement des noms déjà révélés. Les propositions écartées **n’entrent jamais** dans l’historique d’équité. Le parcours distingue « nouveau brouillon », « tirage écarté » et « résultat final enregistré ». Conserver ou non une trace d’audit minimale des tentatives annulées est un détail d’implémentation.

## 7. Corrections aux résultats enregistrés

**RÉSOLU 2026-10-14 (décisions d’Avery) — voir `regles-selecteur.md` §7.4.**

**Décisions :** les résultats enregistrés **peuvent être corrigés**. **Qui :** tout membre autorisé de l’équipe qui est autorisé à faire fonctionner le sélecteur; aucune permission réservée à Maxime ni justificatif administrateur distinct (sous réserve de l’approbation de Maxime pour l’accès au sélecteur en général). **Raison écrite : facultative** — on doit pouvoir corriger sans taper d’explication; une brève note est possible, jamais une condition préalable. **Aucune limite de temps :** corrections à tout moment, **aucune limite arbitraire fondée sur l’âge**. **Vérification obligatoire et automatique :** conserver **toutes** les versions enregistrées antérieures, la date / heure de chaque correction et ce qui a changé; identifier l’auteur seulement si le modèle d’accès le permet vraiment (avec des justificatifs partagés, enregistrer au moins l’événement, l’horodatage et les détails avant / après). L’**ordre corrigé** sert aux calculs futurs. On ne fait **pas** de nouveau tirage rétroactif des séances passées. Le tirage généré d’origine est conservé séparément (voir question 15).

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

## 11. Accès simultané et modifications à partir de plusieurs appareils (partiellement résolue)

**Politique confirmée 2026-10-14 (Avery) — voir `regles-selecteur.md` §10 : un seul éditeur, plusieurs spectateurs + reprise sécuritaire.** **Seul UN membre / appareil** peut modifier activement une sélection donnée (jour de semaine / date) à la fois. Les autres appareils autorisés peuvent **consulter** son état et ses résultats, mais ne doivent pas modifier, écraser, régénérer, corriger ni finaliser cette même sélection en cours pendant qu’un autre appareil en détient le contrôle. Indiquer clairement aux spectateurs que la modification est déjà en cours, en français québécois simple (« Tirage en cours sur un autre appareil » si l’identité n’est pas disponible). Empêcher les écrasements silencieux du type « dernière écriture gagne » et les doubles enregistrements finaux. **Reprise sécuritaire obligatoire :** si le navigateur qui modifie se ferme, perd la connexion ou est abandonné, un autre membre autorisé doit pouvoir reprendre le contrôle en sécurité (par exemple, bail à expiration géré par le serveur + reprise contrôlée, vérifications de version). Valider à nouveau l’autorité au moment d’enregistrer un résultat final; empêcher un éditeur d’origine périmé d’écraser le travail après une reprise. Aucune cérémonie quotidienne obligatoire de verrouillage / déverrouillage en plusieurs étapes. S’il existe un dossier final terminé pour le jour, ouvrir un autre appareil doit afficher ce dossier, pas lancer silencieusement un deuxième résultat officiel en conflit. Les corrections de l’historique enregistré ont aussi besoin d’une protection contre les conflits / versions.

**Ce qu’il reste à décider :** la conception technique exacte du verrouillage / de la reprise et le délai d’expiration (choix d’ingénierie à tester; aucune valeur de temporisation approuvée).

## 12. Vue « Équité des tirages »

**RÉSOLU 2026-10-14 (décision d’Avery) — voir `regles-selecteur.md` §8.3.**

**Décision :** inclure une page **facultative, distincte et facile à comprendre** de statistiques / aperçu de l’historique d’équité, loin du sélecteur quotidien sans encombrement. Facultative *à consulter* ne veut pas dire facultative *à mettre en place*. Elle aide l’équipe à comprendre comment les occasions ont été réparties, par exemple des comptes de places en première moitié vs en deuxième moitié, à partir des résultats réellement enregistrés. Elle ne doit **pas** ressembler à une évaluation du rendement ni classer les personnes par mérite; éviter le jargon et les affirmations trompeuses de garanties mathématiques. Distinguer correctement les absences, les pauses d’anniversaire, les séances uniques exclues et les priorités / modifications manuelles enregistrées. Les mesures individuelles et les détails de visualisation seront choisis pendant la conception de l’interface.

## 13. Prénoms identiques

**RÉSOLU 2026-10-14 (décision d’Avery) — voir `regles-selecteur.md` §2.3.**

**Décision :** utiliser le **nom usuel préféré** de chaque personne, tel qu’inscrit sur la liste. Si quelqu’un utilise déjà un surnom au quotidien, ce surnom est son nom d’affichage dès le départ. **Ne pas inventer, exiger ni attribuer de surnoms** pour distinguer des personnes qui préfèrent leur prénom. **Seulement** quand deux personnes du même groupe du jour auraient autrement des noms d’affichage identiques, les distinguer par une **initiale** appropriée, par exemple « Alex M. » et « Alex T. », inscrite / confirmée par l’équipe (jamais devinée automatiquement). Étiquettes claires et respectueuses, jamais « Alex 1 » / « Alex 2 ». Le nom d’affichage ou l’initiale n’est jamais la clé d’identité de la base de données : identifiant interne stable, étiquettes validées uniques dans chaque groupe actif. Si les initiales entrent aussi en collision, signaler l’ambiguïté pour une distinction respectueuse fournie explicitement par l’équipe. Aucun nom de famille ni autre détail personnel au-delà des initiales de distinction.

## 14. Priorités récurrentes et accommodements

**RÉSOLU 2026-10-14 (décision d’Avery) — voir `regles-selecteur.md` §6.1 : « tout compte pareil ».**

**Décision :** toute place prioritaire compte pleinement dans l’historique d’équité, avec sa provenance manuelle enregistrée. La suggestion de créer une exemption d’équité spéciale pour les priorités d’accommodement a été explicitement rejetée : les accommodements se vivent **dans les tâches, pas dans le processus de sélection de l’ordre**; le sélecteur est censé être réellement égal. **Ne pas mettre en place** de catégories d’accommodement, de champs de raison médicale, ni d’exclusions spéciales de priorité.

## 15. Ordre généré vs ordre final : que garde-t-on?

**RÉSOLU 2026-10-14 (décision d’Avery) — voir `regles-selecteur.md` §7.3.**

**Décision :** pour une sélection terminée, conserver **à la fois l’ordre généré d’origine** et **l’ordre final confirmé par l’équipe**, consultables ensemble dans le détail d’un résultat passé, avec une indication compréhensible de ce qui a changé. **Seul l’ordre final explicitement enregistré sert** à la pondération d’équité et à l’historique première / dernière; le brouillon d’origine sert à la transparence et à la vérification seulement. Les brouillons écartés et les tirages annulés n’entrent jamais dans l’historique d’équité. Si l’ordre final est identique à l’ordre généré, l’interface n’a pas besoin d’afficher un « changement » déroutant. En cas de correction d’un résultat enregistré, conserver les versions antérieures; seul l’ordre final corrigé courant fournit les positions faisant foi; ne pas écraser l’ordre généré d’origine. Les exemptions d’anniversaire, les priorités et les coups de pouce conservent leur provenance / leurs marqueurs. La comparaison appartient à la vue facultative historique / détail, pas à l’écran principal. Le format exact de conservation et le fournisseur de stockage ne sont pas réglés.

## 16. Personne renommée ou retirée : que devient son historique?

**RÉSOLU 2026-10-14 (décision d’Avery) — voir `regles-selecteur.md` §2.3.**

**Décision :** si une personne quitte un groupe du jour puis réintègre **le même groupe**, on **conserve son historique d’équité existant** (y compris les six dernières sélections comptabilisées et la dernière position extrême comptabilisée). Retirer quelqu’un de la liste active la rend inactive pour les tirages futurs; cela ne supprime ni ses dossiers enregistrés ni son identité sous-jacente. Une absence de plusieurs mois ne fait avancer ni ne réinitialise les séquences. L’historique des autres groupes reste indépendant. Une vraie nouvelle personne commence neutre; on ne traite pas silencieusement une personne qui revient comme une nouvelle personne. Corriger un nom ou utiliser un nom d’affichage préféré ne doit pas créer une nouvelle identité ni orpheliner l’historique : identifiant interne stable, parcours de réactivation qui évite les dossiers en double. On ne ressuscite pas d’absences ni de sélections inventées pour la période hors liste. La convention d’affichage des prénoms identiques est réglée séparément (voir question 13).

## 17. « Comment ça fonctionne? » : niveau de détail

**Question :** Jusqu’où va l’explication de l’équité dans l’outil lui-même?

La page « Comment ça fonctionne? » doit expliquer le principe sans jargon ni équations. Il faudra décider si on y montre des exemples concrets, et si on y mentionne les règles de non-répétition et la compensation douce, ou si on reste à un niveau très général (« le tirage tient compte des tirages passés »).

## 18. Coups de pouce manuels : mécanique exacte (partiellement résolue)

**Décisions confirmées 2026-10-14 (Avery) — voir `regles-selecteur.md` §5.5 :** l’équipe peut donner un coup de pouce manuel quand c’est nécessaire, par une option avancée « Donner un coup de pouce » (libellé de travail), hors de l’écran quotidien ordinaire. **Positif seulement :** les ajustements peuvent seulement augmenter les chances; aucun contrôle pour diminuer explicitement la pondération / les chances d’une personne. Nuance : augmenter le poids relatif d’une personne diminue par définition légèrement les probabilités relatives des autres — acceptable, mais ne pas présenter la fonction comme laissant toutes les autres exactement inchangées. **Un seul niveau fixe, doux et positif :** pas de niveaux sélectionnables, pas de curseur. **Plusieurs coups de pouce égaux :** plus d’une personne peut recevoir le même coup de pouce calibré; pas de forces différentes par personne, pas d’empilement, pas de réduction. Si toutes les personnes admissibles reçoivent le même facteur, leurs probabilités relatives restent inchangées (neutre / redondant). **Qui :** tout membre autorisé de l’équipe qui est autorisé à faire fonctionner le sélecteur; aucun mot de passe supplémentaire, code administrateur distinct, ni permission réservée à Maxime (sous réserve de l’approbation de Maxime pour l’accès au sélecteur en général). Enregistrer l’action; avec une connexion partagée, ne pas promettre d’attribution individuelle — enregistrer au minimum les coups de pouce appliqués, à qui, pour quel tirage (plus horodatages quand c’est faisable). **Aucune confirmation pour appliquer :** l’interface indique clairement chaque personne dont le coup de pouce est actif; on peut retirer / annuler avant de générer le tirage, sans confirmation supplémentaire. Cela n’affaiblit pas la confirmation pour recommencer un brouillon ni l’avertissement + confirmation pour déroger à une règle de première / dernière. **Durée :** strictement la sélection du jour courant, **sans option permanente ni report** (remplace « aujourd’hui seulement, par défaut »). Un coup de pouce est une entrée pour une seule sélection, jamais un ajustement à long terme de la pondération de base. Les coups de pouce restent soumis à l’admissibilité, aux réservations d’anniversaire, aux priorités et aux contraintes strictes / repli convenu. Le dossier montre les coups de pouce réellement actifs pour le brouillon généré utilisé dans le résultat final; les coups de pouce annulés avant le tirage ne comptent pas comme actifs; un tirage écarté n’entre jamais dans l’historique.

**Ce qu’il reste à décider :**

- Valeur numérique exacte du coup de pouce (à calibrer / valider par simulations : utile mais modeste, hasard préservé, non-répétition respectée).
- Garde-fous pendant le tirage et détails de la représentation de vérification.
- Que faire quand une personne ayant reçu un coup de pouce devient absente.
- Effet sur les simulations (les scénarios de test doivent couvrir les coups de pouce).

**Aucun biais permanent caché** du système d’équité.

## 19. Mode anniversaire : interactions

**RÉSOLU 2026-10-14 (décisions d’Avery) — voir `regles-selecteur.md` §6.3.**

**Décisions de base (rappel) :** le mode anniversaire est une exception célébratoire explicitement activée. La personne fêtée obtient la première place, sa sélection est une pause pour sa propre histoire d’équité (fenêtre de six sélections comptabilisées + séquence des extrêmes), sa position réelle reste dans l’ordre final enregistré, marquée comme exception d’anniversaire. Les autres personnes comptent normalement. Deux anniversaires le même jour : les deux premières places, ordre aléatoire entre les deux, les deux en pause. Activation manuelle le jour même, sans base de données de dates de naissance (recommandation UX, pas une exigence confirmée).

**Anniversaire avant les priorités ordinaires (décision confirmée) :** les personnes fêtées occupent toujours les premières places, AVANT les priorités manuelles ordinaires. Un anniversaire : place 1, priorités à partir de la place 2. Deux anniversaires : places 1–2, priorités à partir de la place 3. Les anniversaires **s’ajoutent** à la limite d’au plus trois priorités ordinaires, ils n’y sont pas inclus (deux anniversaires + trois priorités : places 1–2 anniversaire, places 3–5 priorités, reste en tirage aléatoire pondéré). Ne pas laisser tomber ni rétrograder une priorité approuvée; une priorité ne déplace pas une personne fêtée. La sélection simultanée anniversaire / priorité de la même personne et les cas avec plus de places spéciales que de personnes présentes sont des détails explicites de validation de l’interface.

**Réorganisation manuelle (décision confirmée) :** une personne fêtée déplacée manuellement hors des places réservées aux anniversaires **perd son exemption**; sa position finale réelle enregistrée compte normalement. Échanger simplement les deux personnes fêtées entre les places 1 et 2 conserve les deux exemptions. Déplacer l’une des deux hors des deux premières places : seule la personne concernée perd son exemption. Pour un anniversaire, seule la place 1 compte. Évaluer sur l’ordre final enregistré (ou corrigé), pas sur un brouillon ni l’ordre généré initial. Garder une trace de vérification.

**Personne fêtée absente (décision confirmée) :** le mode anniversaire s’applique seulement si la personne fêtée est **présente à la sélection**. Sinon, enregistrer « Absent(e) au tirage », aucune place réservée, pause normale due à l’absence, aucune priorité transférée, **aucun rattrapage automatique** à la sélection suivante. Règle d’arrivée tardive si la personne arrive après la sélection. Deux personnes fêtées prévues, une absente : seule la participante reçoit la place d’anniversaire. Aucun indicateur d’anniversaire périmé dans un brouillon ou un résultat final pour la personne absente.
