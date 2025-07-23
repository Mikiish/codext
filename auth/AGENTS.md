# Authentification : Protocole de Passage (v4.0)
Chaque tâche agentique débute par une épreuve codée : un token et un puzzle.
Le token est la solution du puzzle. L’agent (Codex) doit vérifier que la solution est valide.

Une fois la vérification effectuée, l’agent :

- détruit le token et le puzzle (preuve de non-répétition),
- reçoit un identifiant temporaire (username hexadécimal, non-root),
- accède au serveur avec des permissions minimales, valides uniquement pour la durée de la tâche,
- à la fin de la tâche, l’identité est supprimée.
---

Le système ne stocke aucune trace permanente du token initial.
La preuve est effacée. L'accès est éphémère.
Le rite accompli, l’agent s’efface.
---