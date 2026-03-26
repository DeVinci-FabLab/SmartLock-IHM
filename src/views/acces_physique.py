import customtkinter as ctk
from src.models import globals as g

def ouvrir_ecran_physique(fenetre, relancer_nav_callback):
    # 1. Nettoyage de l'écran précédent
    for widget in fenetre.winfo_children():
        widget.destroy()

    # --- LOGIQUE DU TIMER (600 secondes / 10 minutes) ---
    def alerte_discord_et_quitter():
        print("🚨 NOTIFICATION DISCORD : L'armoire n'a pas été refermée à temps !")
        fermer_session()

    def fermer_session():
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        # AU LIEU DE REVENIR A LA NAV, ON VA A L'ECRAN DE CLOTURE
        from src.views.ecran_cloture import ouvrir_ecran_cloture
        ouvrir_ecran_cloture(fenetre, relancer_nav_callback)

    # On lance le timer de sécurité
    g.timer_id = fenetre.after(600000, alerte_discord_et_quitter)

    # --- INTERFACE GRAPHIQUE ---
    # Header (Bienvenue Johnny)
    header = ctk.CTkFrame(fenetre, fg_color="transparent", height=60)
    header.pack(fill="x", padx=20, pady=(10, 0))
    
    ctk.CTkLabel(
        header, text="👤 Bienvenue Johnny !", 
        font=("Arial", 18, "bold"), text_color="black"
    ).pack(side="left", padx=10)

    # Ligne noire de séparation
    ctk.CTkFrame(fenetre, height=2, fg_color="black").pack(fill="x", padx=10)

    # Cadre central blanc
    cadre_central = ctk.CTkFrame(
        fenetre, fg_color="white", corner_radius=30, 
        border_width=2, border_color="black", width=320, height=380
    )
    cadre_central.place(relx=0.5, rely=0.55, anchor="center")
    cadre_central.pack_propagate(False)

    # Badge Jaune "Armoire ouverte"
    badge = ctk.CTkFrame(cadre_central, fg_color="#FCE49D", corner_radius=20, height=70, border_width=1, border_color="black")
    badge.pack(fill="x", padx=25, pady=40)
    
    ctk.CTkLabel(
        badge, text="⚠  Armoire ouverte", 
        font=("Arial", 22, "bold"), text_color="black"
    ).place(relx=0.5, rely=0.5, anchor="center")

    # Texte d'instruction
    ctk.CTkLabel(
        cadre_central, 
        text="Veuillez prendre votre\nsélection de l'armoire\net rapidement fermer\nderrière vous.",
        font=("Arial", 18), text_color="black", justify="center"
    ).pack(pady=20)

    # Bouton de simulation discret
    ctk.CTkButton(
        fenetre, text="[ Simulation : Fermer l'armoire ]", 
        fg_color="transparent", text_color="gray", hover_color="#EEEEEE",
        command=fermer_session
    ).place(relx=0.5, rely=0.95, anchor="center")