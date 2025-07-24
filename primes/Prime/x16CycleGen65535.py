import sympy
import json

# Génération des cycles modulo 16 pour tous les nombres premiers utiles
def generate_cycle_data(limit=0xFFFF):
    cycle_data = {}
    prime_table = [p for p in sympy.primerange(6, limit)]

    for p in prime_table:
        cycle = []
        val = 1
        iteration = 0  # Compteur de sécurité
        print(f"Calcul du cycle pour p = {p}...")
        while True:
            cycle.append(val)
            val = (val * 16) % p
            iteration += 1
            if val in cycle:
                print(f"Cycle détecté pour p = {p}, longueur = {len(cycle)}")
                break

        cycle_data[p] = cycle  # On stocke uniquement le cycle réduit

    # Gestion du cas spécifique de 17 (-1 mod 17)
    cycle_data[17] = [-1]

    with open("cycle_data.json", "w") as f:
        json.dump(cycle_data, f, indent=4)

    print(f"Cycle data saved to cycle_data.json with {len(cycle_data)} primes.")

if __name__ == "__main__":
    generate_cycle_data()