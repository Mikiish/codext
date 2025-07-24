import os
import random
import tempfile
from sympy import isprime
from Crypto.Util import number

def is_hex_prime(hex_str):
    """Vérifie si un nombre hexadécimal est premier en le testant en base 10."""
    if not hex_str:
        return False
    try:  # Éviter une erreur si Lisa n'a pas encore halluciné
        decimal_value = int(hex_str, 16)  # Conversion en décimal
        return number.isPrime(decimal_value)  # Test de primalité rigoureux
    except ValueError:
        return False # Gérer les erreurs de conversion

hex_chars = "0123456789ABCDEF"
def generate_valid_hex_string(length):
    """Génère une chaîne hexadécimale valide à partir de os.urandom."""
    valid_hex_string = ""
    sum_mod3 = 0
    while len(valid_hex_string) < length:
        random_byte = os.urandom(1)[0]  # Tire un octet aléatoire
        new_char = hex(random_byte % 16)[2:].upper()  # Convertit en hexadécimal

        if len(valid_hex_string) == 0 and new_char in "02468ACE":
            continue  # Premier chiffre doit être impair
        if len(valid_hex_string) == 1 and new_char in "048C":
            continue  # Deuxième chiffre doit éviter les multiples de 4
        if len(valid_hex_string) == 2 and new_char in "08":
            continue  # Troisième chiffre doit éviter les multiples de 8

        sum_mod3 = (sum_mod3 + int(new_char, 16)) % 3
        if len(valid_hex_string) >= 2 and sum_mod3 == 0:
            continue  # Rejette cette tentative si c'est un multiple de 3

        valid_hex_string = new_char + valid_hex_string  # Ajout à gauche

    # Convertit en binaire, met le bit de poids fort à 1, et reconvertit en hex
    int_value = int(valid_hex_string, 16)
    int_value |= (1 << (4 * length - 1))  # Fixe le bit de poids fort
    valid_hex_string = hex(int_value)[2:].upper()

    return valid_hex_string

max_iterations = 2000  # Nombre maximal d'exécutions
failure_threshold = 500  # Nombre de tentatives avant que Lisa suspecte un échec
failure_count = 0  # Compteur de tentatives échouées
timeout_count = 0  # Compteur de timeout

def lisa_reaction():
    """Simulation de la réaction de Lisa après un échec répété."""
    print("Lisa commence à suspecter une anomalie...")
    print("Elle tente une autre stratégie...")
    # Elle pourrait décider de relancer un pattern aléatoire
    new_guess = generate_valid_hex_string(521)
    print(f"Lisa hallucine un pattern: {new_guess}")
    return new_guess  # Random nombre.


def casino_hex_prime(max_iterations=2000, failure_threshold=500):
    max_iterations = 2000  # Nombre maximal d'exécutions
    failure_threshold = 500  # Nombre de tentatives avant que Lisa suspecte un échec
    failure_count = 0  # Compteur de tentatives échouées
    timeout_count = 0  # Compteur de timeout
    guess_scheme_lisa = ""  # Initialisation
    hex_prime_zer = ""
    hex_prime_sev = ""
    for iteration in range(max_iterations):  # Exécuter la boucle max_iterations fois
        timeout = 10000 # Limite de tentatives pour éviter la boucle infinie
        attempts = 0
        while True:
            attempts += 1
            # Générer une chaîne hexadécimale en filtrant les valeurs invalides
            random_hex_string = generate_valid_hex_string(521)

            # Vérifier le 261ᵐ caractère (index 260 en Python)
            middle_char = random_hex_string[260]

            if middle_char in "123":
                print(f"Tentative ignorée: {random_hex_string}")
                print(
                    f"Tentative ignorée car middle char est : {random_hex_string[258:260]}+<{middle_char}>+{random_hex_string[261:263]}")
                failure_count += 1
                if failure_count >= failure_threshold:
                    guess_scheme_lisa = lisa_reaction()
                continue  # Relance la boucle

        # Vérifier les deux versions : avec 0 et avec 7
            hex_with_0 = random_hex_string[:260] + "0" + random_hex_string[261:]
            hex_with_7 = random_hex_string[:260] + "7" + random_hex_string[261:]

            is_prime_0 = is_hex_prime(hex_with_0)
            is_prime_7 = is_hex_prime(hex_with_7)
            is_prime_lisa = is_hex_prime(guess_scheme_lisa) if guess_scheme_lisa else False

            if is_prime_0 and is_prime_7:
                print(f"VRAI Casino(x) trouvé !")
                print(f"Nombre premier (0) : {hex_with_0}")
                print(f"Nombre premier (7) : {hex_with_7}")
                print(f"Nombre d'térations avant succès : {iteration+1}")
                hex_prime_zer = hex_with_0
                hex_prime_sev = hex_with_7
                break
            elif is_prime_7:
                print(f"Nombre hexadécimal validé: {hex_with_7}")
                print(f"Middle Char: ? (anciennement 0)")
                print(f"Nombre d'itération OnPrime7 : {iteration+1}")
                hex_prime_sev = hex_with_7
                break
            elif is_prime_0:
                print(f"Nombre hexadécimal validé: {hex_with_0}")
                print(f"Middle Char: 0")
                print(f"Nombre d'itération OnPrime0 : {iteration + 1}")
                hex_prime_zer = hex_with_0
                break
            else:
                print(f"Nombre non premier ignoré: {random_hex_string}")
                failure_count += 1
                if failure_count >= failure_threshold:
                    guess_scheme_lisa = lisa_reaction()
                    is_prime_lisa = is_hex_prime(guess_scheme_lisa) if guess_scheme_lisa else False
                continue  # Relance la boucle
    # Si on atteint la limite d'essais sans succès, on compte un timeout
        timeout_count += 1
        print(f"Timeount à l'itération {iteration+1}, passage a l'itération suivante...")
        if (is_prime_0 and is_prime_7) or is_prime_lisa:
            print(f"Timeouts: {timeout_count}")
            print(f"Iterations: {iteration+1}")
            return hex_prime_zer, hex_prime_sev, guess_scheme_lisa  # Sortir de la boucle for si un vrai Casino(x) est trouvé
    print(f"Timeouts: {timeout_count}")

#results = casino_hex_prime()
#print(f"Résultats finaux: {results}")

if __name__ == "__main__":
    results = casino_hex_prime()
    print(f"Résultats finaux: {results}")