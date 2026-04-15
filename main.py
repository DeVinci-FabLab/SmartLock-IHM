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

    #g.SW = 600
    #g.SH = 1024
    #tout est parfait

    g.SW = 1080
    g.SH = 1920
    #ecran trop petit

    #g.SW = 400
    #g.SH = 700
    #le bouton de validation est nickel, mais toujours trop d espace blan en dessous de ce vouton et de panier dans ecran navigation

    #g.SW = 768
    #g.SH = 1024
    #résolution moche mais c est bien géré

    #g.SW = 720
    #g.SH = 1280
    #c est trop grand ca bug de fou sur mon pc

    #g.SW = 800
    #g.SH = 1280
    #j'ai pas la longueur pour fair ca sur mon pc

    #g.SW = 1024
    #g.SH = 600
    #pareil

    #g.SW = 1280
    #g.SH = 720
    #toujours le meme probleme

    #g.SW = 1920
    #g.SH = 1080
    #mon ecran est juste trop petit pas possible de faire de tests

    #g.SW = 800
    #g.SH = 600
    #pareil

    #g.SW = 1024
    #g.SH = 768
    #Bouton valider un peu gros par rapport au reste dans ecran navigation + trop d espace blanc en bas des boutons panier et validaiton, le reste est parfait
    fenetre.geometry(f'{g.SW}x{g.SH}')
    #fenetre.attributes('-fullscreen', True)



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