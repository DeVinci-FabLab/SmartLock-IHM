import time
import requests
from src.models import globals as g

SIMULATION_MODE = True

API_URL              = "https://api.smartlock.devinci-fablab.fr"
KEYCLOAK_URL         = "https://auth.devinci-fablab.fr"
KEYCLOAK_REALM       = "dev"
LOCKER_CLIENT_SECRET = "bXOpaWO6Z5y2auWEX4wwK0Fjsi7cQZgF"
LOCKER_ID            = 1


class TokenManager:
    def __init__(self):
        self._token = None
        self._expiry = 0.0

    def get_token(self) -> str:
        if self._token and time.time() < self._expiry - 30:
            return self._token
        print("🔑 Renouvellement token Keycloak...")
        token_url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
        try:
            resp = requests.post(token_url, data={
                "grant_type": "client_credentials",
                "client_id": "smartlock-lockers",
                "client_secret": LOCKER_CLIENT_SECRET,
            }, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            self._token = data["access_token"]
            self._expiry = time.time() + data.get("expires_in", 300)
            print("✅ Token Keycloak obtenu.")
            return self._token
        except Exception as e:
            print(f"❌ Erreur obtention token Keycloak : {e}")
            return ""


_token_manager = TokenManager()


def _headers() -> dict:
    return {"Authorization": f"Bearer {_token_manager.get_token()}"}


def recuperer_stocks_api() -> dict:
    if SIMULATION_MODE:
        return {
            "PLA Rouge": 0,  "PLA Bleu": 19, "PLA Vert": 4,   "PLA Jaune": 10, "PLA Orange": 60, "PLA Gris": 60,
            "PETG Rouge": 12,"PETG Bleu": 8, "PETG Vert": 0,  "PETG Jaune": 10,"PETG Orange": 10,"PETG Gris": 10,
            "ASA Rouge": 10, "ASA Bleu": 10, "ASA Vert": 10,  "ASA Jaune": 10, "ASA Orange": 10, "ASA Gris": 10,
            "driver": 5, "moteur": 3, "Item 1": 10, "Item 2": 10, "Item 3": 0
        }
    try:
        resp = requests.get(f"{API_URL}/lockers/{LOCKER_ID}/stock", headers=_headers(), timeout=5)
        resp.raise_for_status()
        stock_entries = resp.json()

        stocks = {}
        for entry in stock_entries:
            item_id = entry.get("item_id")
            quantity = entry.get("quantity", 0)
            try:
                item_resp = requests.get(f"{API_URL}/items/{item_id}", headers=_headers(), timeout=5)
                item_resp.raise_for_status()
                item_name = item_resp.json().get("name", f"Item {item_id}")
            except Exception:
                item_name = f"Item {item_id}"
            stocks[item_name] = quantity

        return stocks
    except Exception as e:
        print(f"❌ Erreur récupération stocks : {e}")
        return {}


def initialiser_stocks():
    stocks = recuperer_stocks_api()
    if stocks:
        g.stocks.update(stocks)
        mode = "Simulation" if SIMULATION_MODE else "Réel"
        print(f"✅ Inventaire initialisé (Mode {mode})")
    else:
        print("⚠️ Échec récup stocks, conservation des valeurs par défaut.")


def lire_badge_nfc() -> str | None:
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
                uid_str = ":".join([format(b, "02X") for b in uid])
                print(f"Badge détecté : {uid_str}")
                return uid_str
            time.sleep(0.1)
    except Exception as e:
        print(f"❌ Erreur lecteur NFC : {e}")
        return None


def identifier_utilisateur(uid_badge: str) -> bool:
    if SIMULATION_MODE:
        time.sleep(0.5)
        if uid_badge == "12345":
            g.utilisateur_actuel = "Guilhem"
            return True
        return False
    try:
        resp = requests.post(
            f"{API_URL}/auth/locker/{LOCKER_ID}/check",
            headers=_headers(),
            json={"card_id": uid_badge},
            timeout=5
        )
        resp.raise_for_status()
        data = resp.json()

        if data.get("allowed"):
            g.utilisateur_actuel = data.get("display_name", "Utilisateur")
            print(f"✅ Accès autorisé pour : {g.utilisateur_actuel}")
            return True
        else:
            reason = data.get("reason", "inconnu")
            print(f"⛔ Accès refusé — raison : {reason}")
            return False
    except Exception as e:
        print(f"❌ Erreur identification : {e}")
        return False


def enregistrer_transaction(panier: dict) -> bool:
    if SIMULATION_MODE:
        print(f"🛠 [SIMU] Envoi transaction pour {g.utilisateur_actuel}...")
        for item, qte in panier.items():
            if item in g.stocks:
                g.stocks[item] -= qte
                print(f"   -> Débit de {qte} sur {item}")
        return True
    try:
        headers = _headers()
        for nom_item, qte_prise in panier.items():
            resp = requests.get(
                f"{API_URL}/stock/",
                headers=headers,
                params={"locker_id": LOCKER_ID},
                timeout=5
            )
            resp.raise_for_status()
            all_stock = resp.json()

            stock_entry = None
            for entry in all_stock:
                item_resp = requests.get(f"{API_URL}/items/{entry['item_id']}", headers=headers, timeout=5)
                if item_resp.ok and item_resp.json().get("name") == nom_item:
                    stock_entry = entry
                    break

            if stock_entry is None:
                print(f"⚠️ Item '{nom_item}' introuvable dans le stock API.")
                continue

            nouveau_stock = max(0, stock_entry["quantity"] - qte_prise)
            put_resp = requests.put(
                f"{API_URL}/stock/{stock_entry['id']}",
                headers=headers,
                json={"quantity": nouveau_stock},
                timeout=5
            )
            if put_resp.ok:
                g.stocks[nom_item] = nouveau_stock
                print(f"   -> Débit de {qte_prise} sur {nom_item} (nouveau stock : {nouveau_stock})")
            else:
                print(f"⚠️ Échec mise à jour stock pour {nom_item} : {put_resp.status_code}")

        return True
    except Exception as e:
        print(f"❌ Erreur enregistrement transaction : {e}")
        return False


def commander_ouverture_relais() -> bool:
    if SIMULATION_MODE:
        print("🛠 [SIMU] Relais activé : CLIC ! (Porte déverrouillée)")
        return True
    try:
        import RPi.GPIO as GPIO
        SOLENOID_PIN = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SOLENOID_PIN, GPIO.OUT)
        GPIO.output(SOLENOID_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(SOLENOID_PIN, GPIO.LOW)
        print("✅ Relais activé (GPIO)")
        return True
    except Exception as e:
        print(f"❌ Erreur relais GPIO : {e}")
        return False


def verifier_etat_porte() -> bool:
    if SIMULATION_MODE:
        return False
    try:
        import RPi.GPIO as GPIO
        DOOR_PIN = 27
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DOOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        closed = GPIO.input(DOOR_PIN) == GPIO.LOW
        return closed
    except Exception as e:
        print(f"❌ Erreur capteur porte GPIO : {e}")
        return False


def envoyer_alerte_discord(motif: str = "Armoire non refermée à temps") -> bool:
    if SIMULATION_MODE:
        print(f"🛠 [SIMU] Alerte Discord : '{motif}' — utilisateur : {g.utilisateur_actuel}")
        return True
    try:
        resp = requests.post(
            f"{API_URL}/notifications/discord",
            headers=_headers(),
            json={"utilisateur": g.utilisateur_actuel, "motif": motif},
            timeout=5
        )
        return resp.ok
    except Exception as e:
        print(f"❌ Erreur alerte Discord : {e}")
        return False


def signaler_erreur_stock(nom_item: str) -> bool:
    if SIMULATION_MODE:
        print(f"🛠 [SIMU] Erreur stock signalée pour : '{nom_item}' — utilisateur : {g.utilisateur_actuel}")
        return True
    try:
        resp = requests.post(
            f"{API_URL}/notifications/stock-error",
            headers=_headers(),
            json={"utilisateur": g.utilisateur_actuel, "article": nom_item},
            timeout=5
        )
        return resp.ok
    except Exception as e:
        print(f"❌ Erreur signalement stock : {e}")
        return False