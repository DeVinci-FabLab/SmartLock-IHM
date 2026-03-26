import customtkinter as ctk
from src.models import globals as g
from src.logic.api_service import commander_ouverture_relais, verifier_etat_porte

def ouvrir_ecran_physique(fenetre, relancer_nav_callback):
    for widget in fenetre.winfo_children():
        widget.destroy()

    # --- ACTION PHYSIQUE : OUVERTURE ---
    ouverture_reussie = commander_ouverture_relais()
    if not ouverture_reussie:
        print("🚨 ERREUR : Le verrou n'a pas répondu.")

    # --- LOGIQUE DE FERMETURE AUTOMATIQUE ---
    def checker_porte():
        """Vérifie toutes les 2 secondes si la porte a été refermée"""
        if verifier_etat_porte():
            print("✅ Porte refermée détectée. Fin de session.")
            fermer_session()
        else:
            g.timer_porte_id = fenetre.after(2000, checker_porte)

    def alerte_discord_et_quitter():
        print("🚨 NOTIFICATION DISCORD : L'armoire n'a pas été refermée à temps !")
        fermer_session()

    def fermer_session():
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        if hasattr(g, 'timer_porte_id'):
            fenetre.after_cancel(g.timer_porte_id)
            
        from src.views.ecran_cloture import ouvrir_ecran_cloture
        ouvrir_ecran_cloture(fenetre, relancer_nav_callback)

    g.timer_id = fenetre.after(600000, alerte_discord_et_quitter)
    
    checker_porte()

    # --- INTERFACE GRAPHIQUE ---
    header = ctk.CTkFrame(fenetre, fg_color="transparent", height=60)
    header.pack(fill="x", padx=20, pady=(10, 0))
    
    ctk.CTkLabel(
        header, text=f"👤 Bienvenue {g.utilisateur_actuel} !", 
        font=("Arial", 18, "bold"), text_color="black"
    ).pack(side="left", padx=10)

    ctk.CTkFrame(fenetre, height=2, fg_color="black").pack(fill="x", padx=10)

    cadre_central = ctk.CTkFrame(
        fenetre, fg_color="white", corner_radius=30, 
        border_width=2, border_color="black", width=320, height=380
    )
    cadre_central.place(relx=0.5, rely=0.55, anchor="center")
    cadre_central.pack_propagate(False)

    badge = ctk.CTkFrame(cadre_central, fg_color="#FCE49D", corner_radius=20, height=70, border_width=1, border_color="black")
    badge.pack(fill="x", padx=25, pady=40)
    
    ctk.CTkLabel(
        badge, text="⚠  Armoire ouverte", 
        font=("Arial", 22, "bold"), text_color="black"
    ).place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        cadre_central, 
        text="Veuillez prendre votre\nsélection de l'armoire\net rapidement fermer\nderrière vous.",
        font=("Arial", 18), text_color="black", justify="center"
    ).pack(pady=20)

    ctk.CTkButton(
        fenetre, text="[ Simulation : Forcer Fermeture ]", 
        fg_color="transparent", text_color="gray", hover_color="#EEEEEE",
        command=fermer_session
    ).place(relx=0.5, rely=0.95, anchor="center")