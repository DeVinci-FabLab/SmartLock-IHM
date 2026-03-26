import customtkinter as ctk
from src.models import globals as g
from src.logic.inventory_logic import toggle_selection
from src.views.selection_couleur import ecran_choix_couleur
from src.views.vue_panier import ouvrir_vue_panier
from src.views.validation_finale import ouvrir_validation_finale

def ecran_navigation(fenetre, revenir_callback, fermer_callback):
    # --- FOND DE FENÊTRE ---
    fenetre.configure(fg_color="white")
    
    for widget in fenetre.winfo_children():
        widget.place_forget()

    def auto_logout():
        for widget in fenetre.winfo_children():
            widget.place_forget()
        revenir_callback()

    def aller_a_validation():
        for widget in fenetre.winfo_children():
            widget.place_forget()
        ouvrir_validation_finale(fenetre, lambda: ecran_navigation(fenetre, revenir_callback, fermer_callback))

    # --- LOGIQUE DES COULEURS DYNAMIQUES ---
    def get_colors(item_name):
        actif = any(key.startswith(item_name) for key in g.panier.keys())
        if actif:
            # Vert pastel -> Vert un peu plus soutenu au survol
            return "#7CDD81", "#68C66D"
        else:
            # Gris très clair -> Gris moyen au survol
            return "#F2F2F2", "#E0E0E0"

    # --- HEADER ---
    ctk.CTkLabel(fenetre, text="👤", font=("Arial", 25)).place(x=20, y=25, anchor="center")

    g.titre_nav = ctk.CTkLabel(fenetre, text="Bienvenue Johnny !", font=("Segoe Print", 15), text_color="black")
    g.titre_nav.place(x=140, y=25, anchor="center")
    
    g.trait_nav = ctk.CTkFrame(fenetre, height=2, width=360, fg_color="black")
    g.trait_nav.place(relx=0.5, y=50, anchor="center")

    # --- MENU PRINCIPAL ---
    style_menu = {
        "width": 115, 
        "height": 40, 
        "fg_color": "white", 
        "border_width": 1, 
        "border_color": "#E0E0E0", 
        "text_color": "Black", 
        "hover_color": "#F2F2F2" # Survol léger pour le menu blanc
    }

    g.bouton_tendance = ctk.CTkButton(fenetre, text="Tendances", **style_menu)
    g.bouton_tendance.place(x=62, y=85, anchor="center")

    g.bouton_filaments = ctk.CTkButton(fenetre, text="Filaments", **style_menu)
    g.bouton_filaments.place(relx=0.5, y=85, anchor="center")

    g.bouton_Electronique = ctk.CTkButton(fenetre, text="Electronique", **style_menu)
    g.bouton_Electronique.place(x=298, y=85, anchor="center")

    # --- SECTION TENDANCES ---
    g.cadre_tendances = ctk.CTkFrame(fenetre, width=350, height=70, corner_radius=15, fg_color="white", border_width=1, border_color="#E0E0E0")
    g.cadre_tendances.place(relx=0.5, y=190, anchor="center")
    
    g.sous_titre_nav1 = ctk.CTkLabel(fenetre, text="Tendances", font=("Segoe Print", 15), text_color="black")
    g.sous_titre_nav1.place(x=27, y=120)
    
    c1, h1 = get_colors("Item 1")
    g.bouton_tendance1 = ctk.CTkButton(fenetre, text="Item 1", width=105, height=50, fg_color=c1, hover_color=h1, text_color="Black",
                                       command=lambda: toggle_selection(g.bouton_tendance1, "Item 1", fenetre, revenir_callback))
    g.bouton_tendance1.place(x=65, y=190, anchor="center")

    c2, h2 = get_colors("Item 2")
    g.bouton_tendance2 = ctk.CTkButton(fenetre, text="Item 2", width=105, height=50, fg_color=c2, hover_color=h2, text_color="Black",
                                       command=lambda: toggle_selection(g.bouton_tendance2, "Item 2", fenetre, revenir_callback))
    g.bouton_tendance2.place(relx=0.5, y=190, anchor="center")

    c3, h3 = get_colors("Item 3")
    g.bouton_tendance3 = ctk.CTkButton(fenetre, text="Item 3", width=105, height=50, fg_color=c3, hover_color=h3, text_color="Black",
                                       command=lambda: toggle_selection(g.bouton_tendance3, "Item 3", fenetre, revenir_callback))
    g.bouton_tendance3.place(x=295, y=190, anchor="center")

    # --- SECTION FILAMENTS ---
    g.cadre_filaments = ctk.CTkFrame(fenetre, width=350, height=70, corner_radius=15, fg_color="white", border_width=1, border_color="#E0E0E0")
    g.cadre_filaments.place(relx=0.5, y=300, anchor="center")
    
    g.sous_titre_nav2 = ctk.CTkLabel(fenetre, text="Filaments", font=("Segoe Print", 15), text_color="black")
    g.sous_titre_nav2.place(x=27, y=230)

    f1, fh1 = get_colors("PLA")
    g.bouton_filament1 = ctk.CTkButton(fenetre, text="PLA", width=105, height=50, fg_color=f1, hover_color=fh1, text_color="Black",
                                       command=lambda: ecran_choix_couleur(fenetre, "PLA", revenir_callback, lambda: ecran_navigation(fenetre, revenir_callback, fermer_callback)))
    g.bouton_filament1.place(x=65, y=300, anchor="center")

    f2, fh2 = get_colors("PETG")
    g.bouton_filament2 = ctk.CTkButton(fenetre, text="PETG", width=105, height=50, fg_color=f2, hover_color=fh2, text_color="Black", 
                                       command=lambda: ecran_choix_couleur(fenetre, "PETG", revenir_callback, lambda: ecran_navigation(fenetre, revenir_callback, fermer_callback)))
    g.bouton_filament2.place(relx=0.5, y=300, anchor="center")

    f3, fh3 = get_colors("ASA")
    g.bouton_filament3 = ctk.CTkButton(fenetre, text="ASA", width=105, height=50, fg_color=f3, hover_color=fh3, text_color="Black", 
                                       command=lambda: ecran_choix_couleur(fenetre, "ASA", revenir_callback, lambda: ecran_navigation(fenetre, revenir_callback, fermer_callback)))
    g.bouton_filament3.place(x=295, y=300, anchor="center")

    # --- SECTION ELECTRONIQUE ---
    g.cadre_elec = ctk.CTkFrame(fenetre, width=235, height=70, corner_radius=15, fg_color="white", border_width=1, border_color="#E0E0E0")
    g.cadre_elec.place(x=124, y=420, anchor="center")
   
    g.sous_titre_nav3 = ctk.CTkLabel(fenetre, text="Electronique", font=("Segoe Print", 15), text_color="black")
    g.sous_titre_nav3.place(x=27, y=350)

    e1, eh1 = get_colors("driver")
    g.bouton_electronique1 = ctk.CTkButton(fenetre, text="driver", width=105, height=50, fg_color=e1, hover_color=eh1, text_color="Black",
                                           command=lambda: toggle_selection(g.bouton_electronique1, "driver", fenetre, revenir_callback))
    g.bouton_electronique1.place(x=65, y=420, anchor="center")

    e2, eh2 = get_colors("moteur")
    g.bouton_electronique2 = ctk.CTkButton(fenetre, text="moteur", width=105, height=50, fg_color=e2, hover_color=eh2, text_color="Black",
                                           command=lambda: toggle_selection(g.bouton_electronique2, "moteur", fenetre, revenir_callback))
    g.bouton_electronique2.place(relx=0.5, y=420, anchor="center")

    # --- BOUTONS BAS ---
    g.btn_voir_panier = ctk.CTkButton(fenetre, text="Voir Panier", width=115, height=40, corner_radius=20, fg_color="#E9F904", hover_color="#D4E404", text_color="black", font=("Arial", 12, "bold"),
        command=lambda: ouvrir_vue_panier(fenetre, lambda: ecran_navigation(fenetre, revenir_callback, fermer_callback)))
    g.btn_voir_panier.place(x=20, rely=0.94, anchor="sw")

    g.btn_retour = ctk.CTkButton(fenetre, text="Déconnexion", width=60, height=30, fg_color="#E74C3C", hover_color="#C0392B", command=auto_logout)
    g.btn_retour.place(x=310, y=25, anchor="center")

    from src.logic.inventory_logic import update_validation_button
    g.btn_valider = ctk.CTkButton(fenetre, text="✓", font=("Arial", 30, "bold"), width=70, height=70, corner_radius=35, fg_color="gray", state="disabled", text_color="white",
                                  command=aller_a_validation)
    g.btn_valider.place(x=285, rely=0.9, anchor="center")
    
    update_validation_button()
    if g.timer_id: fenetre.after_cancel(g.timer_id)
    g.timer_id = fenetre.after(90000, auto_logout)