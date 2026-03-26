import customtkinter as ctk
from src.models import globals as g
from src.logic.inventory_logic import update_validation_button
from src.views.selection_couleur import ouvrir_selection_couleur
from src.views.ecran_selection import ouvrir_ecran_selection
from src.views.vue_panier import ouvrir_vue_panier
from src.views.validation_finale import ouvrir_validation_finale

def ecran_navigation(fenetre, revenir_callback, fermer_callback):
    # --- NETTOYAGE ET FOND ---
    fenetre.configure(fg_color="white")
    for widget in fenetre.winfo_children():
        widget.place_forget()

    def auto_logout():
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        for widget in fenetre.winfo_children():
            widget.destroy()
        revenir_callback()

    # Fonction pour recharger cet écran avec les bonnes couleurs de boutons
    def rafraichir():
        ecran_navigation(fenetre, revenir_callback, fermer_callback)

    def aller_a_validation():
        if not g.panier: return
        for widget in fenetre.winfo_children():
            widget.destroy()
        ouvrir_validation_finale(fenetre, rafraichir)

    # --- LOGIQUE VISUELLE ---
    def get_button_style(item_name):
        # On vérifie si l'item (ou une de ses couleurs) est dans le panier
        actif = any(key.startswith(item_name) for key in g.panier.keys())
        
        if item_name in ["PLA", "ASA", "PETG"]:
            stock = sum(v for k, v in g.stocks.items() if k.startswith(item_name))
        else:
            stock = g.stocks.get(item_name, 0)

        color = "#7CDD81" if actif else "#F2F2F2"
        hover = "#68C66D" if actif else "#E0E0E0"
        state = "normal" if stock > 0 else "disabled"
        suffixe = "" if stock > 0 else "\n(Vide)"
        
        return color, hover, state, suffixe

    # --- HEADER ---
    ctk.CTkLabel(fenetre, text="👤", font=("Arial", 25)).place(x=20, y=25, anchor="center")
    g.titre_nav = ctk.CTkLabel(fenetre, text=f"Bienvenue {g.utilisateur_actuel} !", font=("Segoe Print", 14), text_color="black")
    g.titre_nav.place(x=140, y=25, anchor="center")
    ctk.CTkFrame(fenetre, height=2, width=360, fg_color="black").place(relx=0.5, y=50, anchor="center")

    # --- MENU PRINCIPAL ---
    style_menu = {"width": 110, "height": 35, "fg_color": "white", "border_width": 1, "border_color": "#E0E0E0", "text_color": "Black", "font": ("Arial", 11)}
    ctk.CTkButton(fenetre, text="Tendances", **style_menu).place(x=60, y=85, anchor="center")
    ctk.CTkButton(fenetre, text="Filaments", **style_menu).place(relx=0.5, y=85, anchor="center")
    ctk.CTkButton(fenetre, text="Electronique", **style_menu).place(x=300, y=85, anchor="center")

    x_pos = [65, 180, 295]

    # --- SECTION TENDANCES ---
    ctk.CTkFrame(fenetre, width=350, height=75, corner_radius=15, fg_color="white", border_width=1, border_color="#E0E0E0").place(relx=0.5, y=190, anchor="center")
    ctk.CTkLabel(fenetre, text="Tendances", font=("Segoe Print", 14, "bold"), text_color="black").place(x=25, y=120)
    
    for i, name in enumerate(["Item 1", "Item 2", "Item 3"]):
        c, h, st, txt = get_button_style(name)
        btn = ctk.CTkButton(fenetre, text=f"{name}{txt}", width=100, height=55, fg_color=c, hover_color=h, text_color="Black", state=st)
        # Redirection vers l'écran +/-
        btn.configure(command=lambda n=name: ouvrir_ecran_selection(fenetre, n, rafraichir))
        btn.place(x=x_pos[i], y=190, anchor="center")

    # --- SECTION FILAMENTS ---
    ctk.CTkFrame(fenetre, width=350, height=75, corner_radius=15, fg_color="white", border_width=1, border_color="#E0E0E0").place(relx=0.5, y=305, anchor="center")
    ctk.CTkLabel(fenetre, text="Filaments", font=("Segoe Print", 14, "bold"), text_color="black").place(x=25, y=235)

    for i, name in enumerate(["PLA", "PETG", "ASA"]):
        c, h, st, txt = get_button_style(name)
        btn = ctk.CTkButton(fenetre, text=f"{name}{txt}", width=100, height=55, fg_color=c, hover_color=h, text_color="Black", state=st)
        btn.configure(command=lambda n=name: ouvrir_selection_couleur(fenetre, n, rafraichir))
        btn.place(x=x_pos[i], y=305, anchor="center")

    # --- SECTION ELECTRONIQUE ---
    ctk.CTkFrame(fenetre, width=235, height=75, corner_radius=15, fg_color="white", border_width=1, border_color="#E0E0E0").place(x=124, y=420, anchor="center")
    ctk.CTkLabel(fenetre, text="Electronique", font=("Segoe Print", 14, "bold"), text_color="black").place(x=25, y=355)

    for i, name in enumerate(["driver", "moteur"]):
        c, h, st, txt = get_button_style(name)
        btn = ctk.CTkButton(fenetre, text=f"{name}{txt}", width=100, height=55, fg_color=c, hover_color=h, text_color="Black", state=st)
        # Redirection vers l'écran +/-
        btn.configure(command=lambda n=name: ouvrir_ecran_selection(fenetre, n, rafraichir))
        btn.place(x=x_pos[i], y=420, anchor="center")

    # --- BOUTONS BAS ---
    g.btn_voir_panier = ctk.CTkButton(fenetre, text="Voir Panier", width=110, height=45, corner_radius=22, fg_color="#E9F904", hover_color="#D4E404", text_color="black", font=("Arial", 12, "bold"),
        command=lambda: ouvrir_vue_panier(fenetre, rafraichir))
    g.btn_voir_panier.place(x=20, rely=0.94, anchor="sw")

    g.btn_retour = ctk.CTkButton(fenetre, text="Quitter", width=70, height=30, fg_color="#E74C3C", font=("Arial", 11, "bold"), command=auto_logout)
    g.btn_retour.place(x=315, y=25, anchor="center")

    g.btn_valider = ctk.CTkButton(fenetre, text="✓", font=("Arial", 32, "bold"), width=75, height=75, corner_radius=38, 
                                  fg_color="gray", state="disabled", text_color="white", command=aller_a_validation)
    g.btn_valider.place(x=290, rely=0.9, anchor="center")
    
    update_validation_button()

    if g.timer_id: fenetre.after_cancel(g.timer_id)
    g.timer_id = fenetre.after(90000, auto_logout)