import os
import time

import requests
from dotenv import load_dotenv

from src.models import globals as g
from src.logic.logger import logger

load_dotenv()

SIMULATION_MODE      = os.getenv("SIMULATION_MODE", "True").lower() in ("true", "1", "yes")
API_URL              = os.getenv("API_URL", "https://api.smartlock.devinci-fablab.fr")
KEYCLOAK_URL         = os.getenv("KEYCLOAK_URL", "https://auth.devinci-fablab.fr")
KEYCLOAK_REALM       = os.getenv("KEYCLOAK_REALM", "dev")
LOCKER_CLIENT_SECRET = os.getenv("LOCKER_CLIENT_SECRET", "")
LOCKER_ID            = int(os.getenv("LOCKER_ID", "1"))


class TokenManager:
    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._token = None
        self._expiry = 0.0

    def get_token(self) -> str:
        if self._token and time.time() < self._expiry - 30:
            return self._token
        logger.info(f"Renouvellement token Keycloak ({self._client_id})")
        token_url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
        try:
            resp = requests.post(token_url, data={
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            }, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            self._token = data["access_token"]
            self._expiry = time.time() + data.get("expires_in", 300)
            logger.info(f"Token Keycloak obtenu ({self._client_id})")
            return self._token
        except Exception as e:
            logger.error(f"Erreur obtention token Keycloak ({self._client_id}) : {e}")
            return ""


_locker_token_manager = TokenManager("smartlock-lockers", LOCKER_CLIENT_SECRET)


def _headers() -> dict:
    return {"Authorization": f"Bearer {_locker_token_manager.get_token()}"}


def recuperer_stocks_api() -> dict:
    if SIMULATION_MODE:
        g.stock_ids = {
            "Arduino Uno R3": 101, "ESP32 DevKit": 102,
            "Filament PLA 1kg": 201, "Résine UV 500ml": 202,
        }
        g.categories_items = {
            "Électronique":  ["Arduino Uno R3", "ESP32 DevKit"],
            "Impression 3D": ["Filament PLA 1kg", "Résine UV 500ml"],
        }
        g.items_description = {
            "Arduino Uno R3":    "Carte microcontrôleur ATmega328P",
            "ESP32 DevKit":      "Module WiFi+BT pour IoT",
            "Filament PLA 1kg":  "Filament PLA 1.75mm blanc",
            "Résine UV 500ml":   "Résine photopolymère transparente",
        }
        g.items_threshold = {
            "Arduino Uno R3": 3, "ESP32 DevKit": 3,
            "Filament PLA 1kg": 5, "Résine UV 500ml": 2,
        }
        g.items_unit = {
            "Arduino Uno R3": "pce", "ESP32 DevKit": "pce",
            "Filament PLA 1kg": "kg", "Résine UV 500ml": "ml",
        }
        return {
            "Arduino Uno R3": 5, "ESP32 DevKit": 8,
            "Filament PLA 1kg": 10, "Résine UV 500ml": 0,
        }
    try:
        headers = _headers()

        # 1. Catégories
        cat_resp = requests.get(f"{API_URL}/categories/", headers=headers, timeout=5)
        cat_resp.raise_for_status()
        categories_map: dict[int, str] = {
            cat["id"]: cat["name"] for cat in cat_resp.json()
        }

        # 2. Tous les items (nom, description, category_id)
        items_resp = requests.get(f"{API_URL}/items/", headers=headers, timeout=5)
        items_resp.raise_for_status()
        items_data = items_resp.json()
        items_map: dict[int, dict] = {
            item["id"]: item for item in items_data
        }

        # 3. Stock du casier
        stock_resp = requests.get(
            f"{API_URL}/lockers/{LOCKER_ID}/stock", headers=headers, timeout=5
        )
        stock_resp.raise_for_status()
        stock_entries = stock_resp.json()

        stocks: dict[str, int] = {}
        stock_ids: dict[str, int] = {}
        categories_items: dict[str, list] = {}
        items_description: dict[str, str] = {}
        items_threshold: dict[str, int | None] = {}
        items_unit: dict[str, str] = {}

        for entry in stock_entries:
            item_id = entry.get("item_id")
            item = items_map.get(item_id, {})
            item_name = item.get("name", f"Item {item_id}")
            category_name = categories_map.get(item.get("category_id"), "Autre")

            stocks[item_name] = entry.get("quantity", 0)
            stock_ids[item_name] = entry["id"]
            items_description[item_name] = item.get("description") or ""
            items_threshold[item_name] = item.get("low_stock_threshold")
            items_unit[item_name] = entry.get("unit_measure") or "pce"
            categories_items.setdefault(category_name, [])
            if item_name not in categories_items[category_name]:
                categories_items[category_name].append(item_name)

        g.stock_ids = stock_ids
        g.categories_items = categories_items
        g.items_description = items_description
        g.items_threshold = items_threshold
        g.items_unit = items_unit
        logger.info(f"Stocks chargés : {len(stocks)} articles / {len(categories_items)} catégories")
        return stocks

    except Exception as e:
        logger.error(f"Erreur récupération stocks : {e}")
        return {}


def initialiser_stocks():
    stocks = recuperer_stocks_api()
    if stocks:
        g.stocks.update(stocks)
        mode = "Simulation" if SIMULATION_MODE else "Réel"
        logger.info(f"Inventaire initialisé (Mode {mode})")
    else:
        logger.warning("Échec récupération stocks, conservation des valeurs par défaut.")


def lire_badge_nfc() -> str | None:
    if SIMULATION_MODE:
        logger.info("[SIMU] Lecture NFC simulee - UID : 12345")
        return "12345"
    try:
        import board
        import busio
        from adafruit_pn532.i2c import PN532_I2C
        i2c = busio.I2C(board.SCL, board.SDA)
        pn532 = PN532_I2C(i2c)
        pn532.SAM_configuration()
        logger.info("En attente d'un badge NFC...")
        while True:
            uid = pn532.read_passive_target(timeout=0.5)
            if uid is not None:
                uid_str = ":".join([format(b, "02X") for b in uid])
                logger.info(f"Badge detecte : {uid_str}")
                return uid_str
            time.sleep(0.1)
    except Exception as e:
        logger.error(f"Erreur lecteur NFC : {e}")
        return None



def identifier_utilisateur(uid_badge: str) -> bool:
    if SIMULATION_MODE:
        time.sleep(0.5)
        if uid_badge == "12345":
            g.utilisateur_actuel = "Guilhem"
            g.derniere_raison_acces = None
            logger.info(f"[SIMU] Accès autorisé pour Guilhem (UID: {uid_badge})")
            return True
        g.derniere_raison_acces = "no_permission"
        logger.warning(f"[SIMU] Accès refusé — UID inconnu : {uid_badge}")
        return False
    try:
        resp = requests.post(
            f"{API_URL}/auth/locker/{LOCKER_ID}/check",
            headers=_headers(),
            json={"card_id": uid_badge},
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()

        if data.get("allowed"):
            g.utilisateur_actuel = data.get("display_name", "Utilisateur")
            g.derniere_raison_acces = None
            logger.info(f"Accès autorisé : {g.utilisateur_actuel} (UID: {uid_badge})")
            return True

        reason = data.get("reason", "inconnu")
        g.derniere_raison_acces = reason
        logger.warning(f"Accès refusé — raison : {reason} (UID: {uid_badge})")
        return False

    except Exception as e:
        logger.error(f"Erreur identification badge : {e}")
        g.derniere_raison_acces = None
        return False


def enregistrer_transaction(panier: dict) -> bool:
    if SIMULATION_MODE:
        logger.info(f"[SIMU] Envoi transaction pour {g.utilisateur_actuel}...")
        for item, qte in panier.items():
            if item in g.stocks:
                g.stocks[item] -= qte
                logger.info(f"[SIMU] Debit de {qte} sur {item}")
        return True
    try:
        headers = _headers()
        success = True

        logger.info(f"Transaction : {g.utilisateur_actuel} — {panier}")
        for nom_item, qte_prise in panier.items():
            stock_entry_id = g.stock_ids.get(nom_item)
            if stock_entry_id is None:
                logger.warning(f"ID stock introuvable pour '{nom_item}' — ignoré.")
                success = False
                continue

            nouveau_stock = max(0, g.stocks.get(nom_item, 0) - qte_prise)
            put_resp = requests.put(
                f"{API_URL}/stock/{stock_entry_id}",
                headers=headers,
                json={"quantity": nouveau_stock},
                timeout=5,
            )
            if put_resp.ok:
                g.stocks[nom_item] = nouveau_stock
                logger.info(f"Débit {qte_prise}x {nom_item} → stock restant : {nouveau_stock}")
            else:
                logger.error(f"Échec mise à jour stock {nom_item} : {put_resp.status_code}")
                success = False

        return success

    except Exception as e:
        logger.error(f"Erreur enregistrement transaction : {e}")
        return False


def commander_ouverture_relais() -> bool:
    try:
        import RPi.GPIO as GPIO
        SOLENOID_PIN = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SOLENOID_PIN, GPIO.OUT)
        GPIO.output(SOLENOID_PIN, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(SOLENOID_PIN, GPIO.LOW)
        logger.info("Relais activé (GPIO)")
        return True
    except Exception as e:
        logger.warning(f"Relais GPIO indisponible : {e}")
        return True  # ne bloque pas le flux si GPIO absent


def verifier_etat_porte() -> bool:
    return False  # capteur Hall non branché — fermeture via timer ou bouton


def envoyer_alerte_discord(motif: str = "Armoire non refermée à temps") -> bool:
    # TODO: endpoint /notifications/discord non implémenté côté backend
    if SIMULATION_MODE:
        logger.info(f"[SIMU] Alerte Discord : '{motif}' — utilisateur : {g.utilisateur_actuel}")
        return True
    try:
        resp = requests.post(
            f"{API_URL}/notifications/discord",
            headers=_headers(),
            json={"utilisateur": g.utilisateur_actuel, "motif": motif},
            timeout=5,
        )
        return resp.ok
    except Exception as e:
        logger.error(f"Erreur alerte Discord : {e}")
        return False


def signaler_erreur_stock(nom_item: str) -> bool:
    # TODO: endpoint /notifications/stock-error non implémenté côté backend
    if SIMULATION_MODE:
        logger.info(f"[SIMU] Erreur stock signalee pour : '{nom_item}' — utilisateur : {g.utilisateur_actuel}")
        return True
    try:
        resp = requests.post(
            f"{API_URL}/notifications/stock-error",
            headers=_headers(),
            json={"utilisateur": g.utilisateur_actuel, "article": nom_item},
            timeout=5,
        )
        return resp.ok
    except Exception as e:
        logger.error(f"Erreur signalement stock : {e}")
        return False
