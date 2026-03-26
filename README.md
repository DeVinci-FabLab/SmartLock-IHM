# Smartlock-IHM

📖 À quoi sert le projet ?
SmartLock-IHM est l'interface de contrôle tactile pour le système d'armoire connectée du FabLab. Elle permet une gestion autonome du libre-service matériel en liant l'accès physique à une base de données centralisée.

L'application assure la transition entre l'identification de l'utilisateur, la gestion du panier et la commande de déverrouillage du matériel.

🌟 Pourquoi est-ce utile ?
- Contrôle d'accès automatisé : Identification par badge UID via API.
- Inventaire en temps réel : Synchronisation des stocks avec le backend.
- Interface Intuitive : Navigation optimisée pour écran tactile avec retours visuels colorimétriques.
- Sécurité Matérielle : Monitoring de l'état de la porte et alertes automatiques en cas de non-fermeture.

🚀 Comment démarrer ?
Installation
1. Cloner le dépôt :

git clone https://github.com/votre-repo/SmartLock-IHM.git
cd SmartLock-IHM

2. Création de l'environnement virtuel (Recommandé)

A. Windows :
python -m venv .venv
.venv\Scripts\activate

B. Sur macOS/Linux :
python3 -m venv .venv
source .venv/bin/activate

3. Installation des dépendances
pip install -r requirements.txt

4. Utilisation
python main.py


🛠 Structure du Code
Le projet utilise une architecture MVC (Model-View-Controller) simplifiée :

- src/models/globals.py : État global de l'application (Singleton-like).
- src/views/ : Définition des écrans (Identification, Navigation, Sélection, Clôture).
- src/logic/ : Services API, logique métier de l'inventaire et timers de sécurité.
- images/ : Ressources graphiques et photos des matériaux.

SmartLock-IHM/
├── main.py                 # Point d'entrée de l'application
├── images/                 # Ressources graphiques (Logos, Photos produits)
└── src/
    ├── models/
    │   └── globals.py      # État partagé (panier, utilisateur, stocks)
    ├── logic/
    │   ├── api_service.py  # Appels HTTP (requests) vers le backend
    │   └── inventory_logic.py # Calculs et mise à jour du panier
    ├── views/              # Écrans de l'interface (Identification, Nav, Panier...)
    └── components/         # Éléments UI réutilisables

🆘 Aide et Support
- Problème de Badge : Vérifiez la connectivité avec URL_IDENTIFICATION.
- Erreur Image : Assurez-vous que le dossier images/ est à la racine.
- Logs : Les erreurs de communication API sont affichées dans la console standard.

👥 Contributeurs et Maintenance
Équipe DeVinci FabLab 
