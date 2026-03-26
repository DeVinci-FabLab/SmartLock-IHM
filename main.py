# main.py
import customtkinter as ctk
from src.models import globals as g
from src.views.home_view import setup_home_screen, reset_timer
from src.logic.api_service import initialiser_stocks

def main():
    # --- CONFIGURATION FENÊTRE PRINCIPALE ---
    fenetre = ctk.CTk()
    g.fenetre_principale = fenetre 
    
    fenetre.geometry('360x550') 
    fenetre.title('SmartLock - Écran Armoire')
    fenetre.configure(fg_color="white")
    fenetre.resizable(False, False)

    # --- INITIALISATION API ---
    try:
        initialiser_stocks()
        print("Stocks initialisés avec succès au démarrage.")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'initialisation des stocks : {e}")

    # --- INITIALISATION INTERFACE ---
    setup_home_screen(fenetre)

    reset_timer(fenetre)

    # --- BOUCLE PRINCIPALE ---
    fenetre.mainloop()

if __name__ == "__main__":
    main()