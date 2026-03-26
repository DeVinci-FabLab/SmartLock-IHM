import requests
import time
from src.models import globals as g

# --- CONFIGURATION ---
SIMULATION_MODE = True  # <--- Change à False quand le serveur est ON

URL_STOCKS = "https://api-smartlock.devinci.fr/v1/inventory"
URL_IDENTIFICATION = "https://api-smartlock.devinci.fr/v1/auth"
URL_RELAIS_OUVERTURE = "https://api-smartlock.devinci.fr/v1/hardware/unlock"
URL_CAPTEUR_PORTE = "https://api-smartlock.devinci.fr/v1/hardware/door-status"
URL_TRANSACTION = "https://api-smartlock.devinci.fr/v1/transactions"

# --- LOGIQUE API ---

def recuperer_stocks_api():
    if SIMULATION_MODE:
        return {
            "PLA Rouge": 13, "PLA Bleu": 19, "PLA Vert": 4, "PLA Jaune": 10, "PLA Orange": 60, "PLA Gris": 60,
            "PETG Rouge": 12, "PETG Bleu": 8, "PETG Vert": 3, "PETG Jaune": 10, "PETG Orange": 10, "PETG Gris": 10,
            "ASA Rouge": 10, "ASA Bleu": 10, "ASA Vert": 10, "ASA Jaune": 10, "ASA Orange": 10, "ASA Gris": 10,
            "driver": 5, "moteur": 3, "Item 1": 10, "Item 2": 10, "Item 3": 15
        }

    try:
        reponse = requests.get(URL_STOCKS, timeout=5)
        return reponse.json() if reponse.status_code == 200 else None
    except Exception as e:
        print(f"Erreur API Stocks : {e}")
        return {}

def initialiser_stocks():
    stocks = recuperer_stocks_api()
    if stocks:
        g.stocks.update(stocks)
        mode = "Simulation" if SIMULATION_MODE else "Réel"
        print(f"✅ Inventaire initialisé (Mode {mode})")
    else:
        print("⚠️ Échec récup stocks, conservation des valeurs par défaut.")

def identifier_utilisateur(uid_badge):
    if SIMULATION_MODE:
        time.sleep(0.5)
        if uid_badge == "12345":
            g.utilisateur_actuel = "Guilhem"
            return True
        return False

    try:
        donnees = {"uid": uid_badge}
        reponse = requests.post(URL_IDENTIFICATION, json=donnees, timeout=3)
        if reponse.status_code == 200:
            infos_user = reponse.json()
            g.utilisateur_actuel = infos_user.get("prenom", "Utilisateur")
            return True
        return False
    except Exception as e:
        print(f"Erreur d'identification : {e}")
        return False

def enregistrer_transaction(panier):
    if SIMULATION_MODE:
        print(f"🛠 [SIMU] Envoi transaction pour {g.utilisateur_actuel}...")
        for item, qte in panier.items():
            if item in g.stocks:
                g.stocks[item] -= qte
                print(f"   -> Débit de {qte} sur {item}")
        return True

    try:
        payload = {
            "utilisateur": g.utilisateur_actuel,
            "articles": panier
        }
        reponse = requests.post(URL_TRANSACTION, json=payload, timeout=5)
        return reponse.status_code == 201
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")
        return False

# --- HARDWARE ---

def commander_ouverture_relais():
    if SIMULATION_MODE:
        print("🛠 [SIMU] Relais activé : CLIC ! (Porte déverrouillée)")
        return True

    try:
        reponse = requests.post(URL_RELAIS_OUVERTURE, timeout=3)
        return reponse.status_code == 200
    except Exception:
        return False
    
def verifier_etat_porte():
    """Simule le capteur de porte (True = Fermée, False = Ouverte)"""
    if SIMULATION_MODE:
        return False 
    try:
        reponse = requests.get(URL_CAPTEUR_PORTE, timeout=2)
        return reponse.json().get("closed", False)
    except:
        return False