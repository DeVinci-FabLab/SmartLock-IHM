# == ÉTAT MÉTIER ==
fenetre_principale = None
timer_id = None
timer_porte_id = None
panier = {}

utilisateur_actuel = "Utilisateur"
stocks = {}
stock_ids: dict = {}         # item_name → stock_entry_id
categories_items: dict = {}  # category_name → [item_name, ...]
items_description: dict = {} # item_name → description
derniere_raison_acces: str | None = None   # raison du dernier refus badge
dernier_display_name: str | None = None    # nom lors du dernier accès

# == DIMENSIONS ÉCRAN (calculées au démarrage dans main.py) ==
SW = 1024
SH = 600

# == RÉFÉRENCES WIDGETS UI ==
label_logo = None
sous_titre1 = None
trait_accueil = None
sous_titre2 = None
btn_simu = None

titre_nav = None
btn_retour = None
btn_valider = None
btn_voir_panier = None

cadre_tendances = None
cadre_filaments = None
cadre_elec = None

dict_widgets_panier = {}
cadre_liste = None
btn_retour_panier = None

titre_couleur = None
btn_rouge = None
btn_bleu = None
btn_vert = None
btn_jaune = None
btn_orange = None
btn_gris = None
btn_annuler_couleur = None

cadre_feedback = None