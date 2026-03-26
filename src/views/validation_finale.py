import customtkinter as ctk
from src.models import globals as g

def ouvrir_validation_finale(fenetre, relancer_nav_callback):
    fenetre.configure(fg_color="white")

    def auto_logout_validation():
        for widget in fenetre.winfo_children():
            widget.destroy()
        relancer_nav_callback()

    def relancer_timer():
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        g.timer_id = fenetre.after(90000, auto_logout_validation)

    relancer_timer()

    for widget in fenetre.winfo_children():
        widget.destroy()

    # --- SÉCURITÉ ANTI-DÉPASSEMENT ---
    # On vérifie chaque item du panier avant l'affichage
    for nom in list(g.panier.keys()):
        stock_max = g.stocks.get(nom, 0)
        if g.panier[nom] > stock_max:
            g.panier[nom] = stock_max  

    # --- HEADER ---
    ctk.CTkLabel(fenetre, text="Validation de la sélection", font=("Segoe Print", 18, "bold"), text_color="black").place(relx=0.5, y=35, anchor="center")
    ctk.CTkFrame(fenetre, height=2, width=300, fg_color="#EEEEEE").place(relx=0.5, y=60, anchor="center")

    # --- ZONE SCROLLABLE (MODIFIÉE) ---
    scroll_container = ctk.CTkScrollableFrame(
        fenetre, 
        width=350, 
        height=330, 
        fg_color="transparent",
        scrollbar_button_color="#D0D0D0",      
        scrollbar_button_hover_color="#A0A0A0" 
    )
    scroll_container.place(relx=0.5, y=245, anchor="center")

    g.dict_widgets_panier = {}

    def dessiner_un_article(nom_article, index_ligne):
        if nom_article in g.dict_widgets_panier:
            g.dict_widgets_panier[nom_article].destroy()

        qte_choisie = g.panier.get(nom_article, 0)
        stock_actuel = g.stocks.get(nom_article, 0)

        item_frame = ctk.CTkFrame(scroll_container, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E0E0")
        item_frame.grid(row=index_ligne, column=0, sticky="ew", pady=8, padx=5)
        scroll_container.grid_columnconfigure(0, weight=1)
        
        g.dict_widgets_panier[nom_article] = item_frame

        inner_container = ctk.CTkFrame(item_frame, fg_color="transparent")
        inner_container.pack(fill="x", padx=10, pady=10)

        ligne_haut = ctk.CTkFrame(inner_container, fg_color="transparent")
        ligne_haut.pack(fill="x")

        ctk.CTkButton(ligne_haut, text="🗑", width=30, height=30, fg_color="transparent", text_color="#E74C3C", font=("Arial", 18),
                      command=lambda: supprimer_article(nom_article)).pack(side="left")

        ctk.CTkLabel(ligne_haut, text=nom_article, fg_color="#F8F8F8", corner_radius=10, width=155, height=35, text_color="black", font=("Arial", 11, "bold")).pack(side="left", padx=5)

        btn_frame = ctk.CTkFrame(ligne_haut, fg_color="#F2F2F2", corner_radius=10)
        btn_frame.pack(side="right")

        def modif_qty(n, delta, idx):
            relancer_timer()
            stock_max = g.stocks.get(n, 0)
            nouveau_total = g.panier[n] + delta
            
            if delta > 0 and nouveau_total > stock_max:
                return 
            
            g.panier[n] = nouveau_total
            if g.panier[n] <= 0: 
                supprimer_article(n)
            else: 
                dessiner_un_article(n, idx)

        # Boutons de modification
        ctk.CTkButton(btn_frame, text="-", width=40, height=40, fg_color="transparent", text_color="black", 
                      command=lambda: modif_qty(nom_article, -1, index_ligne)).pack(side="left")
        
        color_plus = "gray" if qte_choisie >= stock_actuel else "black"
        ctk.CTkButton(btn_frame, text="+", width=40, height=40, fg_color="transparent", text_color=color_plus, 
                      command=lambda: modif_qty(nom_article, 1, index_ligne)).pack(side="right")

        infos_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        infos_frame.pack(fill="x", padx=35)
        
        color_qte = "#E74C3C" if qte_choisie >= stock_actuel else "#555555"
        
        ctk.CTkLabel(infos_frame, text=f"Quantité : {qte_choisie}", font=("Arial", 10, "bold"), text_color=color_qte).pack(anchor="w")
        ctk.CTkLabel(infos_frame, text=f"Stock total : {stock_actuel}", font=("Arial", 10), text_color="#2C3E50").pack(anchor="w")

    def supprimer_article(nom):
        if nom in g.panier:
            del g.panier[nom]
            rafraichir_tout()

    def rafraichir_tout():
        for widget in scroll_container.winfo_children():
            widget.destroy()
        g.dict_widgets_panier.clear()
        
        if not g.panier:
            ctk.CTkLabel(scroll_container, text="Le panier est vide", font=("Arial", 14), text_color="gray").pack(pady=50)
        else:
            items_tries = sorted(g.panier.keys())
            for i, nom in enumerate(items_tries):
                dessiner_un_article(nom, i)

    rafraichir_tout()

    # --- BOUTONS NAVIGATION ---
    ctk.CTkButton(fenetre, text="✖ Annuler", width=150, height=45, corner_radius=15, fg_color="#E74C3C", font=("Arial", 14, "bold"),
                  command=relancer_nav_callback).place(x=20, y=475)

    def action_valider():
        from src.views.acces_physique import ouvrir_ecran_physique
        if g.timer_id: fenetre.after_cancel(g.timer_id)
        ouvrir_ecran_physique(fenetre, relancer_nav_callback)

    ctk.CTkButton(fenetre, text="Valider & Ouvrir", width=150, height=45, corner_radius=15, fg_color="#2ECC71", text_color="black", font=("Arial", 14, "bold"),
                  command=action_valider).place(x=190, y=475)