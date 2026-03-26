# src/views/ecran_selection.py
import customtkinter as ctk
from src.models import globals as g
from tkinter import StringVar
from PIL import Image
import os

def ouvrir_selection_quantite(fenetre, nom_item, relancer_nav_callback):
    """
    Ouvre l'écran détaillé de sélection de quantité avec image et description dynamiques.
    """
    
    # --- CONFIGURATION FOND ---
    fenetre.configure(fg_color="white") # Force le fond en blanc pur

    # --- FONCTION DE NETTOYAGE ---
    def nettoyer_et_quitter():
        for widget in fenetre.winfo_children():
            widget.place_forget()
        relancer_nav_callback()

    for widget in fenetre.winfo_children():
        widget.place_forget()

    # --- GESTION DU TIMER ---
    def relancer_timer():
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        g.timer_id = fenetre.after(90000, nettoyer_et_quitter)

    relancer_timer()

    # --- LOGIQUE DE STOCK RÉEL ---
    stock_disponible = g.stocks.get(nom_item, 0)
    var_qte = StringVar(value="+ 2") 
    qte_interne = 2

    def modifier_quantite(delta):
        nonlocal qte_interne
        nouvelle_qte = qte_interne + delta
        if 1 <= nouvelle_qte <= stock_disponible:
            qte_interne = nouvelle_qte
            var_qte.set(f"+ {qte_interne}")
            relancer_timer()

    # --- 1. HEADER (Titre + Bouton X) ---
    ctk.CTkLabel(
        fenetre, text=f"Configuration : {nom_item}", 
        font=("Segoe Print", 15, "bold"), text_color="black", anchor="w"
    ).place(x=20, y=20) 

    ctk.CTkButton(
        fenetre, text="✕", width=30, height=30, corner_radius=8,
        fg_color="#E74C3C", text_color="white", hover_color="#C0392B",
        font=("Arial", 14, "bold"), command=nettoyer_et_quitter
    ).place(x=350, y=15, anchor="ne") 

    # --- 2. LOGIQUE DYNAMIQUE (IMAGE & DESCRIPTION) ---
    base_path = r"C:\Users\loish\.vscode\SmartLock-IHM\assets\images"
    nom_item_upper = nom_item.upper()
    
    # Dictionnaire des descriptions
    DESCRIPTIONS = {
        "PLA": "Matériau idéal pour les objets esthétiques et la précision. Attention, il est fragile et se déforme au-delà de 60°C.",
        "PETG": "Combine facilité d'impression et haute résistance aux chocs. Parfait pour les pièces fonctionnelles solides et flexibles.",
        "ASA": "Matériau robuste résistant aux UV et aux intempéries. Idéal pour l'extérieur et les hautes températures, mais plus complexe à imprimer."
    }

    if "ASA" in nom_item_upper:
        fichier = "image_ASA.png"
        desc_text = DESCRIPTIONS["ASA"]
    elif "PETG" in nom_item_upper:
        fichier = "image_PETG.png"
        desc_text = DESCRIPTIONS["PETG"]
    else:
        fichier = "image_PLA.jpg" 
        desc_text = DESCRIPTIONS["PLA"]
    
    chemin_complet = os.path.join(base_path, fichier)
    
    try:
        img_pil = Image.open(chemin_complet)
        photo_item = ctk.CTkImage(light_image=img_pil, size=(140, 170))
    except Exception as e:
        print(f"Erreur : Impossible de charger {chemin_complet} -> {e}")
        photo_item = None

    # --- CADRE PHOTO CORRIGÉ (Blanc + Bordure douce) ---
    cadre_photo = ctk.CTkFrame(
        fenetre, width=150, height=180, corner_radius=15, 
        fg_color="white", border_width=1, border_color="#E0E0E0"
    )
    cadre_photo.place(x=20, y=85)

    if photo_item:
        ctk.CTkLabel(cadre_photo, image=photo_item, text="").place(relx=0.5, rely=0.5, anchor="center")
    else:
        ctk.CTkLabel(cadre_photo, text="photo", font=("Arial", 16, "italic"), text_color="gray30").place(relx=0.5, rely=0.5, anchor="center")

    # --- 3. SECTION DROITE (Infos + Boutons Gris) ---
    ctk.CTkLabel(fenetre, text=f"Reste : {stock_disponible} g", font=("Arial", 14, "bold"), text_color="black").place(x=190, y=95)
    ctk.CTkLabel(fenetre, text="Quantité :", font=("Arial", 14), text_color="black").place(x=190, y=130)

    # Cadre sélecteur transparent pour ne pas faire de tâche grise
    cadre_selecteur = ctk.CTkFrame(fenetre, width=130, height=50, corner_radius=10, fg_color="transparent")
    cadre_selecteur.place(x=190, y=160)

    ctk.CTkButton(
        cadre_selecteur, text="-", width=40, height=40, corner_radius=10,
        fg_color="#F2F2F2", text_color="black", hover_color="#CCCCCC", # Gris très clair
        font=("Arial", 18, "bold"), command=lambda: modifier_quantite(-1)
    ).place(x=0, y=5)

    ctk.CTkLabel(cadre_selecteur, textvariable=var_qte, width=40, font=("Arial", 16, "bold"), text_color="black").place(x=45, y=5)

    ctk.CTkButton(
        cadre_selecteur, text="+", width=40, height=40, corner_radius=10,
        fg_color="#F2F2F2", text_color="black", hover_color="#CCCCCC", # Gris très clair
        font=("Arial", 18, "bold"), command=lambda: modifier_quantite(1)
    ).place(x=90, y=5)

    # --- 4. SECTION DESCRIPTION (Dynamique) ---
    label_desc = ctk.CTkLabel(
        fenetre, 
        text=f"Propriétés : {desc_text}", 
        font=("Arial", 14), 
        text_color="black", 
        wraplength=340, 
        justify="left"
    )
    label_desc.place(x=20, y=290)

    # --- LOGIQUE ALERTE UNIQUE ---
    alerte_envoyee = False

    def declencher_alerte():
        nonlocal alerte_envoyee
        if not alerte_envoyee:
            alerte_envoyee = True
            cadre_notif = ctk.CTkFrame(fenetre, width=320, height=40, corner_radius=8, fg_color="#777777")
            cadre_notif.place(relx=0.5, y=380, anchor="n") 
            
            ctk.CTkLabel(
                cadre_notif, text="✅ Alerte envoyée", 
                font=("Arial", 12, "bold"), text_color="white"
            ).place(relx=0.5, rely=0.5, anchor="center")
            
            btn_alerte.configure(state="disabled", fg_color="#BDC3C7", text="Alerte effectuée")

    # --- 5. LOGIQUE VALIDATION ---
    def valider():
        if 0 < qte_interne <= stock_disponible:
            g.panier[nom_item] = g.panier.get(nom_item, 0) + qte_interne
            from src.logic.inventory_logic import update_validation_button
            update_validation_button()
            nettoyer_et_quitter()

    # --- 6. BOUTONS BAS ---
    btn_alerte = ctk.CTkButton(
        fenetre, text="⚠️ Alerte stock ⚠️", width=150, height=45, corner_radius=15,
        fg_color="#E9F904", hover_color="#D4E404", text_color="black",
        font=("Arial", 14, "bold"), command=declencher_alerte
    )
    btn_alerte.place(x=20, y=465)

    btn_confirmer = ctk.CTkButton(
        fenetre, text="Ajouter au Panier", width=150, height=45, corner_radius=15,
        fg_color="#2ECC71", hover_color="#27AE60", text_color="black",
        font=("Arial", 14, "bold"), command=valider
    )
    btn_confirmer.place(x=190, y=465)