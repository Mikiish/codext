import sympy
import numpy as np
import random
import array
from sympy import factorint, isprime
import primes.Prime.complicated.IsPrime as IsPrime

# Définition de Phi2 en décimal
phi2_dec = 0x96cae7
phi2_hex = 0x96cae7

# Test de Miller-Rabin
def is_prime(n, k=40):
    """Test de primalité de Miller-Rabin avec k itérations (fiabilité élevée)."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Trouver d tel que n-1 = d * 2^r avec d impair
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Test de Miller-Rabin
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def hex_is_prime(hex_number):
    """Convertit un nombre hexadécimal en entier et teste sa primalité."""
    decimal_value = int(hex_number, 16)
    return is_prime(decimal_value)

# Test de Carmichael
def is_carmichael(n):
    factors = factorint(n)
    if len(factors) < 3:
        return False  # Un nombre de Carmichael a au moins 3 facteurs premiers
    for p in factors:
        if (n - 1) % (p - 1) != 0:
            return False
    return True

# Test de Sophie Germain
def is_sophie_germain_prime(n):
    return isprime(n) and isprime(2 * n + 1)

# Conversion dans différentes bases pour observer les patterns
def to_base(n, base):
    digits = []
    while n:
        digits.append(n % base)
        n //= base
    return digits[::-1]

# Analyse de la fréquence des bits via la transformée de Fourier
def fourier_analysis(binary_str):
    bit_array = np.array([int(bit) for bit in binary_str])
    spectrum = np.fft.fft(bit_array)
    return np.abs(spectrum)[:20]  # Garder les 20 premières fréquences

# Analyse de la structure binaire
phi2_bin = bin(phi2_dec)[2:]  # Conversion en binaire
bit_density = phi2_bin.count("1") / len(phi2_bin)  # Ratio de 1 sur la longueur totale
fourier_spectrum = fourier_analysis(phi2_bin)
bases_to_test = [3, 7, 11, 17, 19, 23]
base_representations = {base: to_base(phi2_dec, base)[:20] for base in bases_to_test}
sophie_germain_test = is_sophie_germain_prime(phi2_dec)
#carmichael_test = is_carmichael(phi2_dec)
isprime_test = is_prime(phi2_hex)


# Factorisation modulaire
prime_mod_tests = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
mod_factors = {p: phi2_dec % p for p in prime_mod_tests}

# Représentation 521-adique
def to_p_adic(n, p):
    digits = []
    while n:
        digits.append(n % p)
        n //= p
    return digits[::-1]

phi2_521_adic = to_p_adic(phi2_dec, 521)

# Affichage des résultats
if __name__ == "__main__":
    print("Phi2 est-il premier ?", isprime_test)
    #print("Phi2 est-il un nombre de Carmichael ?", carmichael_test)
    print("Densité des bits à 1 :", bit_density)
    print("Reste modulaire avec petits nombres premiers :", mod_factors)
    print("Représentation 521-adique (premiers 20 chiffres) :", phi2_521_adic[:20])
    print("Phi2 est-il un nombre de Sophie Germain ?", sophie_germain_test)
    print("Représentations dans différentes bases (premiers 20 chiffres) :", base_representations)
    print("Analyse spectrale (premières 20 fréquences) :", fourier_spectrum)
