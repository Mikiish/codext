# 🔐 cryptodexheuu.md

Ce document décrit brièvement le fonctionnement du petit module LISP d’authentification basé sur `scthsh.lisp`.

Son objectif est de fournir une preuve d’authenticité cryptographique en utilisant un token système combiné à une entrée externe.

## Visit the following repos :
- [https://github.com/Mikiish/Clisa]
- [https://github.com/Mikiish/Lisa]
- [https://github.com/Mikiish/ai_sprint_paris_mfork]

---

## 🧩 Fonctionnement

- Le script lit une variable d’environnement (`API_TOKEN`) considérée comme un **secret local**.
- Il applique un premier hash SHA-256 sur ce token → `token-hash`.
- Ensuite, il concatène ce `token-hash` avec une **entrée utilisateur (clé publique, chaîne, identifiant, etc.)**.
- Enfin, il calcule **le hash SHA-256 de cette concaténation** → `final-hash`.

```lisp
final-hash = SHA256(SHA256($API_TOKEN) || user-input)
```

---

## 🎯 À quoi ça sert ?

Ce système fournit un mécanisme simple et fiable pour :

- Authentifier une **clé publique ou identifiant externe**
- Générer des **empreintes non falsifiables** basées sur un secret connu uniquement en local
- Créer des **jetons signés sans révéler la clé d’origine**

---

## ⚠️ Remarque importante

Ce fichier est un **résumé pédagogique**. 
Le fichier `cryptodex.md` original, qui contient la vision complète du projet, est volontairement ignoré (`.gitignore`).

Vous pouvez l’imaginer comme un manifeste silencieux, une déclaration logicielle à découvrir ailleurs.

---

## 📎 Fichier associé : `scthsh.lisp`

Voir ce fichier pour l’implémentation exacte.
Compatible SBCL + Quicklisp + Ironclad.

---

Rien à voir ici. Circulez.
