import customtkinter as ctk
from src.models import globals as g
from src.logic.api_service import commander_ouverture_relais, verifier_etat_porte, envoyer_alerte_discord

def ouvrir_ecran_physique(fenetre, relancer_nav_callback):
    for widget in fenetre.winfo_children():
        widget.destroy()

    W, H = g.SW, g.SH
    fs = int(H * 0.022)
    fs_title = int(H * 0.026)

    ouverture_reussie = commander_ouverture_relais()
    if not ouverture_reussie:
        print("🚨 ERREUR : Le verrou n'a pas répondu.")

    def checker_porte():
        if verifier_etat_porte():
            print("✅ Porte refermée détectée. Fin de session.")
            fermer_session()
        else:
            g.timer_porte_id = fenetre.after(2000, checker_porte)

    def alerte_discord_et_quitter():
        envoyer_alerte_discord(motif="Armoire non refermée après 10 minutes")
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

    header = ctk.CTkFrame(fenetre, fg_color="transparent", height=int(H * 0.09))
    header.pack(fill="x", padx=int(W * 0.05), pady=(int(H * 0.02), 0))

    ctk.CTkLabel(
        header, text=f"👤 Bienvenue {g.utilisateur_actuel} !",
        font=("Arial", fs_title, "bold"), text_color="black"
    ).pack(side="left")

    ctk.CTkFrame(fenetre, height=2, fg_color="#E0E0E0").pack(fill="x", padx=int(W * 0.05))

    cadre_w = int(W * 0.86)
    cadre_h = int(H * 0.60)

    cadre_central = ctk.CTkFrame(
        fenetre, fg_color="white", corner_radius=12,
        border_width=1, border_color="#E0E0E0",
        width=cadre_w, height=cadre_h
    )
    cadre_central.place(relx=0.5, rely=0.56, anchor="center")
    cadre_central.pack_propagate(False)

    badge = ctk.CTkFrame(
        cadre_central, fg_color="#E9F904", corner_radius=12,
        height=int(H * 0.10), border_width=1, border_color="#D4E404"
    )
    badge.pack(fill="x", padx=int(W * 0.05), pady=int(H * 0.04))

    ctk.CTkLabel(
        badge, text="⚠  Armoire ouverte",
        font=("Arial", int(H * 0.030), "bold"), text_color="black"
    ).place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        cadre_central,
        text="Veuillez prendre votre\nsélection de l'armoire\net rapidement fermer\nderrière vous.",
        font=("Arial", int(H * 0.025)), text_color="black", justify="center"
    ).pack(pady=int(H * 0.03))

    ctk.CTkButton(
        fenetre, text="[ Simulation : Forcer Fermeture ]",
        fg_color="transparent", hover_color="#F2F2F2",
        text_color="#AAAAAA", font=("Arial", fs),
        command=fermer_session
    ).place(relx=0.5, rely=0.95, anchor="center")