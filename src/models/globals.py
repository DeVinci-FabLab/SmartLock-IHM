# src/models/globals.py
fenetre_principale = None
timer_id = None
panier = {}

# Accueil
label_logo = sous_titre1 = trait_accueil = sous_titre2 = btn_simu = None

# --- GESTION DES STOCKS --- IL FAUDRA REFLECHIR AVEC LA PARTIE BACK END ET TOUT
stocks = {
    # FILAMENTS
    "PLA Rouge": 10, "PLA Bleu": 10, "PLA Vert": 10, "PLA Jaune": 10, "PLA Orange": 10, "PLA Gris": 10,
    "PETG Rouge": 10, "PETG Bleu": 10, "PETG Vert": 10, "PETG Jaune": 10, "PETG Orange": 10, "PETG Gris": 10,
    "ASA Rouge": 10, "ASA Bleu": 10, "ASA Vert": 10, "ASA Jaune": 10, "ASA Orange": 10, "ASA Gris": 10,

    # TENDANCES (Ajoute-les pour éviter le stock à 0)
    "Item 1": 10, 
    "Item 2": 10, 
    "Item 3": 10,

    # ELECTRONIQUE (Ajoute-les aussi)
    "driver": 10,
    "moteur": 10
}

# --- ÉLÉMENTS DE NAVIGATION ---
titre_nav = trait_nav = btn_retour = btn_valider = None
bouton_tendance = bouton_filaments = bouton_Electronique = None
sous_titre_nav1 = trait_tendances = None
bouton_tendance1 = bouton_tendance2 = bouton_tendance3 = None
sous_titre_nav2 = trait_filaments = None
bouton_filament1 = bouton_filament2 = bouton_filament3 = None
sous_titre_nav3 = trait_electronique = None
bouton_electronique1 = bouton_electronique2 = None
btn_voir_panier = None
cadre_tendances = cadre_filaments = cadre_elec = None

# --- ÉLÉMENTS COULEURS ---
titre_couleur = btn_annuler_couleur = None
btn_rouge = btn_bleu = btn_vert = btn_jaune = btn_orange = btn_gris = None

# --- ÉLÉMENTS PANIER ---
cadre_liste = btn_retour_panier = None