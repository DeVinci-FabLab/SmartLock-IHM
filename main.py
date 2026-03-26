import customtkinter as ctk
from src.models import globals as g
from src.views.home_view import setup_home_screen, reset_timer
from src.logic.api_service import initialiser_stocks

def main():
    # --- CONFIGURATION FENÊTRE PRINCIPALE ---
    fenetre = ctk.CTk()
    g.fenetre_principale = fenetre
    fenetre.geometry('360x550') 
    fenetre.title('Écran de l\'armoire')
    fenetre.configure(fg_color="white")
    fenetre.resizable(False, False)

    # --- INITIALISATION API ---
    print("Démarrage : Synchronisation avec le serveur...")
    initialiser_stocks()

    # --- INITIALISATION IHM ---

    setup_home_screen(fenetre)

    # Lancer le timer d'inactivité initial
    reset_timer(fenetre)

    # --- BOUCLE PRINCIPALE ---
    fenetre.mainloop()

if __name__ == "__main__":
    main()