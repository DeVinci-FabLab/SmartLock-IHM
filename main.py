import tkinter
import customtkinter as ctk
from src.models import globals as g
from src.views.home_view import setup_home_screen, reset_timer
from src.logic.api_service import initialiser_stocks
from src.logic.logger import logger

# Patch CTkButton.destroy pour Python 3.13 (bug _font dans CTk 5.2.2)
_orig_btn_destroy = ctk.CTkButton.destroy
def _safe_btn_destroy(self):
    try:
        _orig_btn_destroy(self)
    except AttributeError:
        tkinter.Frame.destroy(self)
ctk.CTkButton.destroy = _safe_btn_destroy

def main():
    fenetre = ctk.CTk()
    g.fenetre_principale = fenetre

    fenetre.title('SmartLock - Écran Armoire')
    fenetre.configure(fg_color="white")
    fenetre.resizable(False, False)

    g.SW = 600
    g.SH = 1024
    fenetre.geometry(f'{g.SW}x{g.SH}')

    try:
        initialiser_stocks()
        logger.info("Stocks initialises avec succes au demarrage.")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation des stocks : {e}")

    setup_home_screen(fenetre)
    reset_timer(fenetre)
    fenetre.mainloop()

if __name__ == "__main__":
    main()