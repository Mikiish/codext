import json
import sympy
import time
from concurrent.futures import ThreadPoolExecutor

# Charger les cycles pré-calculés depuis le fichier JSON
def load_cycle_data():
    try:
        with open("cycle_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Cycle data not found! Please run `generate_cycle_data.py` first.")
        exit(1)

# Chargement des cycles
precomputed_cycles = load_cycle_data()
prime_table = [int(p) for p in precomputed_cycles.keys()] # Extraire la liste des premiers utilisés


# Pré-calcul des congruences des 4 derniers chiffres hex pour tous les nombres premiers jusqu'à 65536
def precompute_congruences(hex_number):
    last_4_digits = int(hex_number[-4:], 16)
    congruences = {p: last_4_digits % p for p in prime_table}
    return congruences


# Vérifie si un nombre est divisible par p en utilisant le cycle de congruence
def is_divisible_by_p(hex_number, p):
    cycle = precomputed_cycles[p]
    return sum(int(c, 16) * cycle[i % len(cycle)] for i, c in enumerate(reversed(hex_number))) % p == 0


# Retourne les caractères hexadécimaux à éviter pour éventuellement préserver la primalité
def discard_by_prime_cycle(index, prime, current_digit):
    hex_digits = "0123456789ABCDEF"
    hex_digits = hex_digits.replace(current_digit, "")

    if prime == 17:
        # Vérifier la somme alternée : (-1)^i * digit
        return [c for c in hex_digits if (int(c, 16) * (-1) ** index) % 17 == 0]

    elif prime in {3, 5}:
        # Garder uniquement les chiffres congrus au digit initial modulo p
        return [c for c in hex_digits if int(c, 16) % prime == int(current_digit, 16) % prime]

    cycle = precomputed_cycles.get(prime, [1])  # Par défaut, cycle = [1] pour p = 3 ou 5
    cycle_length = len(cycle)
    return [c for c in hex_digits if (int(c, 16) * cycle[index % cycle_length]) % prime == 0]


# Fonction principale de mutation des nombres premiers
def GetPrimeMutation(hex_prime):
    hex_digits = "0123456789ABCDEF"
    casino_prime = hex(hex_prime)[2:].upper()
    prime_list = []

    # Pré-calcul des congruences
    congruences = precompute_congruences(casino_prime)

    for index in range(len(casino_prime)):
        original_digit = casino_prime[-(index + 1)]
        for new_digit in hex_digits.replace(original_digit, ""):
            # Vérification par les critères de divisibilité pré-calculés
            if any(new_digit in discard_by_prime_cycle(index, p, original_digit) for p in prime_table):
                continue

            mutated = list(casino_prime)
            mutated[-(index + 1)] = new_digit
            mutated_hex = "".join(mutated)
            mutated_int = int(mutated_hex, 16)

            # Test final de primalité
            if sympy.isprime(mutated_int):
                print(f"Prime appended: {hex(mutated_int)}")
                prime_list.append(mutated_int)

    prime_list.append(hex_prime)
    return prime_list


def check_mutation(args):
    """Fonction exécutée en parallèle."""
    hex_prime, index, new_digit = args
    mutated = list(hex(hex_prime)[2:].upper())
    mutated[-(index + 1)] = new_digit
    mutated_hex = "".join(mutated)
    mutated_int = int(mutated_hex, 16)

    if sympy.isprime(mutated_int):
        return mutated_int
    return None  # Si non premier, on renvoie None


def GetPrimeMutationNaifThreaded(hex_prime):
    hex_digits = "0123456789ABCDEF"
    casino_prime = hex(hex_prime)[2:].upper()

    tasks = [
        (hex_prime, index, new_digit)
        for index in range(len(casino_prime))
        for new_digit in hex_digits.replace(casino_prime[-(index + 1)], "")
    ]

    prime_list = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(check_mutation, tasks)

    prime_list = [res for res in results if res is not None]
    return prime_list


# Fonction naive qui teste toutes les mutations sans optimisation
def GetPrimeMutationNaif(hex_prime):
    hex_digits = "0123456789ABCDEF"
    casino_prime = hex(hex_prime)[2:].upper()
    prime_list = []
    iter = 0
    iter_iner = 0

    for index in range(len(casino_prime)):  # Mutation sur tous les caractères
        iter += 1
        original_digit = casino_prime[-(index + 1)]
        for new_digit in hex_digits.replace(original_digit, ""):
            iter_iner += 1
            mutated = list(casino_prime)
            mutated[-(index + 1)] = new_digit
            mutated_hex = "".join(mutated)
            mutated_int = int(mutated_hex, 16)

            # Vérification rapide par critère de divisibilité (3, 5 et 17)
            #digit_sum = sum(int(c, 16) for c in mutated_hex)
            #if digit_sum % 3 == 0 or digit_sum % 5 == 0:
            #    continue
            # Test final de primalité sans optimisation
            if sympy.isprime(mutated_int):
                print(f"Prime appended at {iter}-th iteration.  : {hex(mutated_int)}")
                prime_list.append(mutated_int)

    prime_list.append(hex_prime)
    print(f"Total iter : {iter_iner}\nTotal prime appended : {len(prime_list)}")
    return prime_list


if __name__ == "__main__":
    #start_time = time.time()
    #prime_mutations_optimized = GetPrimeMutation(0xBA6E0C754A8A1443C12EC702DEFDAF866FED5591FA44CB13E5DE0F3BE38E15B886561E49999EFB4F7B7671423C44C27A71C2D1FDF86392683A148810C6B654A1E4CD13BAB0C96947A7E1FF9A0E3980B9F1A9608B0F9A324DE5F7E29281F38AB62FB34311756489C3C018CFC933269ACE359D8BDA74B333FEBAB8977D8ECBCE85F84A04B3EFCE28165827BA157E6A20F17321008FF73EB0F3CA40FCECA6418B489B1E0ADEE4E9C6943B7AA43808138609A0AC2F17F4A44D5AB5DE5F3963B4FFD5D51C67BA9E3C461E796973BBE29228DE413910203005C64B4AD9678B5F61014BFD9B0F126916459AA81AF808E55DE6E8366FCC7D1A697EA70104A5B1524F16AA1C8364E7B)
    #end_time = time.time()
    #print(f"Optimisé : {len(prime_mutations_optimized)} mutations trouvées en {end_time - start_time:.4f} sec.")

    start_time = time.time()
    prime_mutations_naif = GetPrimeMutationNaif(0x97dbc121d8683839a1fa8180306d382c297ae639c90a4b89b69d18dec3b1471de84c5449df53c1fbd0f853a77d3f04826ab87a1ff613ce215b6ba7228cacf177210f47166ddd0cc37f0786dd80a4ccedc32949abc1ed99f2c0c28a179ec13a6ffdee9133c7247a383ee9b8e8913497e765bad77e69edb5c1d9d07d88eeac727d15359282b171ed3f9a971bcf9260264806dde6b61e6e47697844f1508ef02d40f2d76546beacbf8f585d2d657866dd1b0c720b0a45cb2f8eb8d82c76d15ae1e64f4a4d430880a2c2464207fdaba71878aa52331febe6a2c5ab5887cd7691b7912e3fe3157cf9fc6ffe83e22857558a7bc797809847f0c534b8ec1f4c692a09ab7849e315d
               )
    end_time = time.time()
    print(f"Naïf : {len(prime_mutations_naif)} mutations trouvées en {end_time - start_time:.4f} sec.")

    # Comparaison des résultats
    #diff = set(prime_mutations_naif) - set(prime_mutations_optimized)
    #if diff:
    #    for i in diff:
    #        print(f"⚠️ Attention, mutation absente de la version optimisée : {hex(i)}")
    #else:
    #    print("✅ Toutes les mutations naïves sont bien conservées dans la version optimisée.")