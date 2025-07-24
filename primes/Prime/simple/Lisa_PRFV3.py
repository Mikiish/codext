import random
import time
from sympy import isprime, factorint
from Crypto.Util import number

def is_hex_prime(hex_str):
    """Vérifie si un nombre hexadécimal est premier en le testant en base 10."""
    if not hex_str:
        return False
    try:
        decimal_value = int(hex_str, 16)
        return number.isPrime(decimal_value)
    except ValueError:
        return False

def pollards_rho(n, timeout=300):
    """Implémente l'algorithme de Pollard's Rho avec un timeout."""
    if n <= 1:
        return None

    start_time = time.time()
    if n % 2 == 0:
        return 2

    x = random.randint(1, max(2, n - 1))
    y = x
    c = random.randint(1, max(2, n - 1))
    f = lambda x: (x * x + c) % n
    d = 1
    while d == 1:
        if time.time() - start_time > timeout:
            print("Timeout atteint pour Pollard's Rho. Passage à la recherche probabiliste.")
            return None
        x = f(x)
        y = f(f(y))
        d = number.GCD(abs(x - y), n)
        if d == n:
            return None
    return d

def probabilistic_factorization(n, min_size, max_size, max_attempts=1000):
    """Essaie de trouver un facteur en générant des nombres aléatoires."""
    print("Passage à l'algorithme probabiliste de factorisation...")
    for _ in range(max_attempts):
        candidate = random.randint(10**(min_size-1), 10**max_size - 1)
        if n % candidate == 0:
            print(f"Facteur trouvé par approche probabiliste : {hex(candidate).upper()[2:]}")
            return candidate
    print("Aucun facteur trouvé par approche probabiliste.")
    return None

def evaluate_prime_range(cofactor, decrement=0):
    """Détermine la plage de nombres premiers pertinents pour factoriser un cofacteur, en décrémentant à chaque timeout."""
    cofactor_size = len(hex(cofactor)[2:])
    min_size = max(2, cofactor_size // 2 - 1 - decrement)
    max_size = max(2, cofactor_size // 2 + 1 - decrement)
    return min_size, max_size

def factorize_number(hex_number, pollard_timeout=300, max_iterations=200):
    """Effectue la factorisation avec une limite d'itérations sur la boucle principale."""
    decimal_number = int(hex_number, 16)
    factors = []
    decrement = 0  # Variable pour réduire min_size et max_size après chaque timeout

    for iteration in range(max_iterations):
        print(f"\n--- Début de l'itération {iteration + 1} de la boucle principale ---")
        if decimal_number <= 1:
            print("Le nombre est trivial (<=1).")
            break
        if number.isPrime(decimal_number):
            print("Le dernier cofacteur est premier.")
            break

        min_size, max_size = evaluate_prime_range(decimal_number, decrement)
        print(f"Recherche de facteurs dans la plage de taille : {min_size}-{max_size}")
        print(f"Target : {hex(decimal_number).upper()[2:]}")

        factor = pollards_rho(decimal_number, pollard_timeout)
        if factor is None:
            decrement += 2  # Réduire la plage de recherche après un timeout
            factor = probabilistic_factorization(decimal_number, min_size, max_size)
            if factor is None:
                print("Timeout atteint pour la méthode probabiliste. Relance de la boucle principale.")
                continue

        if number.isPrime(factor):
            hex_factor = hex(factor).upper()[2:]
            factors.append(hex_factor)
        else:
            decimal_number = factor  # Continuer la factorisation
            continue

        decimal_number //= factor
        print(f"Facteur trouvé : {hex_factor}")
        print(f"Nouveau cofacteur : {hex(decimal_number).upper()[2:]}")

    print(f"Facteurs finaux : {factors}, Cofacteur restant : {hex(decimal_number).upper()[2:]}")
    return factors


# Lancer la factorisation avec limite d'itérations
if __name__ == "__main__":
    hex_number = "3512B41C9BFD239329866F8FC4A468A7A80CB4B9C6C8021B836BBA3C64101742A5B964FF80D921588586C55C6562A3BD959F9D9AFD2E4AF27A1D0AFC93A3B942E0F9B28B6149131D5D8BEA6611BD2B6DFAD0E31F1B4DE1A6D13E1B5E8CD0BCE5E37879FB7F7EC726D263B8BF387E9B0FB49267CA76575D4E6E94BCB0560A13"
    discovered_factors = factorize_number(hex_number, pollard_timeout=300, max_iterations=200)
    print(f"Facteurs finaux : {discovered_factors}")
