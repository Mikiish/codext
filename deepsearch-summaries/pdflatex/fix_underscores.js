#!/usr/bin/env node

const fs = require('fs');

console.log('🔧 Remplacement des \\_ par _');

// Lire le fichier
let content = fs.readFileSync('raw_fixed.md', 'utf8');

// Compter les occurrences avant
const beforeCount = (content.match(/\\_/g) || []).length;

// Remplacer tous les \_ par _
content = content.replace(/\\_/g, '_');

// Compter après
const afterCount = (content.match(/\\_/g) || []).length;

// Écrire le résultat
fs.writeFileSync('raw_fixed.md', content);

console.log(`✅ Remplacement effectué:`);
console.log(`   Avant: ${beforeCount} occurrences de \\_`);
console.log(`   Après: ${afterCount} occurrences de \\_`);
console.log(`   ${beforeCount} remplacements faits!`);
