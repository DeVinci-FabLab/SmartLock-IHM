# SmartLock-IHM

Interface homme-machine (kiosque tactile) pour l'armoire connectée DeVinci FabLab.  
Déployée sur Raspberry Pi avec écran tactile 1024×600 en orientation portrait.

---

## Stack

- Python 3.13 + CustomTkinter
- Lecteur NFC PN532 (I2C)
- Solénoïde sur GPIO 26 (BCM)
- Capteur Hall sur GPIO 27 (BCM) *(optionnel)*
- Backend : [SmartLock-Authentication-Authorization](https://github.com/DeVinci-FabLab/SmartLock-Authentication-Authorization)

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

Insérer la SD dans le RPi, alimenter, attendre ~2 minutes (cloud-init + expansion FS).

Trouver l'IP du RPi (MAC `b8:27:eb:*` ou `dc:a6:32:*`) :
```bash
arp -a
```

Se connecter :
```bash
ssh locker@<IP_DU_RPI>
```

### 3. Installer les dépendances système

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y xorg python3-pip python3-venv python3-tk xinput i2c-tools
sudo raspi-config nonint do_i2c 0      # activer I2C pour le PN532
sudo raspi-config nonint do_boot_behaviour B2  # auto-login console
sudo reboot
```

### 4. Transférer le projet

Depuis **Windows**, dans un terminal PowerShell :

```powershell
scp -r "C:\chemin\vers\SmartLock-IHM" locker@<IP_DU_RPI>:/home/locker/
```

### 5. Installer les dépendances Python

```bash
cd ~/SmartLock-IHM
python3 -m venv venv
source venv/bin/activate
cat > requirements.txt << 'EOF'
customtkinter>=5.2.2
darkdetect==0.8.0
packaging==26.0
python-dotenv>=1.0.0
requests>=2.31.0
pillow>=10.0.0
RPi.GPIO
adafruit-blinka
adafruit-circuitpython-pn532
EOF
pip install -r requirements.txt
```

### 6. Configurer l'environnement

```bash
cp .env.example .env
nano .env
```

Remplir les valeurs :

```env
SIMULATION_MODE=False
API_URL=https://api.smartlock.devinci-fablab.fr
KEYCLOAK_URL=https://auth.devinci-fablab.fr
KEYCLOAK_REALM=dev
LOCKER_CLIENT_SECRET=<secret du client smartlock-lockers dans Keycloak>
LOCKER_ID=1
```

### 7. Configurer le démarrage automatique

```bash
cat > ~/.xinitrc << 'EOF'
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

### 8. Redémarrer

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

### Capteur Hall (optionnel — détection fermeture porte)

| Capteur Hall | Raspberry Pi |
|-------------|-------------|
| VCC  | 3.3V (pin 1) |
| GND  | GND (pin 6) |
| OUT  | GPIO 27 (pin 13) |

Logique : aimant présent (porte fermée) → signal LOW.

---

## Déploiement des mises à jour

Depuis Windows :

```powershell
scp -r "C:\chemin\vers\SmartLock-IHM" locker@<IP_DU_RPI>:/home/locker/
ssh locker@<IP_DU_RPI> "sudo reboot"
```

---

## Logs

```bash
tail -f ~/smartlock.log
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
