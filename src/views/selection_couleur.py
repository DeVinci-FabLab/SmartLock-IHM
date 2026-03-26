import customtkinter as ctk
from src.models import globals as g

def ecran_choix_couleur(fenetre, materiau, revenir_callback, relancer_nav_callback):
    # 1. On nettoie l'affichage de la navigation
    for widget in fenetre.winfo_children():
        widget.place_forget()
    
    # --- GESTION DU TIMER (CORRIGÉ : pointe vers relancer_nav_callback) ---
    if g.timer_id:
        fenetre.after_cancel(g.timer_id)
    
    # On définit une fonction de sortie automatique vers la NAVIGATION
    def auto_retour_navigation():
        nettoyer_ecran_couleur()
        relancer_nav_callback()

    g.timer_id = fenetre.after(90000, auto_retour_navigation)
    
    widgets_a_effacer = [
        g.titre_nav, g.trait_nav, g.btn_retour, g.sous_titre_nav1, g.trait_tendances,
        g.bouton_tendance, g.bouton_tendance1, g.bouton_tendance2, g.bouton_tendance3,
        g.bouton_filaments, g.sous_titre_nav2, g.trait_filaments,
        g.bouton_Electronique, g.sous_titre_nav3, g.trait_electronique, g.bouton_filament1,
        g.bouton_filament2, g.bouton_filament3, g.bouton_electronique1, g.bouton_electronique2,
        g.btn_valider, g.btn_voir_panier 
    ]
    for w in widgets_a_effacer:
        if w is not None:
            w.place_forget()

    # 2. Titre de l'écran
    g.titre_couleur = ctk.CTkLabel(fenetre, text=f"Choisir Couleur : {materiau}", font=("Segoe Print", 16, "bold"), text_color="black")
    g.titre_couleur.place(relx=0.5, y=50, anchor="center")

    # --- LOGIQUE VISUELLE : Détermination des couleurs selon le panier ---
    def get_color(color_name):
        full_name = f"{materiau} {color_name}"
        return "#7CDD81" if any(item.startswith(full_name) for item in g.panier) else None

    c_rouge = get_color("Rouge") or "#E89595"
    c_bleu = get_color("Bleu") or "#B9E9FF"
    c_vert = get_color("Vert") or "#C1FFD7"
    c_jaune = get_color("Jaune") or "#FFFF9D"
    c_orange = get_color("Orange") or "#F6CF94"
    c_gris = get_color("Gris") or "#D7D7D7"

    # --- FONCTIONS DE CLIC ---
    def clic_couleur(couleur):
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        valider_choix_couleur(materiau, couleur, relancer_nav_callback)

    # 3. Boutons couleurs
    g.btn_rouge = ctk.CTkButton(fenetre, text="Rouge", fg_color=c_rouge, hover_color="#D45757", text_color="black", 
                                width=105, height=50, font=("Arial", 14, "bold"),
                                command=lambda: clic_couleur("Rouge"))
    g.btn_rouge.place(x=65, y=190, anchor="center")

    g.btn_bleu = ctk.CTkButton(fenetre, text="Bleu", fg_color=c_bleu, hover_color="#648DDA", text_color="black", 
                               width=105, height=50, font=("Arial", 14, "bold"),
                               command=lambda: clic_couleur("Bleu"))
    g.btn_bleu.place(relx=0.5, y=190, anchor="center")
    
    g.btn_vert = ctk.CTkButton(fenetre, text="Vert", fg_color=c_vert, hover_color="#63D084", text_color="black", 
                               width=105, height=50, font=("Arial", 14, "bold"),
                               command=lambda: clic_couleur("Vert"))
    g.btn_vert.place(x=295, y=190, anchor="center")

    g.btn_jaune = ctk.CTkButton(fenetre, text="Jaune", fg_color=c_jaune, hover_color="#D9DF17", text_color="black", 
                                width=105, height=50, font=("Arial", 14, "bold"),
                                command=lambda: clic_couleur("Jaune"))
    g.btn_jaune.place(x=295, y=250, anchor="center")

    g.btn_orange = ctk.CTkButton(fenetre, text="Orange", fg_color=c_orange, hover_color="#D27C02", text_color="black", 
                                 width=105, height=50, font=("Arial", 14, "bold"),
                                 command=lambda: clic_couleur("Orange"))
    g.btn_orange.place(relx=0.5, y=250, anchor="center")

    g.btn_gris = ctk.CTkButton(fenetre, text="Gris", fg_color=c_gris, hover_color="#868686", text_color="black", 
                               width=105, height=50, font=("Arial", 14, "bold"),
                               command=lambda: clic_couleur("Gris"))
    g.btn_gris.place(x=65, y=250, anchor="center")

    # 4. Bouton Voir Panier 
    from src.views.vue_panier import ouvrir_vue_panier
    def voir_panier():
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        ouvrir_vue_panier(fenetre, lambda: ecran_choix_couleur(fenetre, materiau, revenir_callback, relancer_nav_callback))

    g.btn_voir_panier = ctk.CTkButton(
        fenetre, text="Voir Panier", width=200, height=40,
        fg_color="#E9F904", hover_color="#D4E404", text_color="black",
        font=("Arial", 12, "bold"),
        command=voir_panier
    )
    g.btn_voir_panier.place(relx=0.5, y=420, anchor="center")

    # 5. Bouton Annuler 
    def annuler():
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        nettoyer_ecran_couleur()
        relancer_nav_callback()

    g.btn_annuler_couleur = ctk.CTkButton(
        fenetre, text="Annuler", fg_color="#E74C3C", text_color="black", width=200, height=40,
        command=annuler
    )
    g.btn_annuler_couleur.place(relx=0.5, y=480, anchor="center")

def valider_choix_couleur(materiau, couleur, relancer_nav_callback):
    nom_item = f"{materiau} {couleur}"
    from src.views.ecran_selection import ouvrir_selection_quantite
    nettoyer_ecran_couleur()
    ouvrir_selection_quantite(g.fenetre_principale, nom_item, relancer_nav_callback)

def nettoyer_ecran_couleur():
    widgets = [
        g.titre_couleur, g.btn_rouge, g.btn_bleu, g.btn_vert, 
        g.btn_jaune, g.btn_orange, g.btn_gris, 
        g.btn_voir_panier, g.btn_annuler_couleur
    ]
    for w in widgets:
        if w is not None:
            w.place_forget()