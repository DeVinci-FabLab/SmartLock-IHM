import customtkinter as ctk
from src.models import globals as g
from src.logic.timer_manager import reset_inactivite
from src.logic.api_service import signaler_erreur_stock
from tkinter import StringVar
from PIL import Image
import os

def ouvrir_ecran_selection(fenetre, nom_item, relancer_nav_callback):
    fenetre.configure(fg_color="white")
    W, H = g.SW, g.SH

    def nettoyer_et_quitter():
        for widget in fenetre.winfo_children():
            widget.destroy()
        relancer_nav_callback()

    for widget in fenetre.winfo_children():
        widget.place_forget()

    reset_inactivite(fenetre, nettoyer_et_quitter)

    stock_disponible = g.stocks.get(nom_item, 0)
    qte_interne = min(1, stock_disponible) if stock_disponible > 0 else 0
    var_qte = StringVar(value=f"+{qte_interne}")

    def modifier_quantite(delta):
        nonlocal qte_interne
        nouvelle_qte = qte_interne + delta
        if 1 <= nouvelle_qte <= stock_disponible:
            qte_interne = nouvelle_qte
            var_qte.set(f"+{qte_interne}")
            reset_inactivite(fenetre, nettoyer_et_quitter)

    fs = int(H * 0.020)
    fs_title = int(H * 0.024)

    # Image réduite — max 30% de W et 32% de H
    photo_w = int(W * 0.30)
    photo_h = int(H * 0.32)
    x_photo = int(W * 0.04)
    y_photo = int(H * 0.12)
    x_info  = int(W * 0.42)

    ctk.CTkLabel(
        fenetre, text=f"Configuration : {nom_item}",
        font=("Segoe Print", fs_title, "bold"), text_color="black"
    ).place(x=int(W * 0.04), y=int(H * 0.03))

    ctk.CTkButton(
        fenetre, text="✕",
        width=int(W * 0.09), height=int(H * 0.048),
        corner_radius=12, fg_color="#E74C3C", hover_color="#C0392B",
        text_color="white", font=("Arial", fs_title, "bold"),
        command=nettoyer_et_quitter
    ).place(x=int(W * 0.97), y=int(H * 0.025), anchor="ne")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    base_path = os.path.join(project_root, "assets", "images")

    DESCRIPTIONS = {
        "PLA": "Idéal pour les objets esthétiques. Fragile au-delà de 60°C.",
        "PETG": "Haute résistance aux chocs. Parfait pour les pièces fonctionnelles.",
        "ASA": "Résistant aux UV et intempéries. Idéal pour l'extérieur.",
        "moteur": "Moteur pas à pas pour impression 3D.",
        "driver": "Driver de moteur pas à pas."
    }

    img_map = {
        "ASA": "image_ASA.png", "PETG": "image_PETG.png",
        "PLA": "image_PLA.jpg", "moteur": "moteur.png", "driver": "driver.png"
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
        photo_item = ctk.CTkImage(light_image=img_pil, size=(photo_w, photo_h))
    except:
        photo_item = None

    cadre_photo = ctk.CTkFrame(
        fenetre, width=photo_w + 16, height=photo_h + 16,
        corner_radius=12, fg_color="white", border_width=1, border_color="#E0E0E0"
    )
    cadre_photo.place(x=x_photo, y=y_photo)

    if photo_item:
        ctk.CTkLabel(cadre_photo, image=photo_item, text="").place(relx=0.5, rely=0.5, anchor="center")
    else:
        ctk.CTkLabel(cadre_photo, text="photo", font=("Arial", fs, "italic"), text_color="gray").place(relx=0.5, rely=0.5, anchor="center")

    unite = "g" if any(x in nom_item.upper() for x in ["PLA", "PETG", "ASA"]) else "pce"

    ctk.CTkLabel(
        fenetre, text=f"Reste : {stock_disponible} {unite}",
        font=("Arial", fs, "bold"), text_color="black"
    ).place(x=x_info, y=int(H * 0.14))

    ctk.CTkLabel(
        fenetre, text="Quantité :", font=("Arial", fs), text_color="black"
    ).place(x=x_info, y=int(H * 0.22))

    # Sélecteur contenu dans W - x_info - marge droite
    sel_w = int(W * 0.50)
    sel_h = int(H * 0.080)
    btn_sel = int(sel_w * 0.30)
    sel_w = btn_sel * 3 + 20

    cadre_selecteur = ctk.CTkFrame(fenetre, width=sel_w, height=sel_h, corner_radius=12, fg_color="#F2F2F2")
    cadre_selecteur.place(x=x_info - 10, y=int(H * 0.29))

    marge = (sel_w - btn_sel * 3) // 2
    ctk.CTkButton(
        cadre_selecteur, text="-", width=btn_sel, height=sel_h - 8,
        corner_radius=12, fg_color="#E0E0E0", hover_color="#CCCCCC",
        text_color="black", font=("Arial", int(H * 0.028), "bold"),
        command=lambda: modifier_quantite(-1)
    ).place(x=marge, y=4)
    ctk.CTkLabel(
        cadre_selecteur, textvariable=var_qte, width=btn_sel,
        font=("Arial", int(H * 0.024), "bold"), text_color="black"
    ).place(x=marge + btn_sel, y=4)
    ctk.CTkButton(
        cadre_selecteur, text="+", width=btn_sel, height=sel_h - 8,
        corner_radius=12, fg_color="#E0E0E0", hover_color="#CCCCCC",
        text_color="black", font=("Arial", int(H * 0.028), "bold"),
        command=lambda: modifier_quantite(1)
    ).place(x=marge + btn_sel * 2, y=4)

    # Description sous l'image et le sélecteur
    ctk.CTkLabel(
        fenetre, text=f"Propriétés : {desc_text}",
        font=("Arial", int(H * 0.018)), text_color="#444444",
        wraplength=int(W * 0.90), justify="left"
    ).place(x=int(W * 0.04), y=int(H * 0.49))

    btn_w = int(W * 0.40)
    btn_h = int(H * 0.068)

    def declencher_alerte():
        signaler_erreur_stock(nom_item)
        cadre_notif = ctk.CTkFrame(
            fenetre, width=int(W * 0.60), height=int(H * 0.06),
            corner_radius=12, fg_color="#444444"
        )
        cadre_notif.place(relx=0.5, rely=0.78, anchor="center")
        ctk.CTkLabel(
            cadre_notif, text="✅ Alerte envoyée",
            font=("Arial", fs, "bold"), text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")
        btn_alerte.configure(state="disabled", fg_color="#E0E0E0", text="Alerte effectuée", text_color="#888888")
        fenetre.after(3000, lambda: cadre_notif.destroy() if cadre_notif.winfo_exists() else None)

    def valider():
        if qte_interne > 0:
            from src.logic.inventory_logic import ajouter_au_panier
            ajouter_au_panier(nom_item, qte_interne, nettoyer_et_quitter)

    btn_alerte = ctk.CTkButton(
        fenetre, text="⚠️ Erreur Stock",
        width=btn_w, height=btn_h, corner_radius=12,
        fg_color="#E9F904", hover_color="#D4E404", text_color="black",
        font=("Arial", fs, "bold"), command=declencher_alerte
    )
    btn_alerte.place(x=int(W * 0.04), rely=0.94, anchor="sw")

    ctk.CTkButton(
        fenetre, text="Ajouter au Panier",
        width=btn_w, height=btn_h, corner_radius=12,
        fg_color="#2ECC71", hover_color="#27AE60", text_color="white",
        font=("Arial", fs, "bold"), command=valider,
        state="normal" if stock_disponible > 0 else "disabled"
    ).place(x=int(W * 0.54), rely=0.94, anchor="sw")