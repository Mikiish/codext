import random
import array
import numpy as np
import matplotlib.pyplot as plt
import PrimeMutationFilter
from sympy import isprime
from scipy.stats import linregress
from sympy.physics.quantum.qexpr import QuantumError


class QuantumState:
    def __init__(self, possible_states, hidden_variable=None):
        self.possible_states = possible_states  # Liste des états possibles
        self.state = None  # Indéterminé tant qu'aucune mesure
        self.hidden_variable = hidden_variable if hidden_variable is not None else random.random()
        self.measured = False

    def measure(self):
        """
        Simule l'effondrement de la fonction d'onde.
        L'état final est influencé par la variable cachée.
        """
        if not self.measured:
            weight = [abs(self.hidden_variable - i) for i in range(len(self.possible_states))]
            self.state = self.possible_states[
                weight.index(min(weight))]  # Choisit l'état le plus proche de la variable cachée
            self.measured = True
        return self.state

    def reset(self):
        """Remet l'état en superposition."""
        self.state = None
        self.measured = False

# Mutation inversée : Chercher un chemin vers un voisin premier
def inverse_mutation_search(n, max_steps=7):
    path = []  # Stocke le chemin des mutations
    quantum_state = QuantumState(n)  # Intégration de QuantumState
    quantum_state.measure()
    measured_state = quantum_state.state

    for _ in range(max_steps):
        n_str = list(hex(n)[2:].upper())
        mutation_index = random.randint(0, len(n_str) - 1)
        valid_digits = "0123456789ABCDEF".replace(n_str[mutation_index], "")
        n_str[mutation_index] = random.choice(valid_digits)
        new_n = int("".join(n_str), 16)
        path.append(new_n)  # Stocker chaque tentative

        if isprime(new_n):
            return new_n, path  # Retourne le nombre premier ET le chemin
    quantum_state.reset()
    return None, path

# Détection de nombres premiers robustes (mutants mathématiques) avec un score de stabilité
def mutate_number(hex_number, max_mutations=500000, tolerance=2084):
    decimal_number = int(hex_number, 16)
    original_prime = isprime(decimal_number)

    if not original_prime:
        return None, 0, 0  # Pas un mutant mathématique à l'origine

    stable_mutations = 0
    consecutive_fails = 0
    best_mutant = decimal_number  # Stocke le meilleur mutant
    mutation_history = []
    tolerance_bias = 0  # Stocke le surplus d'échecs
    extra_tolerance_used = 0  # Compteur d'utilisation du joker
    active_tolerance = tolerance  # Variable pour stocker la tolérance active
    ln2 = 0.69314  # Facteur de réduction pour les itérations et mutations

    quantum_state = QuantumState([decimal_number])  # Intégration de QuantumState
    quantum_state.measure()
    measured_state = quantum_state.state
    quantum_state = QuantumState(range(len(hex_number)))  # Possibles positions de mutation
    for i in range(max_mutations):
        mutated_hex = list(hex_number.upper())
        mutation_index = (random.randint(0, len(mutated_hex) - 1) + quantum_state.measure()) % len(mutated_hex)

        # Déterminer l'ensemble des chiffres valides pour la mutation
        if mutation_index == 0:
            valid_hex_digits = "0123456789ABCDEF"  # Exclure 0 pour éviter de réduire la taille // Ne pas exclure 0 et considérer que c'est un phénomène naturel.
        else:
            valid_hex_digits = "0123456789ABCDEF"

        valid_hex_digits = valid_hex_digits.replace(mutated_hex[mutation_index], "")  # Éviter le même chiffre
        mutated_hex[mutation_index] = random.choice(valid_hex_digits)
        mutated_number = int("".join(mutated_hex), 16)

        # ✅ Mise à jour de hex_number pour que la prochaine itération parte de ce nombre muté
        hex_number = "".join(mutated_hex)

        if isprime(mutated_number):
            stable_mutations += 1
            best_mutant = mutated_number  # Stocker le mutant réussi
            consecutive_fails = 0  # Réinitialiser l'échec
            mutation_history.append((i + 1, stable_mutations))
            print(f"Mutation réussie à l'itération {i + 1}: {hex(mutated_number)}")
            print(f"🛠️ Tolérance : {active_tolerance}, 📉 Bias : {tolerance_bias}")

            if (extra_tolerance_used % 4) == 1:
                # Première activation du joker : tolérance réduite à 4168 - bias
                active_tolerance = 4168 - tolerance_bias
                print(f"⚠️ Tolérance ajustée : {active_tolerance}")
            elif (extra_tolerance_used % 4) == 3:
                # Deuxième activation du joker : réinitialisation complète
                active_tolerance *= active_tolerance/ln2
                tolerance_bias = 0
                print(f"✅ Réinitialisation complète de la tolérance.")
            else:
                active_tolerance = 2084
                print(f"✅ Réinitialisation complète de la tolérance.")

        else:
            consecutive_fails += 1
            if consecutive_fails > active_tolerance + tolerance_bias:  # Doit être STRICTEMENT supérieur
                tolerance_bias = consecutive_fails - active_tolerance
                print(f"⚠️ Mise à jour du tolerance_bias : {tolerance_bias}")  # Debug pour voir les changements
                if (extra_tolerance_used % 4) < 2:
                    # Activation du joker
                    tolerance_bias = consecutive_fails - active_tolerance  # Stocke l'excès
                    extra_tolerance_used += 1
                    print(f"⚠️ Mise à jour du tolerance_bias : {tolerance_bias}")
                    if extra_tolerance_used == 2 and tolerance_bias >= 2084:
                        print(f"⛔ Tolérance > 4168 : arrêt du processus.")
                    print(f"⚠️ Tolérance dépassée, activation du joker (tentative {extra_tolerance_used})")
                    active_tolerance = 4168  # Nouvelle tolérance étendue
                else:
                    # Troisième dépassement : multiplier la tolérance et ajuster i et max_mutations
                    active_tolerance *= 2
                    i = int(i * ln2)
                    max_mutations = int(max_mutations * ln2)
                    print(f"⛔ Troisième dépassement : tolérance multipliée ({active_tolerance}), itérations ajustées ({i}/{max_mutations}).")
                    if max_mutations == 0:
                        break

    return best_mutant if stable_mutations > 0 else None, stable_mutations, i + 1, mutation_history



if __name__ == "__main__":
    Phi1 = "BA6E0C754A8A1443C12EC702DEFDAF866FED5591FA44CB13E5DE0F3BE38E15B886561E49999EFB4F7B7671423C44C27A71C2D1FDF86392683A148810C6B654A1E4CD13BAB0C96947A7E1FF9A0E3980B9F1A9608B0F9A324DE5F7E29281F38AB62FB34311756489C3C018CFC933269ACE359D8BDA74B333FEBAB8977D8ECBCE85F84A04B3EFCE28165827BA157E6A20F17321008FF73EB0F3CA40FCECA6418B489B1E0ADEE4E9C6943B7AA43808138609A0AC2F17F4A44D5AB5DE5F3963B4FFD5D51C67BA9E3C461E796973BBE29228DE413910203005C64B4AD9678B5F61014BFD9B0F126916459AA81AF808E55DE6E8366FCC7D1A697EA70104A5B1524F16AA1C8364E7B"
    Phi2 = "BA6E0C754A8A1443C12EC702DEFDAF866FED5591FA44CB13E5DE0F3BE38E15B886561E49999EFB4F7B7671423C44C27A71C2D1FDF86392683A148810C6B654A1E4CD13BAB0C96947A7E1FF9A0E3980B9F1A9608B0F9A324DE5F7E29281F38AB62FB34311756489C3C018CFC933269ACE359D8BDA74B333FEBAB8977D8ECBCE85F84A74B3EFCE28165827BA157E6A20F17321008FF73EB0F3CA40FCECA6418B489B1E0ADEE4E9C6943B7AA43808138609A0AC2F17F4A44D5AB5DE5F3963B4FFD5D51C67BA9E3C461E796973BBE29228DE413910203005C64B4AD9678B5F61014BFD9B0F126916459AA81AF808E55DE6E8366FCC7D1A697EA70104A5B1524F16AA1C8364E7B"

    mutant_Phi1, stability_Phi1, iter_Phi1, history_Phi1 = mutate_number(Phi1)
    mutant_Phi2, stability_Phi2, iter_Phi2, history_Phi2 = mutate_number(Phi2)

    plt.figure(figsize=(10, 5))
    if history_Phi1 and len(history_Phi1) > 1:
        iterations, stability_values = zip(*history_Phi1)
        plt.plot(iterations, stability_values, label="Phi1 Stabilité", marker='o')
        if len(iterations) > 1:
            slope, intercept, _, _, _ = linregress(iterations, stability_values)
            plt.plot(iterations, np.array(iterations) * slope + intercept, 'r--', label="Phi1 Régression")

    if history_Phi2 and len(history_Phi2) > 1:
        iterations, stability_values = zip(*history_Phi2)
        plt.plot(iterations, stability_values, label="Phi2 Stabilité", marker='s')
        slope, intercept, _, _, _ = linregress(iterations, stability_values)
        plt.plot(iterations, np.array(iterations) * slope + intercept, 'b--', label="Phi2 Régression")

    plt.xlabel("Itérations")
    plt.ylabel("Nombre de mutations stables")
    plt.title("Évolution de la stabilité des mutations avec régression")
    plt.legend()
    plt.grid()
    plt.show()
