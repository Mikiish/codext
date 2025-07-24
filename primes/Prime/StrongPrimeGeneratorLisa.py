import random
from sympy import randprime

def generate_strong_prime_hex_optimized(hex_length=1024):
    """Génère un nombre premier fort en hexadécimal de la taille demandée."""
    bit_length = hex_length * 4  # 1 hex = 4 bits

    # Définir une plage autour d'un grand nombre aléatoire
    lower_bound = random.getrandbits(bit_length - 1) | (1 << (bit_length - 1))  # Assure un nombre de bit_length bits
    upper_bound = lower_bound + (1 << 20)  # Recherche un premier proche

    # Trouver un nombre premier dans cet intervalle restreint
    strong_prime = randprime(lower_bound, upper_bound)

    # Convertir en hexadécimal et s'assurer de la bonne longueur
    strong_prime_hex = hex(strong_prime)[2:].upper().zfill(hex_length)
    print(f"GigaPrime : {strong_prime_hex}")
    return strong_prime_hex

def generate_strong_prime_hex_optimized_mutated(hex_length=1024):
    """Génère un nombre premier fort en hexadécimal de la taille demandée."""
    bit_length = hex_length * 4  # 1 hex = 4 bits

    # Définir une plage autour d'un grand nombre aléatoire
    lower_bound = (1 << (bit_length - 1))  # 4096 bits forcé
    upper_bound = (1 << bit_length) - 1  # Prend tous les nombres 4096 bits

    # Trouver un nombre premier dans cet intervalle restreint
    strong_prime = randprime(lower_bound, upper_bound)
    strong_prime_hex = hex(strong_prime)[2:].upper().zfill(hex_length)  # Force la taille à 1024

    # Vérifier que la taille est correcte
    if len(strong_prime_hex) != hex_length:
        raise ValueError(f"Taille incorrecte après conversion : {len(strong_prime_hex)}")

    middle_char = strong_prime_hex[512:514]  # Extraire les 2 caractères du milieu
    #if middle_char == "00":
    strong_prime_hex = strong_prime_hex[:512] + "7" + strong_prime_hex[514:]  # Remplacement
    strong_prime = int(strong_prime_hex, 16)  # Reconversion en entier

    # Vérification finale
    print(f"GigaLouche : {strong_prime_hex} (Taille : {len(strong_prime_hex)})")
    return strong_prime

# Générer un nombre premier fort de 1024 caractères hexadécimaux avec une meilleure approche
strong_prime_hex_optimized = generate_strong_prime_hex_optimized(1024)
strong_prime_hex_upmutated = generate_strong_prime_hex_optimized_mutated(1024)