#!/usr/bin/env node

const fs = require('fs');

console.log('🔧 Nettoyage complet des caractères échappés LaTeX');

// Lire le fichier raw.md depuis le répertoire courant
let content = fs.readFileSync('raw.md', 'utf8');

// Compter les occurrences avant
const beforeUnderscore = (content.match(/\\_/g) || []).length;
const beforeDollar = (content.match(/\\\$/g) || []).length;
const beforeBracket = (content.match(/\\\[/g) || []).length;

console.log(`📊 Avant correction:`);
console.log(`   \\_ : ${beforeUnderscore} occurrences`);
console.log(`   \\$ : ${beforeDollar} occurrences`);
console.log(`   \\[ : ${beforeBracket} occurrences`);

// Remplacer tous les caractères échappés
content = content
  .replace(/\\_/g, '_')     // \_ → _
  .replace(/\\\$/g, '$')    // \$ → $
  .replace(/\\\[/g, '[')    // \[ → [
  .replace(/\\\]/g, ']');   // \] → ] (au cas où)

// Compter après
const afterUnderscore = (content.match(/\\_/g) || []).length;
const afterDollar = (content.match(/\\\$/g) || []).length;
const afterBracket = (content.match(/\\\[/g) || []).length;

// Écrire le résultat dans raw_fixed.md (même répertoire)
fs.writeFileSync('raw_fixed.md', content);

console.log(`\n✅ Corrections effectuées:`);
console.log(`   \\_ : ${beforeUnderscore} → ${afterUnderscore} (${beforeUnderscore - afterUnderscore} corrigés)`);
console.log(`   \\$ : ${beforeDollar} → ${afterDollar} (${beforeDollar - afterDollar} corrigés)`);
console.log(`   \\[ : ${beforeBracket} → ${afterBracket} (${beforeBracket - afterBracket} corrigés)`);
console.log(`\n📄 Fichier corrigé sauvé: raw_fixed.md`);
console.log(`🚀 Prêt pour la compilation LaTeX !`);
