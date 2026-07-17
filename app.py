import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuration de la page
st.set_page_config(page_title="Générateur de Révisions", page_icon="🎓", layout="centered")

# --- STYLE CSS POUR LES FLASHCARDS ---
st.markdown("""
    <style>
    .flashcard {
        background-color: #f0f2f6;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0px;
        border-left: 10px solid #ff4b4b;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Assistant de Révision IA")
st.write("Transformez vos photos de cours en QCM ou en Flashcards !")

# --- CONFIGURATION API ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets Streamlit.")
    st.stop()

# --- INTERFACE ---
tab1, tab2 = st.tabs(["📝 Mode QCM", "🗂️ Mode Flashcards"])

with st.sidebar:
    st.header("Paramètres")
    nb_items = st.slider("Nombre d'éléments à générer", 5, 20, 10)
    uploaded_files = st.file_uploader("Envoyez vos photos de cours", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# --- FONCTION DE GÉNÉRATION CORRIGÉE ---
def generer_contenu(fichiers, mode, quantite):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if mode == "QCM":
        prompt = f"Analyse ces images et crée un QCM de {quantite} questions. Format : Question, puis 4 options (A, B, C, D), puis la Bonne Réponse avec explication."
    else:
        prompt = f"Analyse ces images et crée {quantite} Flashcards de révision. Pour chaque flashcard, donne un Recto (Question/Concept) et un Verso (Réponse/Définition précise). Sois très synthétique."

    # On prépare la liste avec le texte d'abord
    contenu = [prompt]
    
    # On ouvre correctement chaque image avec PIL et on l'ajoute directement
    for f in fichiers:
        img = Image.open(f)
        contenu.append(img)
    
    # Génération
    response = model.generate_content(contenu)
    return response.text

# --- LOGIQUE ONGLET 1 : QCM ---
with tab1:
    if uploaded_files:
        if st.button("🚀 Créer le QCM"):
            with st.spinner("Analyse des images..."):
                try:
                    resultat = generer_contenu(uploaded_files, "QCM", nb_items)
                    st.markdown(resultat)
                except Exception as e:
                    st.error(f"Erreur lors de la génération : {e}")
    else:
        st.info("Veuillez charger des images dans la barre latérale.")

# --- LOGIQUE ONGLET 2 : FLASHCARDS ---
with tab2:
    if uploaded_files:
        if st.button("🗂️ Créer les Flashcards"):
            with st.spinner("Création des cartes..."):
                try:
                    resultat = generer_contenu(uploaded_files, "Flashcards", nb_items)
                    
                    lignes = resultat.split('\n')
                    for ligne in lignes:
                        if ligne.strip():
                            st.markdown(f'<div class="flashcard">{ligne}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erreur lors de la génération : {e}")
    else:
        st.info("Veuillez charger des images dans la barre latérale.")

st.sidebar.markdown("---")
st.sidebar.write(f"📸 {len(uploaded_files) if uploaded_files else 0} images prêtes.")
