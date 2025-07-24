import sympy
import math
import numpy as np
import pandas as pd
import time
import multiprocessing
import random


def algop(p):
    """ Exécution d'Algo(p) si p est premier """
    if (16 % p == 1):
        return 1
    if sympy.isprime(p):
        n = 1
        while pow(16, n, p) != 1:
            n += 1
    else:
        n = None
    return n


def get_prime_cycle(k=16, p=61681, max_iter=500):
    """ Calcul du cycle complet jusqu'à ce que la valeur revienne à 1 ou dépasse max_iter """
    cycle_values = [1]
    kmodp = k % p
    if kmodp == 1:
        cycle_values.append(kmodp)
        return cycle_values
    if kmodp == p - 1:
        cycle_values.append(-1)
        return cycle_values
    value = 1
    for _ in range(max_iter):
        value = (value * k) % p
        if value == 1:
            break
        cycle_values.append(value)
    return cycle_values


def analyze_cycle(p1, p2):
    """ Analyse du cycle et vérification de primalité """
    is_p1prime = sympy.isprime(p1)
    is_p2prime = sympy.isprime(p2)
    print(f"Is p1 Prime ? {is_p1prime}\nIs p2 Prime? {is_p2prime}")

    cycle_p1 = get_prime_cycle(16, p1, max_iter=500)
    df_p1 = pd.DataFrame({"n": range(len(cycle_p1)), f"16^n % {p1}": cycle_p1})
    print(f"\nCycle des puissances de 16 modulo {p1} :")
    print(df_p1)

    cycle_p2 = get_prime_cycle(16, p2, max_iter=500)
    df_p2 = pd.DataFrame({"n": range(len(cycle_p2)), f"16^n % {p2}": cycle_p2})
    print(f"\nCycle des puissances de 16 modulo {p2} :")
    print(df_p2)

    return df_p1, df_p2


def find_prime_cycles(start, end, max_n=260, max_attempts=10000):
    """ Recherche probabiliste des nombres premiers respectant la condition et analyse en parallèle """
    matching_pairs = []
    prev_p = None  # Stocke le précédent p pour comparaison
    checked_primes = set()  # Stocke les nombres premiers déjà testés
    attempts = 0  # Compteur d'essais
    min_cycle_found = float("inf")  # Stocke le plus petit cycle trouvé
    start_time = time.time()

    while attempts < max_attempts:
        attempts += 1
        if (attempts % (10**7) == 0):
            print(f"📌 Deja {(attempts/(10**7))*10} million d'itérations ! Taille du plus petit cycle trouvé : {min_cycle_found}\nContinuing from... : {prev_p}")
        p = random.randint(start, end)  # Génération d'un nombre aléatoire
        if p in checked_primes or not sympy.isprime(p):  # Vérification de primalité et exclusion des doublons
            continue

        checked_primes.add(p)  # Ajout du nombre premier à l'ensemble des nombres testés
        #print(f"[{attempts}] Found Prime: {p} : Testing cycles...")
        cycle_values = get_prime_cycle(16, p, max_iter=max_n)
        cycle_length = len(cycle_values)
        min_cycle_found = min(min_cycle_found, cycle_length)  # Mise à jour du plus petit cycle trouvé

        if cycle_length >= max_n:
            #print(f"[{attempts}] Discarded {p} - Taille du cycle : {cycle_length}+")
            continue  # On ignore ce nombre définitivement en l'ayant ajouté à checked_primes

        matching_pairs.append((p, cycle_length))
        print(f"[{attempts}] Appended :{(p, cycle_length)}")

        if prev_p is not None:
            process = multiprocessing.Process(target=analyze_cycle, args=(prev_p, p))
            process.start()

        prev_p = p  # Mise à jour du précédent p

    elapsed_time = time.time() - start_time
    print(
        f"\nMax attempts reached. Stopping search. Smallest cycle found: {min_cycle_found}. Time elapsed: {elapsed_time:.2f}s")
    df_matching = pd.DataFrame(matching_pairs, columns=["p", "n"])
    return df_matching


if __name__ == "__main__":
    p1 = 641
    p2 = 90289

    # Vérification de Primalité
    is_p1prime = sympy.isprime(p1)
    is_p2prime = sympy.isprime(p2)
    print(f"Is p1 Prime ? {is_p1prime}\nIs p2 Prime? {is_p2prime}")

    # Recherche des nombres premiers respectant la condition avec exécution parallèle
    n_magique = int(math.pow(16, 4))
    n_magique_plus = int(math.pow(16, 8))
    df_result = find_prime_cycles(n_magique, n_magique_plus, 1024, 10 ** 9)
    print("\nNombres premiers trouvés respectant la condition :")
    print(df_result)
