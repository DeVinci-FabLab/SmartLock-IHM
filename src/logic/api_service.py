import requests
from src.models import globals as g
###

URL_STOCKS = "https://api-smartlock.devinci.fr/v1/inventory"
URL_DISCORD = "https://discord.com/api/webhooks/votre_code_unique"
URL_IDENTIFICATION = "https://api-smartlock.devinci.fr/v1/auth"
URL_RELAIS_OUVERTURE = "https://api-smartlock.devinci.fr/v1/hardware/unlock"
URL_CAPTEUR_PORTE = "https://api-smartlock.devinci.fr/v1/hardware/door-status"

def recuperer_stocks_api():
    try:
        reponse = requests.get(URL_STOCKS, timeout=5)
        if reponse.status_code == 200:
            stocks = reponse.json()
            return stocks
        else:
            print(f"Erreur serveur : {reponse.status_code}")
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération des stocks : {e}")
        return {}

def initialiser_stocks():
    stocks = recuperer_stocks_api()
    if stocks:
        g.stocks.update(stocks) #c une fonction du dico
        print("Mise à jour globale effectuée !")
    else:
        print("Le serveur n'a rien renvoyé, on garde les valeurs par défaut.")

def mise_a_jour_stock_validation(panier):
    try:
        reponse = requests.post(URL_STOCKS, json=panier, timeout=5)
        if reponse.status_code in [200, 201]:
            print("Inventaire mis à jour côté serveur.")
            return True
        return False
    except Exception as e:
        print(f"Erreur lors de la validation : {e}")
        return False
    
def identifier_utilisateur(uid_badge):
    try:
        donnees = {"uid":uid_badge}
        reponse = requests.post(URL_IDENTIFICATION, json=donnees, timeout=3)

        if reponse.status_code == 200:
            infos_user = reponse.json()
            g.utilisateur_actuel = infos_user.get("prenom", "Utilisateur")
            return True
        else:
            print(f"Badge inconnu : {reponse.status_code}")
            return False
    except Exception as e:
        print(f"Erreur d'identification : {e}")
        return False
    
# --- HARDWARE ---

def commander_ouverture_relais():
    """Envoie l'ordre au Back-end d'activer le relais physique du verrou"""
    try:
        reponse = requests.post(URL_RELAIS_OUVERTURE, timeout=3)
        if reponse.status_code == 200:
            print("Signal d'ouverture envoyé au verrou.")
            return True
        else:
            print(f"Échec de l'ouverture : {reponse.status_code}")
            return False
    except Exception as e:
        print(f"Erreur matérielle (Relais) : {e}")
        return False

def verifier_etat_porte():
    try:
        reponse = requests.get(URL_CAPTEUR_PORTE, timeout=2)
        if reponse.status_code == 200:
            etat = reponse.json() # On attend un truc du genre {"is_closed": true}
            return etat.get("is_closed", False)
        return False
    except Exception as e:
        print(f"Erreur capteur porte : {e}")
        return False