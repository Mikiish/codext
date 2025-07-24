import sympy
import random
import time
import os

# Constantes globales
no_mutation_streak = 0  # Compteur de nombres sans mutation trouvée
longest_streak = 0  # Plus grande séquence sans mutation première
total_iterations = 0  # Compteur total des nombres testés


# Fonction pour générer un nombre premier aléatoire en binaire
def generate_random_prime(bits=2084):
    while True:
        candidate = int.from_bytes(os.urandom(bits // 8), "big")  # Vrai aléatoire
        candidate |= (1 << (bits - 1))  # 🔥 Force le bit de poids fort à 1
        if sympy.isprime(candidate):
            return candidate


def HasPrimeMutation(hex_prime):
    """Teste toutes les mutations d'un nombre hexadécimal et retourne une liste de mutations premières."""
    global no_mutation_streak, longest_streak
    hex_digits = "0123456789ABCDEF"
    casino_prime = hex(hex_prime)[2:].upper()
    found_mutation = False  # ✅ Variable pour suivre si on a trouvé au moins UNE mutation première

    for index in range(len(casino_prime)):
        original_digit = casino_prime[-(index + 1)]
        for new_digit in hex_digits.replace(original_digit, ""):
            mutated = list(casino_prime)
            mutated[-(index + 1)] = new_digit
            mutated_hex = "".join(mutated)
            mutated_int = int(mutated_hex, 16)

            # Vérification de primalité
            if sympy.isprime(mutated_int):
                no_mutation_streak = 0
                return True  # ⛔ Arrêt immédiat pour ce nombre (pas besoin de continuer)

            no_mutation_streak += 1
            # 🔥 On incrémente SEULEMENT si AUCUNE mutation n'a été trouvée
            if no_mutation_streak > longest_streak:
                longest_streak = no_mutation_streak

    return False


if __name__ == "__main__":
    # 🔄 Boucle principale
    start_time = time.time()
    while True:
        total_iterations += 1
        prime_candidate = generate_random_prime()
        if (total_iterations % 10) == 0:
            print(f"🟢 {int(total_iterations)} nombres testés - Longest streak: {longest_streak}")

        result = HasPrimeMutation(prime_candidate)
        if not result:
            end_time = time.time()
            print(f"🔥 Nombre trouvé après {total_iterations} tentatives en {end_time - start_time}.\n Monstre : {hex(prime_candidate)}")
            break

