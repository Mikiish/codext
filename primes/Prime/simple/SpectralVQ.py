import random, threading, time, os, sympy
import numpy as np
import matplotlib.pyplot as plt
import PrimeMutationFilter as pmf
import primes.Prime.simple.spectral as spectral
import newgptint
import tempfile
from scipy.stats import linregress
from sympy.physics.quantum.qexpr import QuantumError

global mutate_number, quantum_state
quantum_lock = threading.Lock()  # 🔒 Création d'un verrou global
plot_lock = threading.Lock()  # 🔒 Verrou pour empêcher les conflits graphiques
iteration_counter = 0  # Compteur global pour le graphique
history_primary = []  # Stocke les mutations du premier nombre
history_secondary = []  # Stocke les mutations du deuxième nombre
plt.figure(figsize=(10, 5))  # Initialisation du graphique global
nombre_incroyable = float(np.e)
nombre_banale = 61681 ** nombre_incroyable
NOMBRE = 61681

# 📌 Stockage des 500 premiers nombres premiers
global prime_list
prime_list = list(sympy.primerange(5, 5000))[:500]  # Extraction des 500 premiers

class QuantumLisa:
    def __init__(self, possible_states=None, hidden_variable=None):
        """
        Initialise un état quantique adversarial.
        """
        if hidden_variable is not None:
            self.possible_states = pmf.GetPrimeMutationNaif(hidden_variable)
            if not self.possible_states:
                self.possible_states = possible_states if possible_states is not None else []
        else:
            self.possible_states = possible_states if possible_states is not None else []

        self.bits = 2084
        self.state = None  # Indéterminé tant qu’aucune mesure
        self.hidden_variable = hidden_variable \
            if hidden_variable is not None \
            else (int.from_bytes(os.urandom(self.bits // 8), "big"))
        self.hidden_variable |= (1 << (self.bits - 1))

        if not possible_states:
            self.possible_states = pmf.GetPrimeMutationNaif(self.hidden_variable)

        self.measured = False

    def measure(self):
        """Simule l'effondrement en choisissant un état basé sur `hidden_variable`."""
        if not self.measured and self.possible_states:
            weight = [abs((self.hidden_variable % len(self.possible_states)) - i) for i in
                      range(len(self.possible_states))]
            self.state = self.possible_states[weight.index(min(weight))]  # Choix de l'état le plus proche
            self.measured = True
        return self.state

    def reset(self):
        """Remet l’état en superposition."""
        self.state = None
        self.measured = False


# 📌 Fonction pour générer un nouvel exposant spécial basé sur prime_list
def generate_special_exponent(iter_magique):
    """Crée un exposant basé sur la séquence des nombres premiers"""
    if iter_magique >= len(prime_list) - 1:
        iter_magique = 1  # Évite les dépassements de liste
    return np.e * (float(prime_list[iter_magique - 1] / prime_list[iter_magique]))

def adversarial_cycle(initial_prime, history_storage, color):
    """Boucle principale où QuantumLisa et mutate_number() alternent leurs exécutions."""
    global quantum_lisa
    global mutate_number
    global iteration_counter

    quantum_lisa = QuantumLisa([], initial_prime)  # Initialisation avec le premier donné
    while True:
        measured_prime = quantum_lisa.measure()
        if measured_prime is None:
            print("❌ Aucun état possible dans QuantumLisa, arrêt du processus.")
            break

        print(f"🔄 QuantumLisa mesuré: {hex(measured_prime)}")

        mutate_number = measured_prime
        hex_mutate_number = hex(mutate_number).upper()[2:]
        last_prime, stability, iterations, mutation_history = spectral.mutate_number(hex_mutate_number)

        if not last_prime:
            print("❌ Aucun nombre premier trouvé après mutation, arrêt du processus.")
            break

        print(f"✨ Nouveau nombre premier trouvé: {hex(last_prime)}")
        iteration_counter += len(mutation_history)
        history_storage.extend([(iteration_counter + i, stability) for i, stability in mutation_history])

        quantum_lisa = QuantumLisa([], last_prime)
        plot_mutation_history()
        threading.current_thread().result = last_prime  # Stocke le dernier nombre trouvé dans le thread
        return last_prime

# Constantes pour l'échelle fixe
MAX_ITERATIONS = 302000
MAX_MUTATIONS = 302
def plot_mutation_history():
    """Affiche le graphique en temps réel avec toutes les mutations trouvées, en évitant les conflits multi-thread."""
    with plot_lock:  # 🔒 Empêche plusieurs threads d'accéder au graphique en même temps
        plt.clf()  # Nettoyage du graphe

        if history_primary:
            iterations_primary, stability_values_primary = zip(*history_primary)
            plt.scatter(iterations_primary, stability_values_primary, c='black', s=5, alpha=0.5,
                        label="Mutations (Primary)")  # Petits points noirs transparents
            plt.plot(iterations_primary, stability_values_primary, 'r-', alpha=0.5,
                     label="Primary Prime")  # Ligne rouge transparente

        if history_secondary:
            iterations_secondary, stability_values_secondary = zip(*history_secondary)
            plt.scatter(iterations_secondary, stability_values_secondary, c='black', s=5, alpha=0.5,
                        label="Mutations (Secondary)")  # Petits points noirs transparents
            plt.plot(iterations_secondary, stability_values_secondary, 'b-', alpha=0.5,
                     label="Secondary Prime")  # Ligne bleue transparente

        plt.xlabel("Itérations")
        plt.ylabel("Nombre de mutations stables")
        plt.title("Évolution de la stabilité des mutations")
        plt.legend()
        plt.grid()

        # 🔄 Fixer l'échelle des axes
        plt.xlim(0, MAX_ITERATIONS)
        plt.ylim(0, MAX_MUTATIONS)
        plt.pause(0.01)  # 🔄 Met à jour l'affichage proprement


if __name__ == "__main__":
    nombre = NOMBRE
    print(os.getcwd())  # Affiche le répertoire de travail
    print(tempfile.gettempdir())
    initial_prime = int(
        "D9602D2BEBA420D487118330693591E9ADA26EB469954963D4F3099738702158443C29FFD0292C5FC4B1EFCB700A8D9A7E2C6619A76022B587AC64652412903B9FDA1AD8253055D68FFA2BD5B7EFDB61D6D821699EC647CEB2CFE7900B49FA30F94B865C41532A507E32EFDE10345F459A22BB614C18F1C723B0E8A833B8A422D9EF044A947B27E238F364CE4F6C08BA811A506B05CA103A6C1E86FD1CCCF4129D529E227814315030611AE3BBFB3192DA9044F7777DF4D0158873F9E0929C41D4206404DD14E9B5960E33E842BA6A067EA6D1FB35349FC0C3D75F5780A0145A614295A5464079A3DA20D25F1060D25AFB17C4B689C6557DECE3FA9DC060E301ADE043E5F",
        16)
    secondary_prime = int(
        "D9602D2BEBA420D487118330693591E9ADA26EB469954963D4F3099738702158443C29FFD0292C5FC4B1EFCB700A8D9A7E2C6619A76022B587AC64652412903B9FDA1AD8253055D68FFA2BD5B7EFDB61D6D821699EC647CEB2CFE7900B49FA30F94B865C41532A507E32EFDE10345F459A22BB614C18F1C723B0E8A833B8A422D9EF744A947B27E238F364CE4F6C08BA811A506B05CA103A6C1E86FD1CCCF4129D529E227814315030611AE3BBFB3192DA9044F7777DF4D0158873F9E0929C41D4206404DD14E9B5960E33E842BA6A067EA6D1FB35349FC0C3D75F5780A0145A614295A5464079A3DA20D25F1060D25AFB17C4B689C6557DECE3FA9DC060E301ADE043E5F",
        16)

    discovered_casinos = []  # Liste pour stocker les nouveaux nombres hybrides
    nombre_magique = 0
    iter_magique = 0
    while True:
        iter_magique += 1
        nombre_magique = 61681 ** generate_special_exponent(iter_magique)
        thread1 = threading.Thread(target=adversarial_cycle, args=(initial_prime, history_primary, 'r'))
        thread2 = threading.Thread(target=adversarial_cycle, args=(secondary_prime, history_secondary, 'b'))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        print("✅ Les deux threads ont terminé un cycle.")
        initial_prime = thread1.result if hasattr(thread1, 'result') else initial_prime
        secondary_prime = thread2.result if hasattr(thread2, 'result') else secondary_prime

        # 📌 Rechercher un petit nombre avec un cycle court
        print("🔎 Recherche d'un nombre premier avec un cycle court...")
        range_min = int(61681 ** (np.e/2) + (initial_prime % 61681))
        range_max = int(nombre_magique + (secondary_prime % 61681))

        # ✅ Toujours s'assurer que range_min < range_max
        range_min, range_max = min(range_min, range_max), max(range_min, range_max)
        # 📌 Exécuter la recherche en s'assurant que l'intervalle est valide
        if range_min < range_max:
            with quantum_lock:
                small_prime = newgptint.find_prime_cycles(61681, (61681 ** 2), max_n=131, max_attempts=42*(8 ** 6))

        if not small_prime.empty:
            # Trouver l'index du plus petit cycle (n)
            min_cycle_index = small_prime["n"].idxmin()
            selected_prime = int(small_prime.loc[min_cycle_index, "p"])  # Prendre le p associé au plus petit cycle
            print(f"✨ Petit nombre premier sélectionné: {hex(selected_prime)} (cycle: {small_prime.loc[min_cycle_index, 'n']})")
            nombre = selected_prime

        else:
            print(f"⚠️ Aucun petit nombre trouvé, utilisation de {hex(nombre)} par défaut.")

        # 🔄 Construire le nouveau nombre hybride
        new_prime_hex = f"{hex(initial_prime)[2:]}{hex(nombre)[2:]}{hex(secondary_prime)[2:]}"
        new_prime = int(new_prime_hex, 16)

        # ✅ Vérifier si c'est un nombre premier
        if sympy.isprime(new_prime):
            print(f"🚀 Nouveau GIGA CASINO trouvé : {hex(new_prime)}")
            discovered_casinos.append(new_prime)
            print(f"List of created creeps :\n")
            for i, casino in enumerate(discovered_casinos):
                print(f"Casino n°{i + 1}: {hex(casino)}")
            break
        else:
            discovered_casinos.append(new_prime)
            print("⚠️ Le nombre construit n'est pas premier, mais il est conservé pour analyse.")

        print(f"End Prime initial : {hex(initial_prime)}\nEnd Prime secondary : {hex(secondary_prime)}\nPrime create : {hex(new_prime)}")
        # 🔄 Retourner dans la boucle avec les nombres principaux mis à jour
