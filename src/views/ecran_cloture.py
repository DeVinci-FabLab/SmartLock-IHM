import customtkinter as ctk
from src.models import globals as g

def ouvrir_ecran_cloture(fenetre, relancer_nav_callback):
    fenetre.configure(fg_color="white")
    
    motif_selectionne = ctk.StringVar(value="")

    for widget in fenetre.winfo_children():
        widget.destroy()

    def fermer_application():
        """Réinitialise la session et retourne à l'écran de Badgeage."""
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
        """Relance l'écran d'accès physique pour déverrouiller à nouveau."""
        from src.views.acces_physique import ouvrir_ecran_physique
        ouvrir_ecran_physique(fenetre, relancer_nav_callback)

    def retourner_a_la_selection():
        """Retourne à l'écran de validation finale (panier)."""
        from src.views.validation_finale import ouvrir_validation_finale
        for widget in fenetre.winfo_children():
            widget.destroy()
        ouvrir_validation_finale(fenetre, relancer_nav_callback)

    # --- HEADER ---
    header = ctk.CTkFrame(fenetre, fg_color="transparent", height=60)
    header.pack(fill="x", padx=20, pady=(10, 0))
    
    ctk.CTkLabel(
        header, 
        text=f"👤 À bientôt {g.utilisateur_actuel} !", 
        font=("Segoe Print", 18, "bold"), 
        text_color="black"
    ).pack(side="left", padx=10)
    
    ctk.CTkFrame(fenetre, height=2, fg_color="#EEEEEE").pack(fill="x", padx=20, pady=(0, 20))

    # --- QUESTION PRINCIPALE ---
    cadre_question = ctk.CTkFrame(fenetre, width=340, height=140, corner_radius=20, fg_color="#F8F9FA", border_width=1, border_color="#E0E0E0")
    cadre_question.place(relx=0.5, y=140, anchor="center")
    cadre_question.pack_propagate(False)

    ctk.CTkLabel(cadre_question, text="Tout s'est bien passé ?", font=("Arial", 16, "bold"), text_color="black").pack(pady=(15, 5))

    btn_frame = ctk.CTkFrame(cadre_question, fg_color="transparent")
    btn_frame.pack(expand=True)

    ctk.CTkButton(
        btn_frame, text="Oui, parfait", fg_color="#7CDD81", hover_color="#5EB563", text_color="black", 
        width=130, height=50, font=("Arial", 14, "bold"), corner_radius=12,
        command=fermer_application
    ).pack(side="left", padx=10)

    g.cadre_feedback = None

    def afficher_feedback():
        if g.cadre_feedback:
            return

        g.cadre_feedback = ctk.CTkFrame(fenetre, width=340, height=360, corner_radius=20, fg_color="white", border_width=1, border_color="#D1D1D1")
        g.cadre_feedback.place(relx=0.5, y=400, anchor="center")
        g.cadre_feedback.pack_propagate(False)

        ctk.CTkLabel(g.cadre_feedback, text="Signaler un problème :", font=("Arial", 14, "bold"), text_color="#2C3E50").pack(pady=(15, 10))
        
        btns_motifs = []
        
        def select_motif(m, btn_source):
            motif_selectionne.set(m)
            if "redirection" in m.lower():
                retourner_a_la_selection()
                return

            for b in btns_motifs:
                b.configure(fg_color="white", text_color="black")
            btn_source.configure(fg_color="#3498DB", text_color="white")

        motifs = [
            "Porte restée bloquée", 
            "Quantité en stock fausse", 
            "Matériel endommagé", 
            "⚠️ Redirection vers panier"
        ]
        
        for m in motifs:
            is_redir = "redirection" in m.lower()
            txt_color = "#D35400" if is_redir else "black" 
            
            btn = ctk.CTkButton(
                g.cadre_feedback, text=m, fg_color="white", text_color=txt_color, 
                border_width=1, border_color="#D1D1D1", height=40, 
                font=("Arial", 11, "bold" if is_redir else "normal")
            )
            
            btn.configure(command=lambda val=m, b=btn: select_motif(val, b))
            btn.pack(fill="x", padx=20, pady=4)
            btns_motifs.append(btn)

        # BOUTONS D'ACTION (Réouvrir / Envoyer)
        action_container = ctk.CTkFrame(g.cadre_feedback, fg_color="transparent", width=300, height=60)
        action_container.pack(pady=20)

        ctk.CTkButton(
            action_container, text="Réouvrir", fg_color="#B9E9FF", text_color="black", 
            width=120, height=45, font=("Arial", 11, "bold"), 
            command=reouvrir_armoire
        ).pack(side="left", padx=5)

        def envoyer_et_quitter():
            if motif_selectionne.get():
                print(f"REPORT [{g.utilisateur_actuel}]: {motif_selectionne.get()}")
                fermer_application()
            else:
                print("⚠️ Veuillez sélectionner un motif.")

        ctk.CTkButton(
            action_container, text="Envoyer", fg_color="#2ECC71", text_color="white", 
            width=120, height=45, font=("Arial", 12, "bold"), 
            command=envoyer_et_quitter
        ).pack(side="left", padx=5)

    ctk.CTkButton(
        btn_frame, text="Non...", fg_color="#FFD1D1", hover_color="#E89595", text_color="black", 
        width=130, height=50, font=("Arial", 14, "bold"), corner_radius=12,
        command=afficher_feedback
    ).pack(side="left", padx=10)