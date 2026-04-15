import customtkinter as ctk
from src.models import globals as g
from src.logic.timer_manager import reset_inactivite

def ouvrir_vue_panier(fenetre, relancer_nav_callback):
    W, H = g.SW, g.SH
    fs = int(H * 0.019)
    fs_title = int(H * 0.027)

    def auto_logout():
        for widget in fenetre.winfo_children():
            widget.destroy()
        relancer_nav_callback()

    reset_inactivite(fenetre, auto_logout)

    for widget in fenetre.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        fenetre, text="Récapitulatif Panier",
        font=("Segoe Print", fs_title, "bold"), text_color="black"
    ).place(relx=0.5, rely=0.03, anchor="center")

    ctk.CTkFrame(fenetre, height=2, width=int(W * 0.88), fg_color="#E0E0E0").place(relx=0.5, rely=0.10, anchor="center")

    g.cadre_liste = ctk.CTkScrollableFrame(
        fenetre, width=int(W * 0.86), height=int(H * 0.52),
        fg_color="#FDFDFD", border_width=1, border_color="#E0E0E0",
        label_text="Articles sélectionnés",
        label_font=("Arial", fs, "bold"),
        scrollbar_button_color="#D0D0D0",
        scrollbar_button_hover_color="#A0A0A0"
    )
    g.cadre_liste.place(relx=0.5, rely=0.42, anchor="center")

    if not g.panier:
        ctk.CTkLabel(
            g.cadre_liste, text="Votre panier est vide...",
            font=("Arial", fs, "italic"), text_color="gray"
        ).pack(pady=int(H * 0.15))
    else:
        for item, quantite in g.panier.items():
            ctk.CTkLabel(
                g.cadre_liste, text=f"• {item}  ×{quantite}",
                font=("Arial", fs), text_color="black", anchor="w"
            ).pack(fill="x", padx=10, pady=5)

    def quitter_panier():
        for widget in fenetre.winfo_children():
            widget.destroy()
        relancer_nav_callback()

    g.btn_retour_panier = ctk.CTkButton(
        fenetre, text="← Continuer la sélection",
        width=int(W * 0.60), height=int(H * 0.062),
        corner_radius=12, fg_color="#B9E9FF", hover_color="#7BBFE0",
        text_color="black", font=("Arial", fs, "bold"),
        command=quitter_panier
    )
    g.btn_retour_panier.place(relx=0.5, rely=0.82, anchor="center")

    if g.panier:
        ctk.CTkButton(
            fenetre, text="Vider le panier",
            width=int(W * 0.50), height=int(H * 0.055),
            corner_radius=12, fg_color="#FFD1D1", hover_color="#E89595",
            text_color="#C0392B", font=("Arial", fs, "bold"),
            command=lambda: [g.panier.clear(), ouvrir_vue_panier(fenetre, relancer_nav_callback)]
        ).place(relx=0.5, rely=0.92, anchor="center")