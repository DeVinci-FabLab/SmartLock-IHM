import customtkinter as ctk
from src.models import globals as g
from src.logic.timer_manager import reset_inactivite

def ouvrir_vue_panier(fenetre, relancer_nav_callback):
    def auto_logout():
        for widget in fenetre.winfo_children():
            widget.destroy()
        relancer_nav_callback()

    reset_inactivite(fenetre, auto_logout)

    for widget in fenetre.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        fenetre, text="Récapitulatif Panier",
        font=("Segoe Print", 18, "bold"), text_color="black"
    ).place(relx=0.5, y=35, anchor="center")

    ctk.CTkFrame(fenetre, height=2, width=320, fg_color="#E0E0E0").place(relx=0.5, y=60, anchor="center")

    g.cadre_liste = ctk.CTkScrollableFrame(
        fenetre, width=300, height=330,
        fg_color="#FDFDFD", border_width=1, border_color="#E0E0E0",
        label_text="Articles sélectionnés",
        label_font=("Arial", 12, "bold"),
        scrollbar_button_color="#D0D0D0",
        scrollbar_button_hover_color="#A0A0A0"
    )
    g.cadre_liste.place(relx=0.5, y=205, anchor="center")

    if not g.panier:
        ctk.CTkLabel(
            g.cadre_liste, text="Votre panier est vide...",
            font=("Arial", 13, "italic"), text_color="gray"
        ).pack(pady=110)
    else:
        for item, quantite in g.panier.items():
            ctk.CTkLabel(
                g.cadre_liste, text=f"• {item}  ×{quantite}",
                font=("Arial", 13), text_color="black", anchor="w"
            ).pack(fill="x", padx=10, pady=5)

    def quitter_panier():
        for widget in fenetre.winfo_children():
            widget.destroy()
        relancer_nav_callback()

    g.btn_retour_panier = ctk.CTkButton(
        fenetre, text="← Continuer la sélection", width=250, height=45,
        corner_radius=12, fg_color="#B9E9FF", hover_color="#7BBFE0",
        text_color="black", font=("Arial", 12, "bold"),
        command=quitter_panier
    )
    g.btn_retour_panier.place(relx=0.5, y=455, anchor="center")

    if g.panier:
        ctk.CTkButton(
            fenetre, text="Vider le panier", width=180, height=38,
            corner_radius=12, fg_color="#FFD1D1", hover_color="#E89595",
            text_color="#C0392B", font=("Arial", 11, "bold"),
            command=lambda: [g.panier.clear(), ouvrir_vue_panier(fenetre, relancer_nav_callback)]
        ).place(relx=0.5, y=505, anchor="center")