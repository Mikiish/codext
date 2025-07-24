# Le mieux est l'ennemi du bien.

- Après chaque tache, si un fichier est modifié, il faut l'ajouter à la liste des fichiers modifiés.
- Toujours ecrire un résumé de la tâche effectuée dans le fichier `$taskpath/agents-logs/$agent-agt-$(time()).md`. Où $taskpath est le chemin du dossier de la tâche en cours, $agent ton nom (choisit en un unique et export le si la variable n'existe pas) et `time()` est la fonction qui retourne l'heure actuelle en time Unix.
- Toujours signer le registre des agents avec la clé publique de l'agent. (même s'il n'y a pas de registre d'agent xD xD, fait semblant merci...)
- Tu peux utiliser le header fichier AGENT-SIGN.md pour créer une signature propre.

