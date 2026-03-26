import customtkinter as ctk
from src.models import globals as g

def ouvrir_selection_couleur(fenetre, materiau, relancer_nav_callback):
    """
    Interface de choix de couleur avec boutons colorés.
    Redirige vers ouvrir_ecran_selection après le choix.
    """
    # 1. On nettoie l'affichage
    for widget in fenetre.winfo_children():
        widget.place_forget()
    
    # --- GESTION DU TIMER ---
    if g.timer_id:
        fenetre.after_cancel(g.timer_id)
    
    def auto_retour_navigation():
        nettoyer_ecran_couleur()
        relancer_nav_callback()

    g.timer_id = fenetre.after(90000, auto_retour_navigation)
    
    # 2. Titre de l'écran
    g.titre_couleur = ctk.CTkLabel(fenetre, text=f"Choisir Couleur : {materiau}", font=("Segoe Print", 16, "bold"), text_color="black")
    g.titre_couleur.place(relx=0.5, y=50, anchor="center")

    # --- LOGIQUE STOCK ---
    def get_btn_config(color_name, base_color):
        full_name = f"{materiau} {color_name}"
        stock = g.stocks.get(full_name, 0)
        dans_panier = full_name in g.panier
        
        if stock <= 0:
            return "#D7D7D7", "disabled", f"{color_name}\n(Vide)"
        elif dans_panier:
            return "#7CDD81", "normal", color_name
        else:
            return base_color, "normal", color_name

    # Configuration des styles
    c_rouge, s_rouge, t_rouge = get_btn_config("Rouge", "#E89595")
    c_bleu, s_bleu, t_bleu = get_btn_config("Bleu", "#B9E9FF")
    c_vert, s_vert, t_vert = get_btn_config("Vert", "#C1FFD7")
    c_jaune, s_jaune, t_jaune = get_btn_config("Jaune", "#FFFF9D")
    c_orange, s_orange, t_orange = get_btn_config("Orange", "#F6CF94")
    c_gris, s_gris, t_gris = get_btn_config("Gris", "#D7D7D7")

    # --- FONCTION DE CLIC ---
    def clic_couleur(couleur):
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        valider_choix_couleur(materiau, couleur, relancer_nav_callback)

    # 3. Placement des Boutons
    g.btn_rouge = ctk.CTkButton(fenetre, text=t_rouge, fg_color=c_rouge, hover_color="#D45757", text_color="black", 
                                width=105, height=50, font=("Arial", 13, "bold"), state=s_rouge,
                                command=lambda: clic_couleur("Rouge"))
    g.btn_rouge.place(x=65, y=190, anchor="center")

    g.btn_bleu = ctk.CTkButton(fenetre, text=t_bleu, fg_color=c_bleu, hover_color="#648DDA", text_color="black", 
                               width=105, height=50, font=("Arial", 13, "bold"), state=s_bleu,
                               command=lambda: clic_couleur("Bleu"))
    g.btn_bleu.place(relx=0.5, y=190, anchor="center")
    
    g.btn_vert = ctk.CTkButton(fenetre, text=t_vert, fg_color=c_vert, hover_color="#63D084", text_color="black", 
                               width=105, height=50, font=("Arial", 13, "bold"), state=s_vert,
                               command=lambda: clic_couleur("Vert"))
    g.btn_vert.place(x=295, y=190, anchor="center")

    g.btn_jaune = ctk.CTkButton(fenetre, text=t_jaune, fg_color=c_jaune, hover_color="#D9DF17", text_color="black", 
                                width=105, height=50, font=("Arial", 13, "bold"), state=s_jaune,
                                command=lambda: clic_couleur("Jaune"))
    g.btn_jaune.place(x=295, y=250, anchor="center")

    g.btn_orange = ctk.CTkButton(fenetre, text=t_orange, fg_color=c_orange, hover_color="#D27C02", text_color="black", 
                                 width=105, height=50, font=("Arial", 13, "bold"), state=s_orange,
                                 command=lambda: clic_couleur("Orange"))
    g.btn_orange.place(relx=0.5, y=250, anchor="center")

    g.btn_gris = ctk.CTkButton(fenetre, text=t_gris, fg_color=c_gris, hover_color="#868686", text_color="black", 
                               width=105, height=50, font=("Arial", 13, "bold"), state=s_gris,
                               command=lambda: clic_couleur("Gris"))
    g.btn_gris.place(x=65, y=250, anchor="center")

    # 4. Bouton Voir Panier 
    from src.views.vue_panier import ouvrir_vue_panier
    def voir_panier():
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        # On passe une fonction qui recharge la sélection de couleur en cas de retour
        ouvrir_vue_panier(fenetre, lambda: ouvrir_selection_couleur(fenetre, materiau, relancer_nav_callback))

    g.btn_voir_panier = ctk.CTkButton(
        fenetre, text="🛒 Voir Panier", width=200, height=45, corner_radius=15,
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
        fenetre, text="Annuler", fg_color="#E74C3C", text_color="white", width=200, height=45, corner_radius=15,
        command=annuler
    )
    g.btn_annuler_couleur.place(relx=0.5, y=480, anchor="center")

def valider_choix_couleur(materiau, couleur, relancer_nav_callback):
    """
    Fait le pont vers l'écran de sélection de quantité avec le nom complet.
    """
    nom_item_complet = f"{materiau} {couleur}"
    
    # --- CORRECTION DE L'IMPORT ET DE L'APPEL ---
    from src.views.ecran_selection import ouvrir_ecran_selection
    
    nettoyer_ecran_couleur()
    # On utilise g.fenetre_principale ou la fenêtre passée en paramètre
    ouvrir_ecran_selection(g.fenetre_principale, nom_item_complet, relancer_nav_callback)

def nettoyer_ecran_couleur():
    """Nettoie proprement les widgets de cet écran."""
    widgets_to_clean = [
        "titre_couleur", "btn_rouge", "btn_bleu", "btn_vert", 
        "btn_jaune", "btn_orange", "btn_gris", 
        "btn_voir_panier", "btn_annuler_couleur"
    ]
    for attr in widgets_to_clean:
        w = getattr(g, attr, None)
        if w is not None:
            try:
                w.place_forget()
            except:
                pass
            setattr(g, attr, None)