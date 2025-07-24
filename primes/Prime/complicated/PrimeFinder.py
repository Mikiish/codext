import pandas as pd
import sympy

def find_prime_cycles(start, end, max_n):
    """
    Recherche des nombres premiers p dans l'intervalle [start, end]
    pour lesquels il existe un n tel que 16^n ≡ p - 1 (mod p).
    Filtre les résultats pour ne garder que ceux avec n <= max_n.
    """
    prime_candidates = list(sympy.primerange(start, end))  # Liste des nombres premiers dans l'intervalle donné
    matching_pairs = []

    for p in prime_candidates:
        value = 1
        n = 0
        while n < p:  # On cherche jusqu'à trouver p-1 ou dépasser p
            value = (value * 16) % p
            n += 1
            if value == p - 1:
                if n <= max_n:  # Filtrage par max_n
                    matching_pairs.append((p, n))
                break

    # Conversion en DataFrame pour affichage
    df_matching = pd.DataFrame(matching_pairs, columns=["p", "n"])
    return df_matching

# Exemple d'utilisation
df_result = find_prime_cycles(61681, (61681 ** 61681), 42)
print(df_result)
