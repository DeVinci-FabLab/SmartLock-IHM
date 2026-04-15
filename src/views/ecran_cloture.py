import customtkinter as ctk
from src.models import globals as g

def ouvrir_ecran_cloture(fenetre, relancer_nav_callback):
    fenetre.configure(fg_color="white")
    W, H = g.SW, g.SH
    fs = int(H * 0.019)
    fs_title = int(H * 0.025)

    motif_selectionne = ctk.StringVar(value="")

    for widget in fenetre.winfo_children():
        widget.destroy()

    def fermer_application():
        print(f"Session de {g.utilisateur_actuel} terminée. Nettoyage...")
        g.panier = {}
        g.utilisateur_actuel = "Utilisateur"
        if g.timer_id:
            try:
                fenetre.after_cancel(g.timer_id)
            except:
                pass
            g.timer_id = None
        for widget in fenetre.winfo_children():
            widget.destroy()
        from src.views.home_view import setup_home_screen
        setup_home_screen(fenetre)

    def reouvrir_armoire():
        from src.views.acces_physique import ouvrir_ecran_physique
        ouvrir_ecran_physique(fenetre, relancer_nav_callback)

    def retourner_a_la_selection():
        from src.views.validation_finale import ouvrir_validation_finale
        for widget in fenetre.winfo_children():
            widget.destroy()
        ouvrir_validation_finale(fenetre, relancer_nav_callback)

    header = ctk.CTkFrame(fenetre, fg_color="transparent", height=int(H * 0.09))
    header.pack(fill="x", padx=int(W * 0.05), pady=(int(H * 0.02), 0))

    ctk.CTkLabel(
        header, text=f"👤 À bientôt {g.utilisateur_actuel} !",
        font=("Segoe Print", fs_title, "bold"), text_color="black"
    ).pack(side="left")

    ctk.CTkFrame(fenetre, height=2, fg_color="#E0E0E0").pack(fill="x", padx=int(W * 0.05), pady=(0, int(H * 0.02)))

    cadre_w = int(W * 0.86)
    cadre_h = int(H * 0.22)
    btn_w = int(W * 0.36)
    btn_h = int(H * 0.068)

    cadre_question = ctk.CTkFrame(
        fenetre, width=cadre_w, height=cadre_h, corner_radius=12,
        fg_color="#F8F9FA", border_width=1, border_color="#E0E0E0"
    )
    cadre_question.place(relx=0.5, rely=0.24, anchor="center")
    cadre_question.pack_propagate(False)

    ctk.CTkLabel(
        cadre_question, text="Tout s'est bien passé ?",
        font=("Arial", fs_title, "bold"), text_color="black"
    ).pack(pady=(int(H * 0.018), int(H * 0.008)))

    btn_frame = ctk.CTkFrame(cadre_question, fg_color="transparent")
    btn_frame.pack(expand=True)

    ctk.CTkButton(
        btn_frame, text="Oui, parfait",
        fg_color="#2ECC71", hover_color="#27AE60", text_color="white",
        width=btn_w, height=btn_h, corner_radius=12,
        font=("Arial", fs, "bold"), command=fermer_application
    ).pack(side="left", padx=int(W * 0.02))

    g.cadre_feedback = None

    def afficher_feedback():
        if g.cadre_feedback:
            return

        fb_w = int(W * 0.86)
        fb_h = int(H * 0.60)

        g.cadre_feedback = ctk.CTkFrame(
            fenetre, width=fb_w, height=fb_h, corner_radius=12,
            fg_color="white", border_width=1, border_color="#E0E0E0"
        )
        g.cadre_feedback.place(relx=0.5, rely=0.45, anchor="n")
        g.cadre_feedback.pack_propagate(False)

        ctk.CTkLabel(
            g.cadre_feedback, text="Signaler un problème :",
            font=("Arial", fs, "bold"), text_color="black"
        ).pack(pady=(int(H * 0.015), int(H * 0.008)))

        btns_motifs = []

        def select_motif(m, btn_source):
            motif_selectionne.set(m)
            if "redirection" in m.lower():
                retourner_a_la_selection()
                return
            for b in btns_motifs:
                b.configure(fg_color="#F2F2F2", text_color="black")
            btn_source.configure(fg_color="#2ECC71", text_color="white")

        motifs = [
            "Porte restée bloquée",
            "Quantité en stock fausse",
            "Matériel endommagé",
            "⚠️ Redirection vers panier"
        ]

        for m in motifs:
            is_redir = "redirection" in m.lower()
            txt_color = "#E74C3C" if is_redir else "black"
            btn = ctk.CTkButton(
                g.cadre_feedback, text=m,
                fg_color="#F2F2F2", hover_color="#E0E0E0",
                text_color=txt_color, border_width=1, border_color="#E0E0E0",
                height=int(H * 0.055), corner_radius=12,
                font=("Arial", fs, "bold" if is_redir else "normal")
            )
            btn.configure(command=lambda val=m, b=btn: select_motif(val, b))
            btn.pack(fill="x", padx=int(W * 0.04), pady=int(H * 0.005))
            btns_motifs.append(btn)

        action_container = ctk.CTkFrame(g.cadre_feedback, fg_color="transparent")
        action_container.pack(pady=int(H * 0.015))

        ctk.CTkButton(
            action_container, text="Réouvrir",
            fg_color="#B9E9FF", hover_color="#7BBFE0", text_color="black",
            width=int(W * 0.36), height=btn_h, corner_radius=12,
            font=("Arial", fs, "bold"), command=reouvrir_armoire
        ).pack(side="left", padx=int(W * 0.02))

        def envoyer_et_quitter():
            if motif_selectionne.get():
                print(f"REPORT [{g.utilisateur_actuel}]: {motif_selectionne.get()}")
                fermer_application()
            else:
                print("⚠️ Veuillez sélectionner un motif.")

        ctk.CTkButton(
            action_container, text="Envoyer",
            fg_color="#2ECC71", hover_color="#27AE60", text_color="white",
            width=int(W * 0.36), height=btn_h, corner_radius=12,
            font=("Arial", fs, "bold"), command=envoyer_et_quitter
        ).pack(side="left", padx=int(W * 0.02))

    ctk.CTkButton(
        btn_frame, text="Non...",
        fg_color="#FFD1D1", hover_color="#E89595", text_color="#C0392B",
        width=btn_w, height=btn_h, corner_radius=12,
        font=("Arial", fs, "bold"), command=afficher_feedback
    ).pack(side="left", padx=int(W * 0.02))