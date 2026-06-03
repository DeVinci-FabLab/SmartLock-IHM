# == ÉTAT MÉTIER ==
fenetre_principale = None
timer_id = None
timer_porte_id = None
panier = {}

utilisateur_actuel = "Utilisateur"
stocks = {}
stock_ids: dict = {}          # item_name → stock_entry_id
categories_items: dict = {}   # category_name → [item_name, ...]
items_description: dict = {}  # item_name → description
items_threshold: dict = {}    # item_name → low_stock_threshold (int | None)
items_unit: dict = {}         # item_name → unit_measure (str)
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

cadre_feedback = None