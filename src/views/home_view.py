import threading
import customtkinter as ctk
from PIL import Image
import os
from src.models import globals as g
from src.logic.api_service import identifier_utilisateur, initialiser_stocks, lire_badge_nfc
from src.logic.timer_manager import reset_inactivite
from src.logic.logger import logger

_scan_en_cours = False


def reset_timer(fenetre, event=None):
    reset_inactivite(fenetre, lambda: revenir_accueil(fenetre), duree_ms=120000)


def _afficher_erreur_badge(fenetre, texte: str):
    W, H = g.SW, g.SH
    if hasattr(g, "label_erreur_badge") and g.label_erreur_badge:
        try:
            g.label_erreur_badge.destroy()
        except Exception:
            pass
    g.label_erreur_badge = ctk.CTkLabel(
        fenetre, text=texte,
        font=("Arial", int(H * 0.022), "bold"),
        text_color="white", fg_color="#E74C3C",
        corner_radius=10, wraplength=int(W * 0.7),
    )
    g.label_erreur_badge.place(relx=0.5, rely=0.88, anchor="center")
    fenetre.after(3000, lambda: g.label_erreur_badge.destroy() if g.label_erreur_badge else None)


def _traiter_resultat_scan(fenetre, uid, label_scan):
    global _scan_en_cours
    _scan_en_cours = False

    try:
        label_scan.destroy()
    except Exception:
        pass

    if not uid or not identifier_utilisateur(uid):
        messages = {
            "card_not_registered": "Badge non enregistré\nContactez un administrateur",
            "no_permission":       "Accès non autorisé\npour ce casier",
            "account_revoked":     "Compte désactivé\nContactez un administrateur",
        }
        texte = messages.get(g.derniere_raison_acces or "", "Badge non reconnu")
        _afficher_erreur_badge(fenetre, texte)
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
        fermer_callback=lambda: revenir_accueil(fenetre),
    )


def valider_badge(fenetre):
    global _scan_en_cours
    if _scan_en_cours:
        return
    _scan_en_cours = True

    W, H = g.SW, g.SH
    label_scan = ctk.CTkLabel(
        fenetre, text="En attente de scan...",
        font=("Arial", int(H * 0.022), "bold"),
        text_color="white", fg_color="#3498DB", corner_radius=10,
    )
    label_scan.place(relx=0.5, rely=0.88, anchor="center")

    def scan():
        uid = lire_badge_nfc()
        fenetre.after(0, lambda: _traiter_resultat_scan(fenetre, uid, label_scan))

    threading.Thread(target=scan, daemon=True).start()


def revenir_accueil(fenetre):
    logger.info(f"Retour accueil — session {g.utilisateur_actuel} terminée")
    g.panier = {}
    g.utilisateur_actuel = "Utilisateur"
    g.derniere_raison_acces = None

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
        logger.warning(f"Erreur chargement logo : {e}")
        g.label_logo = ctk.CTkLabel(fenetre, text="Logo Introuvable", text_color="#E74C3C")

    g.label_erreur_badge = None
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

    from src.logic.api_service import SIMULATION_MODE
    btn_label = "SIMULER BADGE" if SIMULATION_MODE else "Scanner Badge"
    g.btn_simu = ctk.CTkButton(
        fenetre, text=btn_label,
        width=int(W * 0.18), height=int(H * 0.055),
        corner_radius=12, font=("Arial", int(H * 0.018), "bold"),
        fg_color="#E0E0E0", hover_color="#CCCCCC", text_color="#444444",
        command=lambda: valider_badge(fenetre)
    )
    g.btn_simu.place(relx=0.95, rely=0.95, anchor="se")

    fenetre.bind("<Button-1>", lambda e: reset_timer(fenetre, e))
    reset_timer(fenetre)
