import customtkinter as ctk
from src.models import globals as g
from src.views.home_view import setup_home_screen, reset_timer
from src.logic.api_service import initialiser_stocks

def main():
    fenetre = ctk.CTk()
    g.fenetre_principale = fenetre

    fenetre.title('SmartLock - Écran Armoire')
    fenetre.configure(fg_color="white")
    fenetre.resizable(False, False)
    fenetre.geometry('600x1024')
    g.SW = 600
    g.SH = 1024

    try:
        initialiser_stocks()
        print("Stocks initialisés avec succès au démarrage.")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'initialisation des stocks : {e}")

    setup_home_screen(fenetre)
    reset_timer(fenetre)
    fenetre.mainloop()

if __name__ == "__main__":
    main()