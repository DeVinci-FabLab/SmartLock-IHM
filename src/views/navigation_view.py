import customtkinter as ctk
from src.models import globals as g
from src.logic.inventory_logic import update_validation_button
from src.logic.timer_manager import reset_inactivite
from src.views.ecran_selection import ouvrir_ecran_selection
from src.views.vue_panier import ouvrir_vue_panier
from src.views.validation_finale import ouvrir_validation_finale

COLS = 2  # articles par ligne dans chaque catégorie


def ecran_navigation(fenetre, revenir_callback, fermer_callback):
    fenetre.configure(fg_color="white")
    for widget in fenetre.winfo_children():
        widget.destroy()

    W, H = g.SW, g.SH
    fs = int(H * 0.019)
    fs_title = int(H * 0.023)
    fs_cat = int(H * 0.021)

    def auto_logout():
        for widget in fenetre.winfo_children():
            widget.destroy()
        revenir_callback()

    def rafraichir():
        ecran_navigation(fenetre, revenir_callback, fermer_callback)

    def aller_a_validation():
        if not g.panier:
            return
        for widget in fenetre.winfo_children():
            widget.destroy()
        ouvrir_validation_finale(fenetre, rafraichir)

    # ── Header ────────────────────────────────────────────────────────────────
    header_h = int(H * 0.09)
    header = ctk.CTkFrame(fenetre, fg_color="white", height=header_h)
    header.place(x=0, y=0, relwidth=1)
    header.pack_propagate(False)

    g.titre_nav = ctk.CTkLabel(
        header, text=f"Bienvenue {g.utilisateur_actuel} !",
        font=("Segoe Print", fs_title, "bold"), text_color="black"
    )
    g.titre_nav.pack(side="left", padx=int(W * 0.04))

    g.btn_retour = ctk.CTkButton(
        header, text="Quitter",
        width=int(W * 0.22), height=int(H * 0.048),
        corner_radius=12, fg_color="#E74C3C", hover_color="#C0392B",
        text_color="white", font=("Arial", fs, "bold"),
        command=auto_logout
    )
    g.btn_retour.pack(side="right", padx=int(W * 0.03))

    ctk.CTkFrame(fenetre, height=2, fg_color="#E0E0E0").place(x=0, y=header_h, relwidth=1)

    # ── Footer ────────────────────────────────────────────────────────────────
    footer_h = int(H * 0.11)
    footer_y = H - footer_h
    footer = ctk.CTkFrame(fenetre, fg_color="white", height=footer_h)
    footer.place(x=0, y=footer_y, relwidth=1)
    footer.pack_propagate(False)

    ctk.CTkFrame(fenetre, height=2, fg_color="#E0E0E0").place(x=0, y=footer_y - 2, relwidth=1)

    g.btn_voir_panier = ctk.CTkButton(
        footer, text="Panier",
        width=int(W * 0.45), height=int(H * 0.075),
        corner_radius=12, fg_color="#E9F904", hover_color="#D4E404",
        text_color="black", font=("Arial", int(H * 0.022), "bold"),
        command=lambda: ouvrir_vue_panier(fenetre, rafraichir)
    )
    g.btn_voir_panier.pack(side="left", padx=int(W * 0.04), pady=int(H * 0.015))

    btn_val_size = int(H * 0.075)
    g.btn_valider = ctk.CTkButton(
        footer, text="OK",
        font=("Arial", int(btn_val_size * 0.5), "bold"),
        width=btn_val_size, height=btn_val_size,
        corner_radius=btn_val_size // 2,
        fg_color="gray", state="disabled",
        text_color="white", command=aller_a_validation
    )
    g.btn_valider.pack(side="right", padx=int(W * 0.04))

    # ── Contenu scrollable ────────────────────────────────────────────────────
    content_y = header_h + 4
    content_h = footer_y - content_y - 4

    scroll = ctk.CTkScrollableFrame(
        fenetre,
        width=W - 20,
        height=content_h,
        fg_color="white",
        scrollbar_button_color="#D0D0D0",
        scrollbar_button_hover_color="#A0A0A0",
    )
    scroll.place(x=0, y=content_y)

    btn_w = int((W - int(W * 0.08)) / COLS) - int(W * 0.02)
    btn_h = int(H * 0.09)

    categories = g.categories_items
    if not categories:
        ctk.CTkLabel(
            scroll, text="Aucun article disponible",
            font=("Arial", fs), text_color="gray"
        ).pack(pady=int(H * 0.1))
    else:
        for cat_name, items in categories.items():
            # Label catégorie
            ctk.CTkLabel(
                scroll, text=cat_name,
                font=("Segoe Print", fs_cat, "bold"), text_color="black",
                anchor="w"
            ).pack(fill="x", padx=int(W * 0.04), pady=(int(H * 0.02), int(H * 0.005)))

            ctk.CTkFrame(scroll, height=1, fg_color="#E0E0E0").pack(
                fill="x", padx=int(W * 0.04), pady=(0, int(H * 0.01))
            )

            # Grille d'articles
            row_frame = None
            for idx, item_name in enumerate(items):
                if idx % COLS == 0:
                    row_frame = ctk.CTkFrame(scroll, fg_color="transparent")
                    row_frame.pack(fill="x", padx=int(W * 0.03), pady=int(H * 0.005))

                stock = g.stocks.get(item_name, 0)
                threshold = g.items_threshold.get(item_name)
                is_low = threshold is not None and 0 < stock < threshold
                in_cart = item_name in g.panier and g.panier[item_name] > 0
                state = "normal" if stock > 0 else "disabled"
                if in_cart:
                    fg, hover, tc = "#2ECC71", "#27AE60", "white"
                elif is_low:
                    fg, hover, tc = "#F39C12", "#D68910", "white"
                else:
                    fg, hover, tc = "#F2F2F2", "#E0E0E0", "black"
                if stock == 0:
                    label = f"{item_name}\n(Vide)"
                elif is_low:
                    label = f"{item_name}\n(Stock bas)"
                else:
                    label = item_name

                btn = ctk.CTkButton(
                    row_frame, text=label,
                    width=btn_w, height=btn_h,
                    corner_radius=12,
                    fg_color=fg, hover_color=hover, text_color=tc,
                    border_width=1, border_color="#E0E0E0",
                    state=state, font=("Arial", fs, "bold"),
                )
                btn.configure(command=lambda n=item_name: (
                    ouvrir_ecran_selection(fenetre, n, rafraichir)
                ))
                btn.pack(side="left", padx=int(W * 0.01))

            # Espace entre catégories
            ctk.CTkFrame(scroll, height=int(H * 0.01), fg_color="transparent").pack()

    update_validation_button()
    reset_inactivite(fenetre, auto_logout)
