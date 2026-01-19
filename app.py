import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="Studio Dabireau (Gemini 3)", layout="wide", page_icon="🍌")

# Texte par défaut
DEFAULT_PROMPT = """
Agis comme un expert retoucheur photo automobile.
Tu reçois une photo de voiture.
TA MISSION :
1. Garde la voiture EXACTEMENT comme elle est (ne la modifie pas).
2. Sur le mur en arrière-plan (bardage métallique), intègre de manière ultra-réaliste le texte suivant :
"GARAGE DABIREAU
25 Rue Alexandre Arnaud
44120 Vertou
Tel. 02 40 34 21 04"

CONTRAINTES :
- Le texte doit suivre la perspective du mur.
- Le texte doit avoir l'air peint ou collé sur le métal (légers reflets, texture).
- Si tu changes l'environnement, garde un style "Parking Pro" ou "Studio Industriel".
"""

st.title("🍌 Studio Dabireau - Moteur IA")

# --- SIDEBAR ---
with st.sidebar:
    st.header("1. Connexion")
    api_key = st.text_input("Clé API Gemini", type="password")
    
    st.header("2. Modèle IA")
    # J'ai mis le nom exact de ton screenshot, mais c'est modifiable si ça change
    model_name = st.text_input("Nom du Modèle", value="gemini-3-pro-image-preview")
    
    st.divider()
    
    st.header("3. Réglages Créatifs")
    environment = st.selectbox("Ambiance", ["Intégration Naturelle (Mur actuel)", "Studio Gris Pro", "Extérieur Ensoleillé"])
    
    # Le Seed permet de figer le style
    seed_enable = st.checkbox("Figer le style (Seed)?")
    seed_val = st.number_input("Numéro du Seed", value=42, step=1) if seed_enable else None

# --- ZONE PRINCIPALE ---
col_left, col_right = st.columns(2)

uploaded_file = None

with col_left:
    st.subheader("📸 Photo Originale")
    uploaded_file = st.file_uploader("Charger la voiture", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image_input = Image.open(uploaded_file)
        st.image(image_input, use_container_width=True)

with col_right:
    st.subheader("✨ Résultat IA")
    
    if uploaded_file and api_key:
        if st.button("Lancer la Génération (Nano Banana)", type="primary"):
            
            genai.configure(api_key=api_key)
            
            # Construction du prompt final
            final_prompt = DEFAULT_PROMPT
            if environment == "Studio Gris Pro":
                final_prompt += "\nCHANGE L'ARRIERE PLAN pour un mur gris neutre style studio photo propre."
            elif environment == "Extérieur Ensoleillé":
                final_prompt += "\nAjoute une lumière solaire chaleureuse et naturelle."
            
            try:
                with st.spinner("L'IA travaille... (Cela peut prendre 10-20 secondes)"):
                    # Configuration du modèle
                    # Note : La configuration exacte dépend de la version de la librairie google-generativeai
                    # Pour la version preview image, on envoie image + prompt
                    model = genai.GenerativeModel(model_name)
                    
                    # Appel API
                    response = model.generate_content([final_prompt, image_input])
                    
                    # Affichage
                    # Gemini peut renvoyer plusieurs formats, on cherche l'image
                    try:
                        # Si l'API renvoie une image directement dans parts
                        img_data = response.parts[0].inline_data
                        image_result = Image.open(io.BytesIO(img_data.data))
                        st.image(image_result, use_container_width=True)
                        
                        # Bouton DL
                        buf = io.BytesIO()
                        image_result.save(buf, format="JPEG", quality=95)
                        st.download_button("Télécharger", buf.getvalue(), "dabireau_ia.jpg", "image/jpeg")
                        
                    except Exception as parse_error:
                        # Parfois le modèle refuse et renvoie du texte (sécurité ou erreur)
                        st.warning("L'IA a renvoyé du texte au lieu d'une image (vérifiez le modèle) :")
                        st.write(response.text)
                        
            except Exception as e:
                st.error(f"Erreur API : {e}")
                st.info("Vérifiez que votre clé API a bien accès au modèle 'gemini-3-pro-image-preview'. Sinon essayez 'gemini-2.0-flash-exp'.")

    elif not api_key:
        st.info("Entrez votre clé API à gauche pour commencer.")
