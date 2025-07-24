#!/usr/bin/env python3

import sympy
import time

START = 133007279  # 4194304
END   = 2**28

def has_prime_mutation(num_int):
    """
    Retourne True si le nombre 'num_int' (supposé prime) a au moins UNE mutation hex
    qui soit elle-même prime.
    Retourne False si AUCUNE mutation n'est prime (i.e. 'num_int' est 'isolé').
    """
    hex_digits = "0123456789ABCDEF"
    hex_str = format(num_int, 'X')  # Représentation hex majuscule
    length = len(hex_str)

    for i in range(length):
        orig_digit = hex_str[i]
        for new_digit in hex_digits:
            if new_digit == orig_digit:
                continue

            # Créer la mutation
            mutated_hex = hex_str[:i] + new_digit + hex_str[i+1:]

            mutated_int = int(mutated_hex, 16)
            # Test de primalité sur la mutation
            if sympy.isprime(mutated_int):
                return True  # On a trouvé une mutation prime, plus besoin de continuer
    return False

def main():
    t0 = time.time()

    count_checked = 0
    count_isolated = 0

    print(f"Recherche de nombres premiers 'isolés' dans [{START}, {END}]...")
    # Utilisation de sympy.primerange(start, end) pour itérer sur tous les premiers
    for prime_candidate in sympy.primerange(START, END+1):
        count_checked += 1

        # Vérifie si ce prime a au moins une mutation prime
        if not has_prime_mutation(prime_candidate):
            # => Aucune mutation n'est prime => prime 'isolé'
            count_isolated += 1
            print(f"[ISOLE] 0x{prime_candidate:X} = {prime_candidate}")

    t1 = time.time()
    print(f"\nTerminé ! {count_checked} nombres premiers testés.")
    print(f"{count_isolated} étaient isolés.")
    print(f"Durée : {t1 - t0:.2f} s")

if __name__ == "__main__":
    main()
