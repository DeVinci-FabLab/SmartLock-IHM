import customtkinter as ctk
from src.models import globals as g
from tkinter import StringVar
from PIL import Image
import os

def ouvrir_ecran_selection(fenetre, nom_item, relancer_nav_callback):
    """
    Écran détaillé pour choisir la quantité avec bouton d'alerte erreur stock.
    """
    
    # --- CONFIGURATION FOND ---
    fenetre.configure(fg_color="white") 

    def nettoyer_et_quitter():
        for widget in fenetre.winfo_children():
            widget.destroy()
        relancer_nav_callback()

    for widget in fenetre.winfo_children():
        widget.place_forget()

    # --- GESTION DU TIMER ---
    def relancer_timer():
        if g.timer_id:
            fenetre.after_cancel(g.timer_id)
        g.timer_id = fenetre.after(90000, nettoyer_et_quitter)

    relancer_timer()

    # --- LOGIQUE DE STOCK ---
    stock_disponible = g.stocks.get(nom_item, 0)
    qte_interne = min(1, stock_disponible) if stock_disponible > 0 else 0
    var_qte = StringVar(value=f"{qte_interne}") 

    def modifier_quantite(delta):
        nonlocal qte_interne
        nouvelle_qte = qte_interne + delta
        if 1 <= nouvelle_qte <= stock_disponible:
            qte_interne = nouvelle_qte
            var_qte.set(f"{qte_interne}")
            relancer_timer()

    # --- 1. HEADER ---
    ctk.CTkLabel(fenetre, text=f"Sélection : {nom_item}", font=("Segoe Print", 16, "bold"), text_color="black").place(x=20, y=20) 
    ctk.CTkButton(fenetre, text="✕", width=35, height=35, fg_color="#E74C3C", text_color="white", corner_radius=8, command=nettoyer_et_quitter).place(x=350, y=15, anchor="ne") 

    # --- 2. LOGIQUE DYNAMIQUE (IMAGES & DESCRIPTIONS) ---
    current_dir = os.path.dirname(os.path.abspath(__file__)) 
    project_root = os.path.dirname(os.path.dirname(current_dir))
    base_path = os.path.join(project_root, "assets", "images")
    
    DESCRIPTIONS = {
        "PLA": "Idéal pour l'esthétique. Se déforme au-delà de 60°C.",
        "PETG": "Résistant et fonctionnel. Bonne adhérence entre couches.",
        "ASA": "Ultra-résistant aux UV. Parfait pour l'extérieur.",
        "moteur": "Moteur pas à pas haute précision pour vos axes NEMA.",
        "driver": "Contrôleur de moteur (driver) pour imprimante 3D.",
        "Item 1": "Description personnalisée pour l'objet 1.",
        "Item 2": "Description personnalisée pour l'objet 2.",
        "Item 3": "Description personnalisée pour l'objet 3."
    }

    img_map = {
        "ASA": "image_ASA.png", "PETG": "image_PETG.png", "PLA": "image_PLA.jpg",
        "moteur": "moteur.png", "driver": "driver.png"
    }
    
    fichier = "placeholder.png"
    for key in img_map:
        if key.upper() in nom_item.upper():
            fichier = img_map[key]
            break

    desc_text = "Pas de description disponible."
    for key in DESCRIPTIONS:
        if key.upper() in nom_item.upper():
            desc_text = DESCRIPTIONS[key]
            break

    try:
        img_pil = Image.open(os.path.join(base_path, fichier))
        photo_item = ctk.CTkImage(light_image=img_pil, size=(140, 150))
    except:
        photo_item = None

    # --- CADRE PHOTO ---
    cadre = ctk.CTkFrame(fenetre, width=150, height=160, fg_color="white", border_width=1, border_color="#E0E0E0")
    cadre.place(x=20, y=80)
    if photo_item:
        ctk.CTkLabel(cadre, image=photo_item, text="").place(relx=0.5, rely=0.5, anchor="center")
    else:
        ctk.CTkLabel(cadre, text="Image n/a", text_color="gray").place(relx=0.5, rely=0.5, anchor="center")

    # --- 3. SÉLECTEUR DE QUANTITÉ ---
    unite = "g" if any(x in nom_item.upper() for x in ["PLA", "PETG", "ASA"]) else "pce"
    ctk.CTkLabel(fenetre, text=f"Stock : {stock_disponible} {unite}", font=("Arial", 14, "bold"), text_color="#2C3E50").place(x=185, y=85)
    
    cadre_qte = ctk.CTkFrame(fenetre, width=140, height=45, fg_color="#F2F2F2", corner_radius=10)
    cadre_qte.place(x=185, y=120)

    ctk.CTkButton(cadre_qte, text="-", width=35, height=35, command=lambda: modifier_quantite(-1), fg_color="white", text_color="black", font=("Arial", 18, "bold")).place(x=5, y=5)
    ctk.CTkLabel(cadre_qte, textvariable=var_qte, font=("Arial", 16, "bold"), text_color="black").place(x=55, y=5)
    ctk.CTkButton(cadre_qte, text="+", width=35, height=35, command=lambda: modifier_quantite(1), fg_color="white", text_color="black", font=("Arial", 18, "bold")).place(x=100, y=5)

    # --- 4. DESCRIPTION ---
    ctk.CTkLabel(fenetre, text=f"Note : {desc_text}", font=("Arial", 12, "italic"), text_color="#555555", wraplength=320, justify="left").place(x=20, y=260)

    # --- 5. BOUTONS ACTIONS---
    def declencher_alerte():
        print(f"⚠️ ALERTE : Stock faux signalé pour {nom_item} par {g.utilisateur_actuel}")
        
        btn_alerte.configure(state="disabled", text="Signalé ✓", fg_color="#BDC3C7", text_color="white")
        
        lbl_msg = ctk.CTkLabel(fenetre, text="Erreur signalée à l'administrateur.", 
                               font=("Arial", 11, "bold"), text_color="#E67E22")
        lbl_msg.place(relx=0.5, y=440, anchor="center")
        
        fenetre.after(3000, lambda: lbl_msg.destroy() if lbl_msg.winfo_exists() else None)

    def valider():
        if qte_interne > 0:
            from src.logic.inventory_logic import ajouter_au_panier
            ajouter_au_panier(nom_item, qte_interne, nettoyer_et_quitter)

    btn_alerte = ctk.CTkButton(
        fenetre, text="⚠️ Erreur Stock", width=155, height=50, corner_radius=12,
        fg_color="#E9F904", hover_color="#D4E404", text_color="black",
        font=("Arial", 13, "bold"), command=declencher_alerte
    )
    btn_alerte.place(x=20, y=470)

    btn_confirmer = ctk.CTkButton(
        fenetre, text="Ajouter au Panier", width=155, height=50, corner_radius=12,
        fg_color="#2ECC71", hover_color="#27AE60", text_color="white",
        font=("Arial", 13, "bold"), command=valider,
        state="normal" if stock_disponible > 0 else "disabled"
    )
    btn_confirmer.place(x=185, y=470)