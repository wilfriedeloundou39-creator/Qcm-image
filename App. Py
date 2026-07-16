import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# Configuration de la page Streamlit
st.set_page_config(page_title="Générateur de QCM par Photo", page_icon="📝", layout="centered")

# --- CONFIGURATION DE L'API GEMINI ---
# Remplacez par votre clé API ou configurez-la dans les secrets d'environnement
API_KEY = st.sidebar.text_input("Entrez votre clé API Gemini", type="password")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.sidebar.warning("Veuillez saisir votre clé API Google Gemini pour faire fonctionner l'application.")

st.title("📸 Générateur automatique de QCM")
st.write("Téléchargez la photo d'un cours ou d'un document, et l'IA va générer un QCM complet instantanément !")

# Paramètres de génération
num_questions = st.slider("Nombre de questions à générer :", min_value=1, max_value=10, value=3)

# --- ZONE D'IMPORTATION DE L'IMAGE ---
uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Affichage de l'image importée
    image = Image.open(uploaded_file)
    st.image(image, caption="Image importée", use_container_width=True)
    
    if st.button("🚀 Générer le QCM"):
        if not API_KEY:
            st.error("Veuillez d'abord configurer votre clé API dans la barre latérale.")
        else:
            with st.spinner("Analyse de l'image et création des questions en cours..."):
                try:
                    # Initialisation du modèle multimodal de Gemini
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Prompt strict pour obtenir un format JSON propre et structuré
                    prompt = f"""
                    Analyse cette image contenant du texte éducatif ou scientifique.
                    Génère exactement {num_questions} questions à choix multiples (QCM) basées uniquement sur les informations présentes dans l'image.
                    
                    Fournis ta réponse UNIQUEMENT sous la forme d'un tableau JSON valide, sans balises de code Markdown (pas de ```json), respectant strictement la structure suivante :
                    [
                      {{
                        "question": "Texte de la question ?",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "reponse_correcte": "L'option exacte copiée mot pour mot",
                        "explication": "Brève explication de pourquoi cette réponse est correcte."
                      }}
                    ]
                    """
                    
                    # Appel de l'API avec l'image et le texte de consigne
                    response = model.generate_content([prompt, image])
                    
                    # Nettoyage et chargement du JSON généré
                    raw_text = response.text.strip()
                    # Parfois le modèle peut ajouter des délimiteurs de bloc de code qu'on retire par sécurité :
                    if raw_text.startswith("```"):
                        raw_text = raw_text.split("\n", 1)[1].rsplit("\n", 1)[0]
                    
                    qcm_data = json.loads(raw_text)
                    
                    # Enregistrement dans la session Streamlit pour l'affichage interactif
                    st.session_state["qcm"] = qcm_data
                    st.success("QCM généré avec succès !")
                    
                except Exception as e:
                    st.error(f"Une erreur est survenue lors de la génération : {e}")

# --- AFFICHAGE INTERACTIF DU QCM ---
if "qcm" in st.session_state:
    st.write("---")
    st.header("📝 Testez vos connaissances :")
    
    qcm = st.session_state["qcm"]
    user_answers = {}
    
    for idx, q in enumerate(qcm):
        st.subheader(f"Question {idx + 1} : {q['question']}")
        # Affichage des choix sous forme de boutons radio
        user_answers[idx] = st.radio(
            "Sélectionnez votre réponse :",
            options=q['options'],
            key=f"q_{idx}"
        )
        st.write("") # Espace visuel
        
    if st.button("Validate vos réponses 🎯"):
        score = 0
        st.write("---")
        st.header("📊 Résultats :")
        
        for idx, q in enumerate(qcm):
            selected = user_answers[idx]
            correct = q['reponse_correcte']
            
            if selected == correct:
                score += 1
                st.success(f"**Question {idx + 1} : Correct !** 🎉\n\n*Votre réponse : {selected}*")
            else:
                st.error(f"**Question {idx + 1} : Incorrect.** ❌\n\n*Votre réponse : {selected}*\n\n*La bonne réponse était : **{correct}***")
            
            st.info(f"💡 **Explication :** {q['explication']}")
            st.write("---")
            
        st.metric(label="Votre Score Final", value=f"{score} / {len(qcm)}")
