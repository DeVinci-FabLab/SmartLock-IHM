# SmartLock-IHM

Interface homme-machine (kiosque tactile) pour l'armoire connectée DeVinci FabLab.  
Déployée sur Raspberry Pi avec écran tactile en orientation portrait (600×1024).

---

## Stack

- Python 3.13 + CustomTkinter 5.2.2
- Lecteur NFC PN532 (I2C)
- Solénoïde sur GPIO 26 (BCM) — temps d'ouverture : 5 secondes
- Capteur Hall sur GPIO 27 (BCM) *(optionnel, non branché actuellement)*
- Backend : [SmartLock-Authentication-Authorization](https://github.com/DeVinci-FabLab/SmartLock-Authentication-Authorization)

---

## Architecture

```
main.py                        — point d'entrée, monkey-patch CTkButton (Python 3.13)
src/
  logic/
    api_service.py             — tous les appels API + GPIO (Keycloak, stocks, relais, NFC)
    inventory_logic.py         — gestion panier et état boutons
    logger.py                  — logger centralisé → ~/smartlock.log
    timer_manager.py           — timer d'inactivité
  models/
    globals.py                 — état global partagé entre les vues
  views/
    home_view.py               — écran d'accueil + scan NFC (thread séparé)
    navigation_view.py         — catalogue par catégories (chargé depuis l'API)
    ecran_selection.py         — détail article + sélecteur de quantité
    vue_panier.py              — récapitulatif du panier
    validation_finale.py       — confirmation avant ouverture
    acces_physique.py          — écran "armoire ouverte" + activation solénoïde
    ecran_cloture.py           — retour d'expérience post-session
```

---

## Fonctionnement

1. **Accueil** — l'utilisateur scanne son badge NFC
2. **Authentification** — l'IHM appelle `POST /auth/locker/{id}/check` via Keycloak
3. **Navigation** — les catégories et articles sont chargés dynamiquement depuis `GET /categories/` + `GET /items/` + `GET /lockers/{id}/stock`
4. **Sélection** — l'utilisateur ajoute des articles au panier (borné par le stock réel)
5. **Validation** — `PUT /stock/{id}` met à jour chaque entrée stock
6. **Ouverture** — le solénoïde s'active 5 secondes via GPIO 26
7. **Clôture** — retour d'expérience, puis retour à l'accueil

### Indicateurs de stock

| Couleur bouton | Signification |
|----------------|--------------|
| Gris (normal) | Stock suffisant |
| Orange "(Stock bas)" | `0 < stock < low_stock_threshold` |
| Gris désactivé "(Vide)" | `stock == 0` |
| Vert | Article déjà dans le panier |

### Comportement kiosk

- Inactivité sur l'accueil (2 min) → reste sur l'accueil
- Inactivité sur la navigation → retour accueil
- Inactivité sur l'écran de clôture (90s) → retour accueil
- Crash de l'app → relance automatique (boucle dans `.xinitrc`)

---

## Installation sur Raspberry Pi

### 1. Flasher la carte SD

Utiliser **Raspberry Pi Imager** avec **Raspberry Pi OS Lite (64-bit)**.

Dans « Modifier les réglages » avant de graver :

| Paramètre | Valeur |
|-----------|--------|
| Hostname | `smartlock1` |
| Utilisateur | `locker` |
| Mot de passe | *(choisir)* |
| WiFi SSID | *(réseau)* |
| WiFi password | *(mot de passe réseau)* |
| SSH | Activé — auth par mot de passe |
| Timezone | `Europe/Paris` |
| Clavier | `fr` |

### 2. Premier démarrage

Insérer la SD dans le RPi, alimenter, attendre ~2 minutes.

Trouver l'IP du RPi :
```bash
arp -a
# chercher MAC b8:27:eb:* ou dc:a6:32:*
```

Se connecter :
```bash
ssh locker@<IP_DU_RPI>
```

### 3. Installer les dépendances système

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y xorg python3-pip python3-venv python3-tk xinput i2c-tools
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_boot_behaviour B2
sudo reboot
```

### 4. Transférer le projet

Depuis **Windows** (PowerShell) :

```powershell
scp -r "C:\chemin\vers\SmartLock-IHM\src" "C:\chemin\vers\SmartLock-IHM\main.py" "C:\chemin\vers\SmartLock-IHM\requirements.txt" "C:\chemin\vers\SmartLock-IHM\.env.example" locker@<IP_DU_RPI>:/home/locker/SmartLock-IHM/
```

### 5. Installer les dépendances Python

```bash
cd ~/SmartLock-IHM
python3 -m venv venv
source venv/bin/activate
pip install customtkinter==5.2.2 darkdetect==0.8.0 packaging python-dotenv requests pillow
pip install RPi.GPIO adafruit-blinka adafruit-circuitpython-pn532
```

### 6. Configurer l'environnement

```bash
cp .env.example .env
nano .env
```

```env
SIMULATION_MODE=False
API_URL=https://api.smartlock.devinci-fablab.fr
KEYCLOAK_URL=https://auth.devinci-fablab.fr
KEYCLOAK_REALM=dev
LOCKER_CLIENT_SECRET=<secret du client smartlock-lockers dans Keycloak>
LOCKER_ID=1
```

### 7. Désactiver la veille WiFi

Évite la coupure SSH et l'arrêt du lecteur NFC après inactivité :

```bash
sudo bash -c 'cat > /etc/NetworkManager/conf.d/wifi-powersave-off.conf << EOF
[connection]
wifi.powersave = 2
EOF'
sudo systemctl restart NetworkManager
```

> La commande coupe brièvement le WiFi — SSH se déconnecte, c'est normal. Reconnecte-toi et continue.

### 8. Configurer le démarrage automatique

```bash
cat > ~/.xinitrc << 'EOF'
xset s off
xset -dpms
xset s noblank
OUTPUT=$(xrandr | grep " connected" | head -1 | awk '{print $1}')
xrandr --output $OUTPUT --rotate right
TOUCH_ID=$(xinput list | grep -i "QDTECH\|MPI7002" | grep -o 'id=[0-9]*' | grep -o '[0-9]*')
[ -n "$TOUCH_ID" ] && xinput set-prop $TOUCH_ID "Coordinate Transformation Matrix" 0 1 0 -1 0 1 0 0 1
while true; do
    cd /home/locker/SmartLock-IHM
    PYTHONUNBUFFERED=1 /home/locker/SmartLock-IHM/venv/bin/python3 main.py >> /home/locker/smartlock.log 2>&1
    tail -c 5M /home/locker/smartlock.log > /tmp/smartlock_tmp && mv /tmp/smartlock_tmp /home/locker/smartlock.log
    sleep 5
done
EOF

echo '[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && startx' >> ~/.bash_profile
```

### 9. Redémarrer

```bash
sudo reboot
```

L'interface se lance automatiquement au boot.

---

## Câblage matériel

### Lecteur NFC PN532 (I2C)

| PN532 | Raspberry Pi |
|-------|-------------|
| VCC   | 3.3V (pin 1) |
| GND   | GND (pin 6) |
| SDA   | GPIO 2 / SDA (pin 3) |
| SCL   | GPIO 3 / SCL (pin 5) |

Vérifier la détection : `sudo i2cdetect -y 1` → adresse `0x24`

### Solénoïde (via relais)

| Relais | Raspberry Pi |
|--------|-------------|
| IN     | GPIO 26 (pin 37) |
| VCC    | 5V (pin 2) |
| GND    | GND (pin 6) |

Durée d'activation : 5 secondes.

### Capteur Hall (optionnel — détection fermeture porte)

| Capteur Hall | Raspberry Pi |
|-------------|-------------|
| VCC  | 3.3V (pin 1) |
| GND  | GND (pin 6) |
| OUT  | GPIO 27 (pin 13) |

Logique : aimant présent (porte fermée) → signal LOW. Actuellement non branché — la session se ferme via un timer de 5 secondes.

---

## Déploiement des mises à jour

```powershell
scp -r "C:\chemin\vers\SmartLock-IHM\src" "C:\chemin\vers\SmartLock-IHM\main.py" locker@<IP_DU_RPI>:/home/locker/SmartLock-IHM/
ssh locker@<IP_DU_RPI> "sudo reboot"
```

---

## Logs

```bash
tail -f ~/smartlock.log
```

Exemple de session complète :
```
2026-06-03 13:01:52 [INFO] Renouvellement token Keycloak (smartlock-lockers)
2026-06-03 13:01:53 [INFO] Token Keycloak obtenu (smartlock-lockers)
2026-06-03 13:01:54 [INFO] Stocks chargés : 4 articles / 2 catégories
2026-06-03 13:01:56 [INFO] En attente d'un badge NFC...
2026-06-03 13:01:57 [INFO] Badge detecte : XX:XX:XX:XX
2026-06-03 13:01:57 [INFO] Accès autorisé : Utilisateur (UID: XX:XX:XX:XX)
2026-06-03 13:02:02 [INFO] Panier mis a jour : ESP32 DevKit x2
2026-06-03 13:02:08 [INFO] Transaction : Utilisateur — {'ESP32 DevKit': 2}
2026-06-03 13:02:08 [INFO] Débit 2x ESP32 DevKit → stock restant : 4
2026-06-03 13:02:13 [INFO] Relais activé (GPIO)
2026-06-03 13:02:20 [INFO] Clôture session : Utilisateur — motif : parfait
```

---

## Dépendances Keycloak

Le client `smartlock-lockers` doit avoir le rôle **`materialiste`** dans ses *Service account roles* pour pouvoir mettre à jour les stocks (`PUT /stock/{id}`).

---

## Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `SIMULATION_MODE` | `True` = badge/stocks simulés, GPIO réel | `True` |
| `API_URL` | URL du backend | `https://api.smartlock.devinci-fablab.fr` |
| `KEYCLOAK_URL` | URL Keycloak | `https://auth.devinci-fablab.fr` |
| `KEYCLOAK_REALM` | Realm Keycloak | `dev` |
| `LOCKER_CLIENT_SECRET` | Secret du client `smartlock-lockers` | — |
| `LOCKER_ID` | ID de l'armoire dans la base | `1` |
