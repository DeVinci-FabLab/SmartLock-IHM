import customtkinter as ctk
from PIL import Image
import os
from src.models import globals as g
from src.logic.api_service import identifier_utilisateur, initialiser_stocks, lire_badge_nfc
from src.logic.timer_manager import reset_inactivite

def fermer_fenetre(fenetre):
    print("Inactivité : Fermeture du programme.")
    fenetre.destroy()

def reset_timer(fenetre, event=None):
    reset_inactivite(fenetre, lambda: fermer_fenetre(fenetre), duree_ms=30000)
    print("Chrono Accueil réinitialisé !")

def valider_badge(fenetre):
    uid = lire_badge_nfc()
    if not identifier_utilisateur(uid):
        print("⚠️ Badge non reconnu.")
        return
    initialiser_stocks()

    if g.timer_id:
        fenetre.after_cancel(g.timer_id)
        g.timer_id = None

    fenetre.unbind("<Button-1>")

    for widget in fenetre.winfo_children():
        widget.destroy()

    from src.views.navigation_view import ecran_navigation
    ecran_navigation(
        fenetre,
        revenir_callback=lambda: revenir_accueil(fenetre),
        fermer_callback=lambda: fermer_fenetre(fenetre)
    )

def revenir_accueil(fenetre):
    print("Déconnexion : Retour accueil.")
    g.panier = {}
    g.utilisateur_actuel = "Utilisateur"

    if g.timer_id:
        fenetre.after_cancel(g.timer_id)
        g.timer_id = None

    for widget in fenetre.winfo_children():
        widget.destroy()

    setup_home_screen(fenetre)

def setup_home_screen(fenetre):
    fenetre.configure(fg_color="white")
    W, H = g.SW, g.SH

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    img_path = os.path.join(project_root, 'assets', 'images', 'logo_FabLab.png')

    try:
        img_pil = Image.open(img_path)
        photo_petite = ctk.CTkImage(
            light_image=img_pil,
            size=(int(img_pil.width / 1.7), int(img_pil.height / 1.7))
        )
        g.label_logo = ctk.CTkLabel(fenetre, image=photo_petite, text="")
    except Exception as e:
        print(f"⚠️ Erreur chargement logo ({img_path}): {e}")
        g.label_logo = ctk.CTkLabel(fenetre, text="Logo Introuvable", text_color="#E74C3C")

    g.label_logo.place(relx=0.5, rely=0.30, anchor="center")

    g.sous_titre1 = ctk.CTkLabel(
        fenetre, text='DeVinci Fablab',
        font=('Segoe Print', int(H * 0.025), 'bold'), text_color="black"
    )
    g.sous_titre1.place(relx=0.5, rely=0.50, anchor="center")

    g.trait_accueil = ctk.CTkFrame(fenetre, height=2, width=int(W * 0.76), fg_color="#E0E0E0")
    g.trait_accueil.place(relx=0.5, rely=0.57, anchor="center")

    g.sous_titre2 = ctk.CTkLabel(
        fenetre, text="Badgez pour continuer",
        font=("Segoe Print", int(H * 0.024)), text_color="black"
    )
    g.sous_titre2.place(relx=0.5, rely=0.73, anchor="center")

    g.btn_simu = ctk.CTkButton(
        fenetre, text="SIMULER BADGE",
        width=int(W * 0.18), height=int(H * 0.055),
        corner_radius=12, font=("Arial", int(H * 0.018), "bold"),
        fg_color="#E0E0E0", hover_color="#CCCCCC", text_color="#444444",
        command=lambda: valider_badge(fenetre)
    )
    g.btn_simu.place(relx=0.95, rely=0.95, anchor="se")

    fenetre.bind("<Button-1>", lambda e: reset_timer(fenetre, e))
    reset_timer(fenetre)