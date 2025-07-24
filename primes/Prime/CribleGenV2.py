import numpy as np
import sympy
import time
import multiprocessing
import os

def process_segment(low, high, small_primes, output_file):
    """
    Traite un segment donné et écrit les nombres premiers trouvés dans un fichier.
    """
    sieve = np.ones(high - low + 1, dtype=bool)

    for p in small_primes:
        start = max(p * p, low + (p - low % p) % p)
        sieve[start - low::p] = False

    # Écrire les nombres premiers du segment dans le fichier
    with open(output_file, "a") as f:
        for prime in np.nonzero(sieve)[0] + low:
            f.write(f"{prime}\n")

def segmented_sieve_parallel(limit, segment_size=10 ** 7, output_file="primes.txt", num_workers=4):
    """
    Génère les nombres premiers jusqu'à 'limit' en utilisant un crible segmenté et du multi-processing.

    :param limit: La borne supérieure pour la génération des nombres premiers
    :param segment_size: Taille des segments de calcul
    :param output_file: Fichier pour stocker les nombres premiers
    :param num_workers: Nombre de processus à utiliser
    """
    print(
        f"Génération des nombres premiers jusqu'à {limit} avec un crible segmenté multi-thread ({num_workers} workers)...")
    start_time = time.time()

    sqrt_limit = int(np.sqrt(limit)) + 1
    small_primes = list(sympy.primerange(2, sqrt_limit))

    # Écriture des petits nombres premiers dans le fichier
    with open(output_file, "w") as f:
        f.write("\n".join(map(str, small_primes)) + "\n")

    # Création des tâches pour le multi-processing
    tasks = []
    for low in range(sqrt_limit, limit + 1, segment_size):
        high = min(low + segment_size - 1, limit)
        tasks.append((low, high, small_primes, output_file))

    with multiprocessing.Pool(processes=num_workers) as pool:
        pool.starmap(process_segment, tasks)

    end_time = time.time()
    print(f"Génération terminée en {end_time - start_time:.2f} secondes. Résultats stockés dans {output_file}.")

    # Demander à l'utilisateur s'il veut supprimer le fichier
    clear_file = input("Voulez-vous supprimer le fichier de résultats ? (o/n): ").strip().lower()
    if clear_file == 'o':
        os.remove(output_file)
        print("Fichier supprimé.")

if __name__ == "__main__":
    # Test avec une limite plus grande
    LIMIT = 10 ** 11
    segmented_sieve_parallel(LIMIT, segment_size=10 ** 7, num_workers=4)

    # Affichage des 3 derniers nombres premiers stockés
    with open("primes.txt", "r") as f:
        last_three_primes = list(f)[-3:]
        print(f"Les 3 derniers nombres premiers générés: {last_three_primes}")
