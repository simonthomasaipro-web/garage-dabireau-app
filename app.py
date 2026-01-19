import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import io
import google.generativeai as genai

# Configuration simple
st.set_page_config(page_title="Studio Dabireau", layout="wide")

st.title("🚗 Studio Garage Dabireau")

# Sidebar - Réglages
with st.sidebar:
    st.header("1. Configuration")
    api_key = st.text_input("Clé Gemini (Optionnel)", type="password")
    
    st.header("2. Réglages Photo")
    brightness = st.slider("Luminosité", 0.5, 1.5, 1.05)
    contrast = st.slider("Contraste", 0.5, 1.5, 1.05)

# Zone principale
col_upload, col_preview = st.columns([1, 2])

with col_upload:
    uploaded_file = st.file_uploader("📸 Charger la photo voiture", type=["jpg", "png", "jpeg"])
    uploaded_logo = st.file_uploader("🏢 Charger le Logo/Texte (PNG)", type=["png"])
    
    if uploaded_logo and uploaded_file:
        st.divider()
        st.subheader("Placement sur le bardage")
        
        # Outils de positionnement
        col_pos1, col_pos2 = st.columns(2)
        with col_pos1:
            x_pos = st.slider("Position Horizontal", 0, 100, 50)
            y_pos = st.slider("Position Vertical", 0, 100, 20)
        with col_pos2:
            size = st.slider("Taille du texte", 10, 100, 30)
            opacity = st.slider("Transparence (Réalisme)", 50, 100, 90)

# Logique de traitement
if uploaded_file:
    # 1. Chargement et Amélioration
    image = Image.open(uploaded_file).convert("RGB")
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)
    
    final_image = image.copy()
    W, H = image.size

    # 2. Incrustation du Logo sur le mur
    if uploaded_logo:
        logo = Image.open(uploaded_logo).convert("RGBA")
        
        # Redimensionnement
        target_width = int(W * (size / 100))
        ratio = target_width / logo.width
        target_height = int(logo.height * ratio)
        logo = logo.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Gestion Opacité (Pour que ça fasse vrai sur le métal)
        if opacity < 100:
            alpha = logo.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity / 100.0)
            logo.putalpha(alpha)
        
        # Positionnement
        px = int((W - target_width) * (x_pos / 100))
        py = int((H - target_height) * (y_pos / 100))
        
        # Collage
        final_image.paste(logo, (px, py), logo)

    # Affichage Grand Format
    with col_preview:
        st.image(final_image, use_container_width=True)
        
        # Bouton Télécharger
        buf = io.BytesIO()
        final_image.save(buf, format="JPEG", quality=95)
        st.download_button("⬇️ Télécharger Photo Finale", data=buf.getvalue(), file_name="dabireau_final.jpg", mime="image/jpeg", type="primary")

        # IA Gemini
        if api_key and st.button("✨ Rédiger annonce avec IA"):
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            with st.spinner("Rédaction en cours..."):
                try:
                    resp = model.generate_content(["Tu es vendeur auto. Rédige une annonce Leboncoin pour cette voiture. Garage Dabireau, Vertou.", final_image])
                    st.text_area("Annonce", resp.text, height=200)
                except:
                    st.error("Erreur IA")
