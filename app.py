import streamlit as st
import requests
import tempfile

from pipeline_act import pipeline  
                               


#                 CONFIG INTERFACE


st.set_page_config(
    page_title="Music Speech Translator",
    page_icon="🎧",
    layout="wide",
)

st.markdown("""
    <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            color: #1f3b4d;
        }

        .sub {
            font-size: 18px;
            text-align: center;
            color: #555;
            margin-bottom: 25px;
        }

        .block {
            padding: 20px;
            background: #f6f8fa;
            border-radius: 12px;
            margin-top: 10px;
            font-size: 17px;
        }

        .stButton>button {
            border-radius: 10px;
            background-color: #1f3b4d;
            color: white;
            font-size: 18px;
            padding: 8px 20px;
        }
    </style>
""", unsafe_allow_html=True)


#                     TITRE


st.markdown("<div class='title'>🎵 Music Speech Translator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Transcription + Traduction automatique des paroles d’une musique</div>", unsafe_allow_html=True)

#        UPLOAD OU TÉLÉCHARGEMENT VIA URL


tab1, tab2 = st.tabs(["💻", "🌐"])
audio_path = None
with tab1:
    file = st.file_uploader("Importer un fichier audio", type=["mp3", "wav", "m4a"])
    if file:
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=file.name)
        temp.write(file.read())
        temp.close()
        st.session_state["audio_path"] = temp.name  # <-- ici


with tab2:
    url = st.text_input("Entrez une URL directe d’un fichier audio")
    if url:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                temp.write(r.content)
                temp.close()
                st.session_state["audio_path"] = temp.name  # <-- ici
                st.success("✔️ Fichier téléchargé")
            else:
                st.error("❌ Impossible de télécharger le fichier")
        except:
            st.error("❌ Erreur lors du téléchargement")




#     CHOIX DE LA LANGUE DE TRADUCTION


langue_cible = st.selectbox(
    "Langue de traduction",
    ["Français", "Anglais", "Espagnol", "Allemand", "Italien", "Portugais"],
)

# Récupération du chemin enregistré
audio_path = st.session_state.get("audio_path", None)

#     mise en forme du bouton copier

#               BOUTON DE LANCEMENT


if audio_path and st.button("Traduire"):
    with st.spinner("Analyse de la musique…"):

        texte, traduction = pipeline(audio_path, langue_cible)


    #          AFFICHAGE STYLE GOOGLE TRADUCTION
    





############################################################
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎤 Paroles détectées")
        st.markdown("<div class='block'>" + texte.replace("\n", "<br>") + "</div>", unsafe_allow_html=True)
        

    with col2:
        st.markdown(f"###  Traduction en {langue_cible}")
        traduction_html = traduction.replace("\n", "<br>")
        st.markdown(f"<div class='block'>{traduction_html}</div>", unsafe_allow_html=True)
        
        
         
    st.success("Analyse terminée.")
