import customtkinter as ctk
from src.models import globals as g

def ouvrir_vue_panier(fenetre, relancer_nav_callback):
    # --- GESTION DU TIMER ---
    def auto_logout():
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        for widget in fenetre.winfo_children():
            widget.destroy()
        relancer_nav_callback() 

    # On annule l'ancien et on lance 90s
    if g.timer_id:
        fenetre.after_cancel(g.timer_id)
    g.timer_id = fenetre.after(90000, auto_logout)

    # 1. NETTOYAGE COMPLET (On détruit tout au lieu de cacher)
    for widget in fenetre.winfo_children():
        widget.destroy()

    # 2. TITRE
    ctk.CTkLabel(
        fenetre, 
        text="Récapitulatif Panier", 
        font=("Segoe Print", 22, "bold"), 
        text_color="#2C3E50"
    ).place(relx=0.5, y=35, anchor="center")

    # 3. CADRE SCROLLABLE (Modifié pour le tactile)
    g.cadre_liste = ctk.CTkScrollableFrame(
        fenetre, 
        width=300, 
        height=330, 
        fg_color="#FDFDFD", 
        border_width=2, 
        border_color="#E0E0E0",
        label_text="Articles sélectionnés",
        label_font=("Arial", 12, "bold"),
        scrollbar_button_color="#D0D0D0",      # Couleur barre tactile
        scrollbar_button_hover_color="#A0A0A0" # Couleur barre pression
    )
    g.cadre_liste.place(relx=0.5, y=205, anchor="center")

    # 4. AFFICHAGE DES ITEMS
    if not g.panier:
        ctk.CTkLabel(
            g.cadre_liste, 
            text="Votre panier est vide...", 
            font=("Arial", 14, "italic"), 
            text_color="gray"
        ).pack(pady=110)
    else:
        for item, quantite in g.panier.items():
            ctk.CTkLabel(
                g.cadre_liste, 
                text=f"• {item} (x{quantite})", 
                font=("Arial", 14), 
                text_color="black",
                anchor="w"
            ).pack(fill="x", padx=10, pady=5)

    # 5. FONCTION DE SORTIE MANUELLE
    def quitter_panier():
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        for widget in fenetre.winfo_children():
            widget.destroy()
        relancer_nav_callback()

    # 6. BOUTONS
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
            command=lambda: [g.panier.clear(), ouvrir_vue_panier(fenetre, relancer_nav_callback)]
        ).place(relx=0.5, y=500, anchor="center")