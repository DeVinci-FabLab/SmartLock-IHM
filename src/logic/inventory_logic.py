from src.models import globals as g
from src.views.ecran_selection import ouvrir_ecran_selection

def toggle_selection(bouton, item_name, fenetre, revenir_callback):
    """
    Désormais, cette fonction ne change plus juste la couleur.
    Elle redirige l'utilisateur vers l'écran de sélection de quantité.
    """
    # --- RESET DU TIMER D'INACTIVITÉ ---
    if g.timer_id:
        fenetre.after_cancel(g.timer_id)
    
    def retour_nav():
        from src.views.navigation_view import ecran_navigation
        ecran_navigation(fenetre, revenir_callback, None)

    print(f"➡️ Redirection vers sélection pour : {item_name}")
    ouvrir_ecran_selection(fenetre, item_name, retour_nav)

def ajouter_au_panier(nom_item, quantite, relancer_nav_callback):
    """
    Ajoute la quantité choisie au panier global.
    Appelé par l'écran de sélection (celui avec le + et le -).
    """
    try:
        qte_int = int(quantite)
        if qte_int <= 0: return
    except (ValueError, TypeError):
        return 

    stock_max = g.stocks.get(nom_item, 0)
    
    if qte_int > stock_max:
        print(f"⚠️ Quantité limitée au stock disponible : {stock_max}")
        qte_int = stock_max 

    if qte_int <= 0:
        print(f"❌ {nom_item} est en rupture de stock.")
        # On peut quand même relancer pour ne pas rester bloqué
        relancer_nav_callback()
        return

    if nom_item in g.panier:
        g.panier[nom_item] = min(g.panier[nom_item] + qte_int, stock_max)
    else:
        g.panier[nom_item] = qte_int 

    print(f"✅ Panier mis à jour : {nom_item} x{g.panier[nom_item]}")
    
    update_validation_button()
    relancer_nav_callback()

def update_validation_button():
    """Met à jour l'état du bouton ✓ en bas à droite."""
    if not hasattr(g, 'btn_valider') or g.btn_valider is None:
        return

    try:
        if len(g.panier) > 0:
            g.btn_valider.configure(state="normal", fg_color="#279727", text_color="white") 
        else:
            g.btn_valider.configure(state="disabled", fg_color="gray", text_color="white")
    except Exception:
        pass