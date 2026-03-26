import customtkinter as ctk
from PIL import Image
import os
from src.models import globals as g
from src.logic.api_service import identifier_utilisateur, commander_ouverture_relais

# --- FONCTIONS DE LOGIQUE ---

def fermer_fenetre(fenetre):
    print("Inactivité : Fermeture du programme.")
    fenetre.destroy()

def reset_timer(fenetre, event=None):
    if g.timer_id:
        fenetre.after_cancel(g.timer_id)
    g.timer_id = fenetre.after(30000, lambda: fermer_fenetre(fenetre))
    print("Chrono Accueil réinitialisé !")

def tentative_connexion(fenetre):
    """Gère le badgeage ou la simulation"""
    uid_test = "123456789" # ID envoyé au serveur
    
    # --- BLOC DE TEST (A supprimer quand j aurais les URL) ---
    print("MODE TEST : On force l'identification pour bypasser l'erreur API.")
    g.utilisateur_actuel = "Johnny" 
    commander_ouverture_relais()   
    passer_a_la_navigation(fenetre)
    return 

    # --- CODE RÉEL (Sera utilisé avec les vraies URL) ---
    if identifier_utilisateur(uid_test):
        commander_ouverture_relais()
        passer_a_la_navigation(fenetre)
    else:
        g.sous_titre2.configure(text="Badge inconnu !", text_color="red")
        fenetre.after(2000, lambda: g.sous_titre2.configure(text="Badgez pour continuer", text_color="black"))

def passer_a_la_navigation(fenetre):
    """Nettoie l'écran et lance la navigation"""
    if g.timer_id:
        fenetre.after_cancel(g.timer_id)
        g.timer_id = None

    fenetre.unbind("<Button-1>")

    for widget in fenetre.winfo_children():
        widget.destroy()

    from src.components.navigation_view import ecran_navigation
    
    ecran_navigation(
        fenetre, 
        revenir_callback=lambda: revenir_accueil(fenetre), 
        fermer_callback=lambda: fermer_fenetre(fenetre) 
    )

def revenir_accueil(fenetre):
    """Reset complet pour l'utilisateur suivant"""
    print("Déconnexion : Retour accueil.")
    
    g.panier = {} 
    g.utilisateur_actuel = None 

    if g.timer_id:
        fenetre.after_cancel(g.timer_id)
        g.timer_id = None

    for widget in fenetre.winfo_children():
        widget.destroy()

    setup_home_screen(fenetre)

# --- INITIALISATION DE L'ÉCRAN D'ACCUEIL ---

def setup_home_screen(fenetre):
    fenetre.configure(fg_color="white")
    
    img_path = os.path.join('images', 'logo_FabLab.png')

    try:
        img_pil = Image.open(img_path)
        photo_petite = ctk.CTkImage(
            light_image=img_pil, 
            size=(int(img_pil.width / 1.7), int(img_pil.height / 1.7))
        )
        g.label_logo = ctk.CTkLabel(fenetre, image=photo_petite, text="")
    except:
        g.label_logo = ctk.CTkLabel(fenetre, text="Logo Introuvable", text_color="red")

    g.label_logo.place(relx=0.5, y=165, anchor="center")

    g.sous_titre1 = ctk.CTkLabel(fenetre, text='DeVinci Fablab', font=('Segoe Print', 14, 'bold'), text_color="black")
    g.sous_titre1.place(relx=0.5, y=275, anchor="center")

    g.trait_accueil = ctk.CTkFrame(fenetre, height=2, width=275, fg_color="black")
    g.trait_accueil.place(relx=0.5, y=315, anchor="center")

    g.sous_titre2 = ctk.CTkLabel(fenetre, text="Badgez pour continuer", font=("Segoe Print", 13), text_color="black")
    g.sous_titre2.place(relx=0.5, y=400, anchor="center")

    g.btn_simu = ctk.CTkButton(
        fenetre, text="SIMULER BADGE", width=100, height=25, 
        font=("Arial", 10), fg_color="gray70", hover_color="gray50",
        command=lambda: tentative_connexion(fenetre)
    )
    g.btn_simu.place(relx=0.95, rely=0.95, anchor="se")
    
    # Timer d'inactivité
    fenetre.bind("<Button-1>", lambda e: reset_timer(fenetre, e))
    reset_timer(fenetre)