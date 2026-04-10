import requests
import time
from src.models import globals as g

SIMULATION_MODE = True

URL_STOCKS          = "https://api-smartlock.devinci.fr/v1/inventory"
URL_IDENTIFICATION  = "https://api-smartlock.devinci.fr/v1/auth"
URL_RELAIS_OUVERTURE= "https://api-smartlock.devinci.fr/v1/hardware/unlock"
URL_CAPTEUR_PORTE   = "https://api-smartlock.devinci.fr/v1/hardware/door-status"
URL_TRANSACTION     = "https://api-smartlock.devinci.fr/v1/transactions"
URL_ALERTE_DISCORD  = "https://api-smartlock.devinci.fr/v1/notifications/discord"
URL_ALERTE_STOCK    = "https://api-smartlock.devinci.fr/v1/notifications/stock-error"


def recuperer_stocks_api():
    if SIMULATION_MODE:
        return {
            "PLA Rouge": 0,  "PLA Bleu": 19, "PLA Vert": 4,   "PLA Jaune": 10, "PLA Orange": 60, "PLA Gris": 60,
            "PETG Rouge": 12,"PETG Bleu": 8, "PETG Vert": 0,  "PETG Jaune": 10,"PETG Orange": 10,"PETG Gris": 10,
            "ASA Rouge": 10, "ASA Bleu": 10, "ASA Vert": 10,  "ASA Jaune": 10, "ASA Orange": 10, "ASA Gris": 10,
            "driver": 5, "moteur": 3, "Item 1": 10, "Item 2": 10, "Item 3": 0
        }
    try:
        reponse = requests.get(URL_STOCKS, timeout=5)
        return reponse.json() if reponse.status_code == 200 else {}
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


def lire_badge_nfc():
    if SIMULATION_MODE:
        print("🛠 [SIMU] Lecture NFC simulée — UID : 12345")
        return "12345"
    try:
        import board
        import busio
        from adafruit_pn532.i2c import PN532_I2C
        i2c = busio.I2C(board.SCL, board.SDA)
        pn532 = PN532_I2C(i2c)
        pn532.SAM_configuration()
        print("En attente d'un badge NFC...")
        while True:
            uid = pn532.read_passive_target(timeout=0.5)
            if uid is not None:
                uid_str = "".join([format(b, "02X") for b in uid])
                print(f"Badge détecté : {uid_str}")
                return uid_str
            time.sleep(0.1)
    except Exception as e:
        print(f"Erreur lecteur NFC : {e}")
        return None


def identifier_utilisateur(uid_badge):
    if SIMULATION_MODE:
        time.sleep(0.5)
        if uid_badge == "12345":
            g.utilisateur_actuel = "Guilhem"
            return True
        return False
    try:
        reponse = requests.post(URL_IDENTIFICATION, json={"uid": uid_badge}, timeout=3)
        if reponse.status_code == 200:
            g.utilisateur_actuel = reponse.json().get("prenom", "Utilisateur")
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
        payload = {"utilisateur": g.utilisateur_actuel, "articles": panier}
        reponse = requests.post(URL_TRANSACTION, json=payload, timeout=5)
        return reponse.status_code == 201
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")
        return False


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
    if SIMULATION_MODE:
        return False
    try:
        reponse = requests.get(URL_CAPTEUR_PORTE, timeout=2)
        return reponse.json().get("closed", False)
    except:
        return False


def envoyer_alerte_discord(motif="Armoire non refermée à temps"):
    if SIMULATION_MODE:
        print(f"🛠 [SIMU] Alerte Discord envoyée : '{motif}' — utilisateur : {g.utilisateur_actuel}")
        return True
    try:
        payload = {"utilisateur": g.utilisateur_actuel, "motif": motif}
        reponse = requests.post(URL_ALERTE_DISCORD, json=payload, timeout=5)
        return reponse.status_code == 200
    except Exception as e:
        print(f"Erreur envoi alerte Discord : {e}")
        return False


def signaler_erreur_stock(nom_item):
    if SIMULATION_MODE:
        print(f"🛠 [SIMU] Erreur stock signalée pour : '{nom_item}' — utilisateur : {g.utilisateur_actuel}")
        return True
    try:
        payload = {"utilisateur": g.utilisateur_actuel, "article": nom_item}
        reponse = requests.post(URL_ALERTE_STOCK, json=payload, timeout=5)
        return reponse.status_code == 200
    except Exception as e:
        print(f"Erreur signalement stock : {e}")
        return False