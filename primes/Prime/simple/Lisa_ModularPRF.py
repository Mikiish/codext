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


def factorize_block(hex_block):
    """Factorise un bloc hexadécimal donné en base 10."""
    decimal_number = int(hex_block, 16)
    factors = []

    try:
        factors_dict = factorint(decimal_number)
        for factor, count in factors_dict.items():
            factors.extend([hex(factor).upper()[2:] for _ in range(count)])
    except Exception:
        print(f"Échec de la factorisation pour {hex_block}")

    return factors


def modular_factorization(hex_number, block_size=105):
    """Effectue une factorisation progressive en divisant le nombre en blocs."""
    factors_candidates = set()
    decimal_number = int(hex_number, 16)
    hex_str = hex_number.upper()

    num_blocks = len(hex_str) // block_size

    for i in range(num_blocks):
        start_index = i * block_size
        end_index = start_index + block_size

        if end_index > len(hex_str):
            end_index = len(hex_str)

        hex_block = hex_str[start_index:end_index]
        print(f"\nBloc {i + 1}: {hex_block}")

        factors = factorize_block(hex_block)
        print(f"Facteurs trouvés: {factors}")
        factors_candidates.update(factors)

    print("\n--- Vérification des facteurs sur d'autres blocs ---")
    confirmed_factors = []

    for factor in factors_candidates:
        decimal_factor = int(factor, 16)
        if decimal_number % decimal_factor == 0:
            print(f"Facteur confirmé: {factor}")
            confirmed_factors.append(factor)

    return confirmed_factors


# Lancer la factorisation progressive
if __name__ == "__main__":
    hex_number = "82615181DE866BA8E04F829A670BB81496A2DDB386F72EEB009243F792A8E84653D5370340A74546EA72F633429FA68C72F0491C4ECF3AA200D930F0BF862595C2F7FBED25DA234DB9FB2014F1C5B93FED9B2C18D414C8FAC93A13EAC71E24E03C780F193A265A4830B7889B994DBCE554BD1CDEBB6DCD76843"
    discovered_factors = modular_factorization(hex_number, block_size=105)
    print(f"\nFacteurs finaux confirmés : {discovered_factors}")
