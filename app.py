import streamlit as st
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from rembg import remove
import io
import google.generativeai as genai

# --- Configuration de la page ---
st.set_page_config(page_title="Studio Garage Dabireau", layout="wide", page_icon="🚗")

# --- Constantes ---
STUDIO_BG_COLOR = (235, 236, 240) # Gris clair studio
INFO_TEXT = "GARAGE DABIREAU - 25 Rue Alexandre Arnaud, 44120 Vertou - Tel. 02 40 34 21 04"

# --- Fonctions Utilitaires ---

def adjust_image(image, brightness, contrast):
    """Ajuste la luminosité et le contraste."""
    img = ImageEnhance.Brightness(image).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    return img

def process_studio_mode(image, logo=None):
    """Détoure la voiture et met le fond."""
    with st.spinner('Détourage intelligent en cours... (Patientez 10s)'):
        # 1. Détourage
        try:
            cutout = remove(image)
        except Exception as e:
            st.error(f"Erreur détourage : {e}")
            return image

        # 2. Création du fond studio
        background = Image.new("RGB", cutout.size, STUDIO_BG_COLOR)
        
        # 3. Collage
        background.paste(cutout, (0, 0), cutout)
        final_image = background

        # 4. Ajout Logo ou Texte
        W, H = final_image.size
        
        if logo:
            # Logo centré en haut
            logo_ratio = logo.width / logo.height
            new_w = int(W * 0.4) # 40% de la largeur
            new_h = int(new_w / logo_ratio)
            logo_resized = logo.resize((new_w, new_h))
            
            pos_x = (W - new_w) // 2
            pos_y = 20
            final_image.paste(logo_resized, (pos_x, pos_y), logo_resized)
        else:
            # Texte simple si pas de logo
            draw = ImageDraw.Draw(final_image)
            try:
                # Essai police système
                font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            # On écrit le texte grossièrement centré (méthode simple)
            draw.text((50, 50), INFO_TEXT, fill=(0, 0, 0))

        return final_image

# --- Interface ---

st.title("Studio Garage Dabireau 🚙")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Clé API Google Gemini", type="password")

# Uploads
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("1. Photo Véhicule", type=["jpg", "png", "jpeg"])
with col2:
    uploaded_logo = st.file_uploader("2. Logo (PNG Transparent)", type=["png"])

logo_img = None
if uploaded_logo:
    logo_img = Image.open(uploaded_logo).convert("RGBA")

if uploaded_file:
    original = Image.open(uploaded_file).convert("RGB")
    
    st.divider()
    
    # Réglages
    c1, c2 = st.columns(2)
    with c1: bright = st.slider("Luminosité", 0.5, 1.5, 1.0)
    with c2: cont = st.slider("Contraste", 0.5, 1.5, 1.0)
    
    img_adjusted = adjust_image(original, bright, cont)
    
    # Choix du mode
    mode = st.radio("Mode", ["Mode Studio (Fond Gris + Logo)", "Mode Simple (Photo d'origine)"])
    
    final_res = img_adjusted

    if mode == "Mode Studio (Fond Gris + Logo)":
        if st.button("Lancer le traitement magique ✨"):
            final_res = process_studio_mode(img_adjusted, logo_img)
            st.image(final_res, use_container_width=True)
    else:
        st.image(final_res, use_container_width=True)

    # Export
    st.divider()
    buf = io.BytesIO()
    final_res.save(buf, format="JPEG", quality=95)
    st.download_button("Télécharger la photo", data=buf.getvalue(), file_name="garage_dabireau.jpg", mime="image/jpeg")

    # IA Texte
    if api_key and st.button("Rédiger l'annonce avec IA"):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Tu es le Garage Dabireau (Vertou). Analyse cette photo. Rédige une annonce Leboncoin pro et vendeuse pour ce véhicule. Inclus les infos: {INFO_TEXT}"
        with st.spinner("Rédaction..."):
            res = model.generate_content([prompt, final_res])
            st.write(res.text)

else:
    st.info("Chargez une photo pour commencer.")
