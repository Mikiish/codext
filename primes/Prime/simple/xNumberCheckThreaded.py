import sympy
import random
import time
import os
import sys
import multiprocessing

# Constantes globales
no_mutation_streak = multiprocessing.Value('i', 0)  # Compteur de nombres sans mutation trouvée
longest_streak = multiprocessing.Value('i', 0)  # Plus grande séquence sans mutation première
total_iterations = multiprocessing.Value('i', 0)  # Compteur total des nombres testés
stop_flag = multiprocessing.Value('i', 0)  # 0 = continuer, 1 = stop


# Fonction pour générer un nombre premier aléatoire en binaire
def generate_random_prime(bits=24):
    while True:
        candidate = int.from_bytes(os.urandom(bits // 8), "big")  # Vrai aléatoire
        candidate |= (1 << (bits - 4))  # 🔥 Force le bit de poids fort à 1
        if sympy.isprime(candidate):
            return candidate


def has_prime_mutation(hex_prime):
    """Teste toutes les mutations d'un nombre hexadécimal et retourne une liste de mutations premières."""
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
                with no_mutation_streak.get_lock():
                    no_mutation_streak.value = 0
                return True  # ⛔ Arrêt immédiat pour ce nombre (pas besoin de continuer)

            with no_mutation_streak.get_lock():
                no_mutation_streak.value += 1
                if no_mutation_streak.value > longest_streak.value:
                    longest_streak.value = no_mutation_streak.value

    return False


def worker():
    start_time = time.time()
    while True:
        # 🔴 Vérification du flag d'arrêt avant de continuer
        if stop_flag.value == 1:
            break

        with total_iterations.get_lock():
            total_iterations.value += 1

        prime_candidate = generate_random_prime()
        if (total_iterations.value % 10) == 0:
            print(f"🟢 {int(total_iterations.value)} nombres testés - Longest streak: {longest_streak.value}")

        result = has_prime_mutation(prime_candidate)
        if not result:
            end_time = time.time()
            print(
                f"🔥 Nombre trouvé après {total_iterations.value} tentatives en {end_time - start_time} sec.\n Monstre : {hex(prime_candidate)}")

            # 🛑 On met le flag d'arrêt à 1
            with stop_flag.get_lock():
                stop_flag.value = 1

            break


if __name__ == "__main__":
    num_processes = 8  # Lancer 8 processus en parallèle
    processes = []

    for _ in range(num_processes):
        p = multiprocessing.Process(target=worker)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
        print(f"✅ Process {p.pid} terminé.")

    print("🔄 Relance automatique...")
    time.sleep(2)
    os.execv(sys.executable, ['python'] + sys.argv)  # Redémarre le script
