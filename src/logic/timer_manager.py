from src.models import globals as g

def reset_inactivite(fenetre, callback, duree_ms=90000):
    if g.timer_id:
        fenetre.after_cancel(g.timer_id)
    g.timer_id = fenetre.after(duree_ms, callback)