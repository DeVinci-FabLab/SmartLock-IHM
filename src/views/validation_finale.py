import customtkinter as ctk
from src.models import globals as g
from src.logic.api_service import enregistrer_transaction
from src.logic.timer_manager import reset_inactivite

def ouvrir_validation_finale(fenetre, relancer_nav_callback):
    fenetre.configure(fg_color="white")

    def auto_logout_validation():
        for widget in fenetre.winfo_children():
            widget.destroy()
        relancer_nav_callback()

    for widget in fenetre.winfo_children():
        widget.destroy()

    for nom in list(g.panier.keys()):
        stock_max = g.stocks.get(nom, 0)
        if g.panier[nom] > stock_max:
            g.panier[nom] = stock_max

    reset_inactivite(fenetre, auto_logout_validation)

    ctk.CTkLabel(
        fenetre, text="Validation de la sélection",
        font=("Segoe Print", 16, "bold"), text_color="black"
    ).place(relx=0.5, y=35, anchor="center")
    ctk.CTkFrame(fenetre, height=2, width=320, fg_color="#E0E0E0").place(relx=0.5, y=60, anchor="center")

    scroll_container = ctk.CTkScrollableFrame(
        fenetre, width=350, height=330, fg_color="transparent",
        scrollbar_button_color="#D0D0D0",
        scrollbar_button_hover_color="#A0A0A0"
    )
    scroll_container.place(relx=0.5, y=245, anchor="center")

    g.dict_widgets_panier = {}

    def dessiner_un_article(nom_article, index_ligne):
        if nom_article in g.dict_widgets_panier:
            try:
                g.dict_widgets_panier[nom_article].destroy()
            except:
                pass

        qte_choisie = g.panier.get(nom_article, 0)
        stock_actuel = g.stocks.get(nom_article, 0)

        item_frame = ctk.CTkFrame(
            scroll_container, fg_color="white", corner_radius=12,
            border_width=1, border_color="#E0E0E0"
        )
        item_frame.grid(row=index_ligne, column=0, sticky="ew", pady=6, padx=5)
        scroll_container.grid_columnconfigure(0, weight=1)

        g.dict_widgets_panier[nom_article] = item_frame

        inner_container = ctk.CTkFrame(item_frame, fg_color="transparent")
        inner_container.pack(fill="x", padx=10, pady=10)

        ligne_haut = ctk.CTkFrame(inner_container, fg_color="transparent")
        ligne_haut.pack(fill="x")

        ctk.CTkButton(
            ligne_haut, text="🗑", width=32, height=32,
            corner_radius=12, fg_color="#FFD1D1", hover_color="#E89595",
            text_color="#E74C3C", font=("Arial", 16),
            command=lambda: supprimer_article(nom_article)
        ).pack(side="left")

        ctk.CTkLabel(
            ligne_haut, text=nom_article,
            fg_color="#F2F2F2", corner_radius=8,
            width=155, height=32, text_color="black",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=5)

        btn_frame = ctk.CTkFrame(ligne_haut, fg_color="#F2F2F2", corner_radius=12)
        btn_frame.pack(side="right")

        def modif_qty(n, delta, idx):
            reset_inactivite(fenetre, auto_logout_validation)
            stock_max = g.stocks.get(n, 0)
            nouveau_total = g.panier[n] + delta
            if delta > 0 and nouveau_total > stock_max:
                return
            g.panier[n] = nouveau_total
            if g.panier[n] <= 0:
                supprimer_article(n)
            else:
                dessiner_un_article(n, idx)

        ctk.CTkButton(
            btn_frame, text="-", width=38, height=38,
            corner_radius=12, fg_color="transparent", hover_color="#E0E0E0",
            text_color="black", font=("Arial", 16, "bold"),
            command=lambda: modif_qty(nom_article, -1, index_ligne)
        ).pack(side="left")

        color_plus = "#AAAAAA" if qte_choisie >= stock_actuel else "black"
        ctk.CTkButton(
            btn_frame, text="+", width=38, height=38,
            corner_radius=12, fg_color="transparent", hover_color="#E0E0E0",
            text_color=color_plus, font=("Arial", 16, "bold"),
            command=lambda: modif_qty(nom_article, 1, index_ligne)
        ).pack(side="right")

        infos_frame = ctk.CTkFrame(inner_container, fg_color="transparent")
        infos_frame.pack(fill="x", padx=35)

        color_qte = "#E74C3C" if qte_choisie >= stock_actuel else "#555555"
        ctk.CTkLabel(
            infos_frame, text=f"Quantité : {qte_choisie}",
            font=("Arial", 10, "bold"), text_color=color_qte
        ).pack(anchor="w")
        ctk.CTkLabel(
            infos_frame, text=f"Stock total : {stock_actuel}",
            font=("Arial", 10), text_color="#555555"
        ).pack(anchor="w")

    def supprimer_article(nom):
        if nom in g.panier:
            del g.panier[nom]
            rafraichir_tout()

    def rafraichir_tout():
        for widget in scroll_container.winfo_children():
            widget.destroy()
        g.dict_widgets_panier.clear()
        if not g.panier:
            ctk.CTkLabel(
                scroll_container, text="Le panier est vide",
                font=("Arial", 13), text_color="gray"
            ).pack(pady=50)
        else:
            for i, nom in enumerate(sorted(g.panier.keys())):
                dessiner_un_article(nom, i)

    rafraichir_tout()

    ctk.CTkButton(
        fenetre, text="✖ Annuler", width=150, height=45, corner_radius=12,
        fg_color="#E74C3C", hover_color="#C0392B", text_color="white",
        font=("Arial", 13, "bold"), command=relancer_nav_callback
    ).place(x=20, y=475)

    def action_valider():
        if g.panier:
            reussite = enregistrer_transaction(g.panier)
            if reussite:
                print("Transaction envoyée à l'API avec succès.")
            else:
                print("⚠️ Erreur lors de l'enregistrement de la transaction.")
        try:
            from src.views.acces_physique import ouvrir_ecran_physique
            if g.timer_id:
                fenetre.after_cancel(g.timer_id)
            ouvrir_ecran_physique(fenetre, relancer_nav_callback)
        except ImportError:
            print("⚠️ Erreur : src.views.acces_physique introuvable.")

    ctk.CTkButton(
        fenetre, text="Valider & Ouvrir", width=150, height=45, corner_radius=12,
        fg_color="#2ECC71", hover_color="#27AE60", text_color="white",
        font=("Arial", 13, "bold"), command=action_valider
    ).place(x=190, y=475)