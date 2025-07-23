# hexentropy_v0

Ce programme expérimente une génération récursive et multithreadée d'une chaîne hexadécimale de longueur `n`. On vise surtout la vitesse brute sur des machines très dotées en cœurs CPU.

## 7 points de réflexion (et tâches associées)
1. **Contrôle de la profondeur** –
   Limiter `MAX_DEPTH` évite une explosion de threads.
   *Tâche : ajuster cette constante selon le matériel.*
2. **Granularité minimum** –
   Passer en mode séquentiel pour les petits blocs (`SMALL_CHUNK`).
   *Tâche : mesurer l'impact sur la performance et ajuster.*
3. **Motif au cas impair** –
   `rand_hexbit` choisit `0x07` ou `0x08` lorsque la longueur est impaire,
   insère cette valeur au centre puis divise les deux moitiés récursivement.
   *Tâche : analyser la répartition obtenue en profondeur.*
4. **Risque de contention mémoire** –
   Plusieurs threads écrivent dans un même buffer.
   *Tâche : profiler l'impact sur de grandes tailles.*
5. **Compatibilité système** –
   `getrandom` n'existe pas partout.
   *Tâche : prévoir une alternative (ex. `/dev/urandom`).*
6. **Rapport avec Miller-Rabin** –
   On vise une génération plus rapide que la vérification de primalité.
   *Tâche : mesurer le temps par rapport à une implémentation de Miller-Rabin.*
7. **C vs C++** –
   Le C est minimaliste, C++ offre plus d'abstractions (threads plus simples, RAII).
   *Tâche : tester une version C++ pour comparer la latence et le confort de code.*

## Fonctions principales
- `rand_hexbit` : renvoie `0x07` ou `0x08` avec la même probabilité.
- `fill_random` : remplit séquentiellement un morceau du buffer.
- `hexentropy_worker` : pour une longueur paire il se scinde simplement en deux,
  pour une longueur impaire il insère `rand_hexbit` au centre puis poursuit la récursion sur chaque moitié.
- `main` : parse la taille, alloue le buffer et lance la génération.

## Explications par blocs
1. **Inclusions** – on embarque `stdio.h`, `stdlib.h`, `pthread.h`,
   `sys/random.h` et `string.h` pour avoir les appels système et les threads.
2. **Structure WorkerCtx** – trois champs pour passer le buffer, la taille
   courante et la profondeur aux threads.
3. **Constantes** – `MAX_DEPTH` limite la récursivité, `SMALL_CHUNK` évite de
   créer trop de threads pour des broutilles.
4. **rand_hexbit** – lit un octet via `getrandom` et renvoie `0x07` ou `0x08`.
5. **fill_random** – lecture séquentielle de `len` octets aléatoires.
6. `hexentropy_worker` : pour une longueur paire il se scinde simplement en deux,
  pour une longueur impaire il insère `rand_hexbit` au centre puis poursuit la récursion sur chaque moitié.
7. **main** – allocation du buffer, déclenchement du premier appel et affichage
   final sous forme hexadécimale.

## Compilation
```bash
gcc -std=c11 -pthread hexentropy_v0.c -o hexentropy_v0
```

## Un mot sur C vs C++
Le C permet un contrôle très direct (pas de surprise côté allocation), ce qui peut être un avantage en latence pure. C++ apporte toutefois des abstractions utiles (std::thread, containers, RAII) qui simplifient l'écriture et peuvent éviter des fuites ou des erreurs. La surcharge en performance est généralement négligeable pour ce type de tâches, surtout avec un code bien optimisé.

---
Bon courage, tu vas en avoir besoin.
