from sympy import isprime, factorint
import random
from decimal import Decimal
from Crypto.Util.number import getStrongPrime


def generate_strong_prime_hex(size):
    """
    Génère un nombre premier fort en hexadécimal de taille spécifiée.
    :param size: int, taille en bits du nombre premier
    :return: str, nombre premier en hexadécimal
    """
    prime = getStrongPrime(size)
    hex_prime = format(prime, 'X')  # Conversion en hexadécimal
    if len(hex_prime) % 2 != 0:
        hex_prime = '0' + hex_prime  # S'assurer que la longueur est paire
    return hex_prime


def apply_z2xz2_mutation(hex_str):
    """
    Applique la transformation Z2xZ2 sur les bits du milieu du nombre hexadécimal.
    :param hex_str: str, nombre hexadécimal
    :return: str, nombre hexadécimal muté
    """
    mid_index = len(hex_str) // 2
    mid_chars = hex_str[mid_index - 1: mid_index + 1]  # Extraction des 2 caractères centraux

    # Transformation Z2xZ2 : flip XOR tout en garantissant un caractère hexadécimal valide
    mutated_chars = format((int(mid_chars, 16) ^ 0b11) & 0xFF, '02X')

    mutated_hex = hex_str[:mid_index - 1] + mutated_chars + hex_str[mid_index + 1:]

    # Vérification que le nombre muté reste impair (évite les nombres pairs non premiers)
    if int(mutated_hex[-1], 16) % 2 == 0:
        mutated_hex = mutated_hex[:-1] + 'F'  # Force le dernier chiffre à être impair

    return mutated_hex


def hex_to_decimal(hex_str):
    """
    Convertit un nombre hexadécimal en décimal avec précision améliorée.
    :param hex_str: str, Nombre en base 16 sous forme de chaîne de caractères
    :return: str, Nombre en base 10 sous forme de chaîne de caractères
    """
    try:
        decimal_value = Decimal(int(hex_str, 16))  # Conversion avec Decimal pour éviter les pertes de précision
        return str(decimal_value)  # Retourner sous forme de chaîne pour éviter les dépassements
    except ValueError as e:
        return f"Erreur : Impossible de convertir. Détail : {e}"


# Génération d'un nombre premier en hexadécimal
original_hex = generate_strong_prime_hex(1024)
mutated_hex = apply_z2xz2_mutation(original_hex)

# Vérification de primalité
original_decimal = int(original_hex, 16)
mutated_decimal = int(mutated_hex, 16)

print("Analyse de la mutation :")
print(f"Nombre original : {original_hex}")
print(f"Nombre muté     : {mutated_hex}")

if isprime(original_decimal):
    print("✅ Le nombre original est premier.")
else:
    print("❌ Le nombre original n'est PAS premier. Problème détecté !")

if isprime(mutated_decimal):
    print("✅ Le nombre muté est toujours premier !")
else:
    print("❌ Le nombre muté n'est PAS premier. Facteurs en cours de recherche...")


    def factor_with_timeout(n, timeout_sec=10):
        """Essaye de factoriser un nombre avec un timeout strict."""
        try:
            factors = factorint(n, limit=10 ** 6)  # Limite les tentatives sur de grands nombres
            return factors
        except Exception as e:
            return f"Erreur lors de la factorisation : {e}"


    factors = factor_with_timeout(mutated_decimal)
    print(f"Facteurs trouvés pour le nombre muté :\n{[hex(factor).upper()[2:] for factor in factors]}")