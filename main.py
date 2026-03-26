# main.py
import customtkinter as ctk
from src.models import globals as g
from src.views.home_view import setup_home_screen, reset_timer


def main():
    # --- CONFIGURATION FENÊTRE PRINCIPALE ---
    fenetre = ctk.CTk()
    g.fenetre_principale = fenetre
    fenetre.geometry('360x550') 
    fenetre.title('Écran de l\'armoire')
    fenetre.configure(fg_color="white")
    fenetre.resizable(False, False)

    # --- INITIALISATION ---
    # On charge les widgets de l'accueil
    setup_home_screen(fenetre)

    # Lancer le timer d'inactivité initial
    reset_timer(fenetre)

    # --- BOUCLE PRINCIPALE ---
    fenetre.mainloop()

if __name__ == "__main__":
    main()