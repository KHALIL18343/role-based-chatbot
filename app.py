"""Interface Streamlit du projet Role-based Chatbot."""
import hashlib
import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from chatbot import PERSONAS, create_chatbot

load_dotenv(Path(__file__).with_name(".env"))
st.set_page_config(page_title="Role-based Chatbot", page_icon="💬", layout="centered")

def configured_value(name, default=""):
    value = os.getenv(name)
    if value:
        return value
    try:
        return str(st.secrets.get(name, default))
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return default

with st.sidebar:
    st.header("Configuration")
    entered_key = st.text_input("Google API key", type="password", key="api_key_input")
    api_key = entered_key.strip() or configured_value("GOOGLE_API_KEY") or configured_value("GEMINI_API_KEY")
    model = st.text_input("Gemini model", value=configured_value("GEMINI_MODEL", "gemini-3.7-flash")).strip()
    st.caption("La clé saisie reste dans cette session et n'est pas enregistrée dans un fichier.")
    st.link_button("Obtenir une clé Google AI Studio", "https://aistudio.google.com/apikey")

st.title("Role-based Chatbot (LangChain + Google Gemini)")
st.write("This app is a chatbot whose behavior changes according to a system message (role/persona).")
persona = st.selectbox("Choose a chatbot persona:", list(PERSONAS), index=2)
st.caption(PERSONAS[persona]["description"])

# Une instance par session. Changer de configuration réinitialise la mémoire.
configuration = (persona, model, hashlib.sha256(api_key.encode()).hexdigest())
if st.session_state.get("configuration") != configuration:
    st.session_state.configuration = configuration
    st.session_state.pop("chatbot", None)

if st.button("Clear conversation"):
    if "chatbot" in st.session_state:
        st.session_state.chatbot.clear()

if not api_key:
    st.info("Ajoute ta clé API Google dans la barre latérale pour commencer.")
elif not model:
    st.warning("Indique le nom d'un modèle Gemini dans la barre latérale.")
elif "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = create_chatbot(api_key, model, persona)
    except Exception:
        st.error("Impossible de configurer Gemini. Vérifie la clé et le nom du modèle.")

bot = st.session_state.get("chatbot")
if bot:
    for message in bot.chat_conversation:
        role = "user" if message.type == "human" else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)

prompt = st.chat_input("Type your message here...", disabled=bot is None)
if prompt and prompt.strip() and bot:
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        with st.spinner("Gemini prépare sa réponse..."):
            answer = bot.chat(prompt)
        with st.chat_message("assistant"):
            st.markdown(answer)
    except Exception:
        # Pas d'exception brute : elle pourrait contenir des détails sensibles.
        st.error(
            "La réponse n'a pas pu être générée. Vérifie ta connexion, ta clé API, "
            "le modèle et ton quota Google. Ce message n'a pas été ajouté à la mémoire ; "
            "tu peux le renvoyer."
        )

