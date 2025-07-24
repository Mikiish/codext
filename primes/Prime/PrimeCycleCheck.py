import sympy
from sympy import factorint, isprime
import numpy as np

# Définition de Phi2 en décimal
phi2_dec = int("96cae7",
               16)

# Test de Carmichael
def is_carmichael(n):
    factors = factorint(n)
    if len(factors) < 3:
        return False  # Un nombre de Carmichael a au moins 3 facteurs premiers
    for p in factors:
        if (n - 1) % (p - 1) != 0:
            return False
    return True

carmichael_test = is_carmichael(phi2_dec)

# Analyse de la structure binaire
phi2_bin = bin(phi2_dec)[2:]  # Conversion en binaire
bit_density = phi2_bin.count("1") / len(phi2_bin)  # Ratio de 1 sur la longueur totale

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

# Analyse de Fourier pour détecter d'éventuelles symétries cachées
def fourier_analysis(binary_str):
    binary_array = np.array([int(b) for b in binary_str])
    spectrum = np.fft.fft(binary_array)
    return np.abs(spectrum)

fourier_spectrum = fourier_analysis(phi2_bin)

# Transformée de Fourier inverse
def inverse_fourier_analysis(spectrum):
    inverse_transform = np.fft.ifft(spectrum)
    return np.real(inverse_transform)

inverse_fourier_spectrum = inverse_fourier_analysis(fourier_spectrum)

# Test d'exponentiation modulaire
def modular_exponentiation_test(n, base=3, mod=521):
    return pow(base, n, mod)

mod_exp_result = modular_exponentiation_test(phi2_dec)

# Approximation logarithmique pour grands nombres
def approximate_log(n, base=10, order=10):
    """
    Approche de l'estimation du logarithme naturel d'un grand nombre
    en utilisant une expansion en série de Taylor centrée sur une approximation initiale.
    """
    n = sympy.Float(n)  # Utilisation de la précision arbitraire de Sympy
    ln_approx = sympy.log(n)  # Calcul précis avec sympy
    return float(ln_approx) / np.log(base)

# Test de transformation logarithmique
log_transform_result = approximate_log(phi2_dec)

# Projection sur la base de Pisano
def pisano_period(n, m=10):
    previous, current = 0, 1
    for i in range(0, m * m):
        previous, current = current, (previous + current) % m
        if previous == 0 and current == 1:
            return i + 1
    return -1

pisano_result = pisano_period(phi2_dec)

# Affichage des résultats
if __name__ == "__main__":
    print("Phi2 est-il un nombre de Carmichael ?", carmichael_test)
    print("Densité des bits à 1 :", bit_density)
    print("Reste modulaire avec petits nombres premiers :", mod_factors)
    print("Représentation 521-adique (premiers 20 chiffres) :", phi2_521_adic[:20])
    print("Spectre de Fourier (premiers 10 coefficients) :", fourier_spectrum[:10])
    print("Transformée de Fourier inverse (premiers 10 valeurs) :", inverse_fourier_spectrum[:10])
    print("Résultat de l'exponentiation modulaire :", mod_exp_result)
    print("Résultat de la transformation logarithmique :", log_transform_result)
    print("Période de Pisano associée :", pisano_result)
