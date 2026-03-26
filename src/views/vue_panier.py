import customtkinter as ctk
from src.models import globals as g

def ouvrir_vue_panier(fenetre, relancer_nav_callback):
    # --- GESTION DU TIMER ---
    def auto_logout():
        if g.timer_id:
            try:
                fenetre.after_cancel(g.timer_id)
                g.timer_id = None
            except:
                pass
        for widget in fenetre.winfo_children():
            widget.destroy()
        relancer_nav_callback() 

    if g.timer_id:
        try:
            fenetre.after_cancel(g.timer_id)
            g.timer_id = None
        except:
            pass
    g.timer_id = fenetre.after(90000, auto_logout)

    # 1. NETTOYAGE COMPLET DE LA FENÊTRE
    for widget in fenetre.winfo_children():
        widget.destroy()
    
    # Reset du dictionnaire de widgets pour l'affichage actuel
    g.dict_widgets_panier.clear()

    # 2. TITRE
    ctk.CTkLabel(
        fenetre, 
        text="Récapitulatif Panier", 
        font=("Segoe Print", 22, "bold"), 
        text_color="#2C3E50"
    ).place(relx=0.5, y=35, anchor="center")

    # 3. CADRE SCROLLABLE 
    g.cadre_liste = ctk.CTkScrollableFrame(
        fenetre, 
        width=300, 
        height=330, 
        fg_color="#FDFDFD", 
        border_width=2, 
        border_color="#E0E0E0",
        label_text="Articles sélectionnés",
        label_font=("Arial", 12, "bold")
    )
    g.cadre_liste.place(relx=0.5, y=205, anchor="center")

    # 4. AFFICHAGE DES ITEMS 
    if not g.panier or len(g.panier) == 0:
        ctk.CTkLabel(
            g.cadre_liste, 
            text="Votre panier est vide...", 
            font=("Arial", 14, "italic"), 
            text_color="gray"
        ).pack(pady=110)
    else:
        # On parcourt le dictionnaire du panier
        for item, quantite in g.panier.items():
            # Création du label
            label_item = ctk.CTkLabel(
                g.cadre_liste, 
                text=f"• {item} (x{quantite})", 
                font=("Arial", 14, "bold"), 
                text_color="black",
                anchor="w"
            )
            label_item.pack(fill="x", padx=10, pady=8)
            
            # Sauvegarde du widget pour le nettoyage API (Back-end)
            g.dict_widgets_panier[item] = label_item
            print(f"Widget créé pour : {item}")

    # 5. FONCTION DE SORTIE
    def quitter_panier():
        if g.timer_id:
            try:
                fenetre.after_cancel(g.timer_id)
                g.timer_id = None
            except:
                pass
        for widget in fenetre.winfo_children():
            widget.destroy()
        
        fenetre.after(100, lambda: relancer_nav_callback())

    # 6. BOUTONS BAS D'ÉCRAN
    g.btn_retour_panier = ctk.CTkButton(
        fenetre, text="← Continuer la sélection", width=250, height=40,
        fg_color="#B9E9FF", text_color="black", hover_color="#A0D8F0",
        font=("Arial", 13, "bold"),
        command=quitter_panier
    )
    g.btn_retour_panier.place(relx=0.5, y=450, anchor="center")

    if g.panier:
        ctk.CTkButton(
            fenetre, text="Vider le panier", width=150, height=30,
            fg_color="#FFCCCC", text_color="#C0392B", hover_color="#FFB3B3",
            font=("Arial", 11),
            command=lambda: [g.panier.clear(), g.dict_widgets_panier.clear(), ouvrir_vue_panier(fenetre, relancer_nav_callback)]
        ).place(relx=0.5, y=500, anchor="center")

# --- FONCTION UTILITAIRE POUR TON API (BACK-END) ---
def vider_panier_apres_validation():
    """Supprime les widgets et vide les datas une fois la commande validée en base"""
    for widget in g.dict_widgets_panier.values():
        try:
            widget.destroy()
        except:
            pass
    g.dict_widgets_panier.clear()
    g.panier.clear()
    print("Panier et widgets vidés avec succès.")