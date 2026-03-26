# src/logic/inventory_logic.py
from src.models import globals as g

def toggle_selection(bouton, item_name, fenetre, revenir_callback):
    if item_name in g.panier:
        del g.panier[item_name]
        bouton.configure(fg_color="#D3D3D3")
    else:

        g.panier[item_name] = 1
        bouton.configure(fg_color="#7CDD81") 
    
    update_validation_button()

    # --- LOGIQUE DE TIMER ---
    if g.timer_id:
        fenetre.after_cancel(g.timer_id) 
    
    g.timer_id = fenetre.after(90000, revenir_callback)
    print(f"Panier actuel : {g.panier}")
    print("Chrono Navigation réinitialisé (90s) !")

def ajouter_au_panier(nom_item, quantite, relancer_nav_callback):
    try:
        qte_int = int(quantite)
        if qte_int <= 0: return
    except ValueError:
        return 

    if nom_item in g.panier:
        g.panier[nom_item] += qte_int 
        print(f"Mise à jour : {nom_item} maintenant à {g.panier[nom_item]}")
    else:
        g.panier[nom_item] = qte_int 
        print(f"Nouvel ajout : {nom_item} x{qte_int}")

    update_validation_button()
    relancer_nav_callback()

def update_validation_button():

    if not g.btn_valider:
        return

    if len(g.panier) > 0:
        g.btn_valider.configure(state="normal", fg_color="#279727") 
    else:
        g.btn_valider.configure(state="disabled", fg_color="gray")