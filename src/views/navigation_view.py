import customtkinter as ctk
from src.models import globals as g
from src.logic.inventory_logic import update_validation_button
from src.logic.timer_manager import reset_inactivite
from src.views.selection_couleur import ouvrir_selection_couleur
from src.views.ecran_selection import ouvrir_ecran_selection
from src.views.vue_panier import ouvrir_vue_panier
from src.views.validation_finale import ouvrir_validation_finale

def ecran_navigation(fenetre, revenir_callback, fermer_callback):
    fenetre.configure(fg_color="white")
    for widget in fenetre.winfo_children():
        widget.place_forget()

    W, H = g.SW, g.SH

    def auto_logout():
        for widget in fenetre.winfo_children():
            widget.destroy()
        revenir_callback()

    def rafraichir():
        ecran_navigation(fenetre, revenir_callback, fermer_callback)

    def aller_a_validation():
        if not g.panier:
            return
        for widget in fenetre.winfo_children():
            widget.destroy()
        ouvrir_validation_finale(fenetre, rafraichir)

    def get_button_style(item_name):
        actif = any(key.startswith(item_name) for key in g.panier.keys())
        if item_name in ["PLA", "ASA", "PETG"]:
            stock = sum(v for k, v in g.stocks.items() if k.startswith(item_name))
        else:
            stock = g.stocks.get(item_name, 0)
        color = "#2ECC71" if actif else "#F2F2F2"
        hover = "#27AE60" if actif else "#E0E0E0"
        text_color = "white" if actif else "black"
        state = "normal" if stock > 0 else "disabled"
        suffixe = "" if stock > 0 else "\n(Vide)"
        return color, hover, text_color, state, suffixe

    fs = int(H * 0.022)
    fs_title = int(H * 0.026)
    btn_w = int(W * 0.27)
    btn_h = int(H * 0.10)
    menu_w = int(W * 0.30)
    menu_h = int(H * 0.058)
    cadre_w = int(W * 0.95)
    cadre_h = int(H * 0.14)

    x_left   = int(W * 0.18)
    x_center = int(W * 0.50)
    x_right  = int(W * 0.82)

    y_header   = int(H * 0.045)
    y_sep      = int(H * 0.09)
    y_menu     = int(H * 0.15)
    y_t_label  = int(H * 0.22)
    y_t_cadre  = int(H * 0.31)
    y_f_label  = int(H * 0.40)
    y_f_cadre  = int(H * 0.49)
    y_e_label  = int(H * 0.58)
    y_e_cadre  = int(H * 0.67)

    ctk.CTkLabel(fenetre, text="👤", font=("Arial", int(H * 0.04))).place(x=int(W * 0.055), y=y_header, anchor="center")
    g.titre_nav = ctk.CTkLabel(
        fenetre, text=f"Bienvenue {g.utilisateur_actuel} !",
        font=("Segoe Print", fs_title, "bold"), text_color="black"
    )
    g.titre_nav.place(x=int(W * 0.40), y=y_header, anchor="center")
    ctk.CTkFrame(fenetre, height=2, width=W, fg_color="#E0E0E0").place(x=0, y=y_sep)

    style_menu = {
        "width": menu_w, "height": menu_h, "corner_radius": 12,
        "fg_color": "white", "border_width": 1, "border_color": "#E0E0E0",
        "text_color": "black", "font": ("Arial", fs, "bold"),
        "hover_color": "#F2F2F2"
    }
    ctk.CTkButton(fenetre, text="Tendances", **style_menu).place(x=x_left, y=y_menu, anchor="center")
    ctk.CTkButton(fenetre, text="Filaments", **style_menu).place(x=x_center, y=y_menu, anchor="center")
    ctk.CTkButton(fenetre, text="Electronique", **style_menu).place(x=x_right, y=y_menu, anchor="center")

    ctk.CTkFrame(fenetre, width=cadre_w, height=cadre_h, corner_radius=12, fg_color="white", border_width=1, border_color="#E0E0E0").place(x=x_center, y=y_t_cadre, anchor="center")
    ctk.CTkLabel(fenetre, text="Tendances", font=("Segoe Print", fs_title, "bold"), text_color="black").place(x=int(W * 0.04), y=y_t_label)

    for i, name in enumerate(["Item 1", "Item 2", "Item 3"]):
        c, h, tc, st, txt = get_button_style(name)
        btn = ctk.CTkButton(
            fenetre, text=f"{name}{txt}", width=btn_w, height=btn_h, corner_radius=12,
            fg_color=c, hover_color=h, text_color=tc,
            border_width=1, border_color="#E0E0E0", state=st,
            font=("Arial", fs, "bold")
        )
        btn.configure(command=lambda n=name: ouvrir_ecran_selection(fenetre, n, rafraichir))
        btn.place(x=[x_left, x_center, x_right][i], y=y_t_cadre, anchor="center")

    ctk.CTkFrame(fenetre, width=cadre_w, height=cadre_h, corner_radius=12, fg_color="white", border_width=1, border_color="#E0E0E0").place(x=x_center, y=y_f_cadre, anchor="center")
    ctk.CTkLabel(fenetre, text="Filaments", font=("Segoe Print", fs_title, "bold"), text_color="black").place(x=int(W * 0.04), y=y_f_label)

    for i, name in enumerate(["PLA", "PETG", "ASA"]):
        c, h, tc, st, txt = get_button_style(name)
        btn = ctk.CTkButton(
            fenetre, text=f"{name}{txt}", width=btn_w, height=btn_h, corner_radius=12,
            fg_color=c, hover_color=h, text_color=tc,
            border_width=1, border_color="#E0E0E0", state=st,
            font=("Arial", fs, "bold")
        )
        btn.configure(command=lambda n=name: ouvrir_selection_couleur(fenetre, n, rafraichir))
        btn.place(x=[x_left, x_center, x_right][i], y=y_f_cadre, anchor="center")

    cadre_e_w = int(W * 0.64)
    ctk.CTkFrame(fenetre, width=cadre_e_w, height=cadre_h, corner_radius=12, fg_color="white", border_width=1, border_color="#E0E0E0").place(x=x_center, y=y_e_cadre, anchor="center")
    ctk.CTkLabel(fenetre, text="Electronique", font=("Segoe Print", fs_title, "bold"), text_color="black").place(x=int(W * 0.04), y=y_e_label)

    for i, name in enumerate(["driver", "moteur"]):
        c, h, tc, st, txt = get_button_style(name)
        btn = ctk.CTkButton(
            fenetre, text=f"{name}{txt}", width=btn_w, height=btn_h, corner_radius=12,
            fg_color=c, hover_color=h, text_color=tc,
            border_width=1, border_color="#E0E0E0", state=st,
            font=("Arial", fs, "bold")
        )
        btn.configure(command=lambda n=name: ouvrir_ecran_selection(fenetre, n, rafraichir))
        btn.place(x=[x_left, x_center][i], y=y_e_cadre, anchor="center")

    g.btn_voir_panier = ctk.CTkButton(
        fenetre, text="🛒 Panier",
        width=int(W * 0.18), height=int(H * 0.082),
        corner_radius=12, fg_color="#E9F904", hover_color="#D4E404",
        text_color="black", font=("Arial", fs, "bold"),
        command=lambda: ouvrir_vue_panier(fenetre, rafraichir)
    )
    g.btn_voir_panier.place(x=int(W * 0.02), rely=0.94, anchor="sw")

    g.btn_retour = ctk.CTkButton(
        fenetre, text="Quitter",
        width=int(W * 0.12), height=int(H * 0.058),
        corner_radius=12, fg_color="#E74C3C", hover_color="#C0392B",
        text_color="white", font=("Arial", fs, "bold"),
        command=auto_logout
    )
    g.btn_retour.place(x=int(W * 0.875), y=y_header, anchor="center")

    btn_val_size = int(H * 0.136)
    g.btn_valider = ctk.CTkButton(
        fenetre, text="✓",
        font=("Arial", int(H * 0.051), "bold"),
        width=btn_val_size, height=btn_val_size,
        corner_radius=btn_val_size // 2,
        fg_color="gray", state="disabled",
        text_color="white", command=aller_a_validation
    )
    g.btn_valider.place(x=int(W * 0.88), rely=0.9, anchor="center")

    update_validation_button()
    reset_inactivite(fenetre, auto_logout)