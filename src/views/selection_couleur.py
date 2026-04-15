import customtkinter as ctk
from src.models import globals as g
from src.logic.timer_manager import reset_inactivite

def ouvrir_selection_couleur(fenetre, materiau, relancer_nav_callback):
    for widget in fenetre.winfo_children():
        widget.place_forget()

    W, H = g.SW, g.SH
    fs = int(H * 0.022)
    fs_title = int(H * 0.026)
    btn_w = int(W * 0.27)
    btn_h = int(H * 0.092)

    def auto_retour_navigation():
        nettoyer_ecran_couleur()
        relancer_nav_callback()

    reset_inactivite(fenetre, auto_retour_navigation)

    g.titre_couleur = ctk.CTkLabel(
        fenetre, text=f"Choisir Couleur : {materiau}",
        font=("Segoe Print", fs_title, "bold"), text_color="black"
    )
    g.titre_couleur.place(relx=0.5, rely=0.09, anchor="center")

    def get_btn_config(color_name, base_color, hover_color):
        full_name = f"{materiau} {color_name}"
        stock = g.stocks.get(full_name, 0)
        dans_panier = full_name in g.panier
        if stock <= 0:
            return "#E0E0E0", "#CCCCCC", "disabled", f"{color_name}\n(Vide)", "#888888"
        elif dans_panier:
            return "#2ECC71", "#27AE60", "normal", color_name, "white"
        else:
            return base_color, hover_color, "normal", color_name, "black"

    couleurs = [
        ("Rouge",  "#E89595", "#C96060"),
        ("Bleu",   "#B9E9FF", "#7BBFE0"),
        ("Vert",   "#C1FFD7", "#63D084"),
        ("Jaune",  "#FFFF9D", "#D9DF17"),
        ("Orange", "#F6CF94", "#D27C02"),
        ("Gris",   "#D7D7D7", "#868686"),
    ]

    x_left   = int(W * 0.18)
    x_center = int(W * 0.50)
    x_right  = int(W * 0.82)
    y_row1   = int(H * 0.25)
    y_row2   = int(H * 0.42)

    positions = [
        (x_left, y_row1), (x_center, y_row1), (x_right, y_row1),
        (x_left, y_row2), (x_center, y_row2), (x_right, y_row2),
    ]

    btn_attrs = ["btn_rouge", "btn_bleu", "btn_vert", "btn_jaune", "btn_orange", "btn_gris"]

    def clic_couleur(couleur):
        valider_choix_couleur(materiau, couleur, relancer_nav_callback)

    for idx, (color_name, base_color, hover_color) in enumerate(couleurs):
        c, h, state, label, tc = get_btn_config(color_name, base_color, hover_color)
        btn = ctk.CTkButton(
            fenetre, text=label, fg_color=c, hover_color=h, text_color=tc,
            width=btn_w, height=btn_h, corner_radius=12,
            border_width=1, border_color="#E0E0E0",
            font=("Arial", fs, "bold"), state=state,
            command=lambda cn=color_name: clic_couleur(cn)
        )
        btn.place(x=positions[idx][0], y=positions[idx][1], anchor="center")
        setattr(g, btn_attrs[idx], btn)

    from src.views.vue_panier import ouvrir_vue_panier

    def voir_panier():
        ouvrir_vue_panier(fenetre, lambda: ouvrir_selection_couleur(fenetre, materiau, relancer_nav_callback))

    g.btn_voir_panier = ctk.CTkButton(
        fenetre, text="🛒 Voir Panier",
        width=int(W * 0.35), height=int(H * 0.082),
        corner_radius=12, fg_color="#E9F904", hover_color="#D4E404",
        text_color="black", font=("Arial", fs, "bold"),
        command=voir_panier
    )
    g.btn_voir_panier.place(relx=0.5, rely=0.72, anchor="center")

    def annuler():
        nettoyer_ecran_couleur()
        relancer_nav_callback()

    g.btn_annuler_couleur = ctk.CTkButton(
        fenetre, text="Annuler",
        width=int(W * 0.35), height=int(H * 0.082),
        corner_radius=12, fg_color="#E74C3C", hover_color="#C0392B",
        text_color="white", font=("Arial", fs, "bold"),
        command=annuler
    )
    g.btn_annuler_couleur.place(relx=0.5, rely=0.86, anchor="center")


def valider_choix_couleur(materiau, couleur, relancer_nav_callback):
    nom_item_complet = f"{materiau} {couleur}"
    from src.views.ecran_selection import ouvrir_ecran_selection
    nettoyer_ecran_couleur()
    ouvrir_ecran_selection(g.fenetre_principale, nom_item_complet, relancer_nav_callback)


def nettoyer_ecran_couleur():
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