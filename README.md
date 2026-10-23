# Projet 3 — Role-based Chatbot

Application Streamlit utilisant LangChain et Google Gemini, réalisée à partir de l'exercice **Enable Role-based Chatbots** du notebook 35 et des captures du devoir.

## Fonctionnalités
- Trois personnalités : **Brief**, **Curious**, **Vocabulary-rich**.
- Message système distinct pour chaque personnalité.
- Historique utilisateur/assistant conservé pendant la session.
- Bouton **Clear conversation** pour effacer la mémoire.
- Changer de rôle, de modèle ou de clé démarre une nouvelle conversation.
- Réponses dans la langue de l'utilisateur ; interface principale en anglais comme la capture.
- Clé masquée et gestion des erreurs API.

## Installation Windows
Prérequis : Python 3.11 ou plus récent et Internet. Si la commande Python ne fonctionne pas, installer Python depuis https://www.python.org/downloads/ avec l'option « Add Python to PATH ».

Tu peux double-cliquer sur **installer.bat**, puis sur **lancer.bat**. Sinon, ouvrir un terminal **dans ce dossier**, puis exécuter :
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```
Ouvrir l'adresse indiquée par Streamlit, généralement http://localhost:8501.
Ensuite, double-cliquer sur **lancer.bat** pour les lancements suivants.

## Clé Gemini
Créer une clé dans [Google AI Studio](https://aistudio.google.com/apikey), puis la saisir dans la barre latérale. Ne pas joindre cette clé au devoir.

Option : copier `.env.example` vers `.env` et compléter `GOOGLE_API_KEY`. Les variables d'environnement et les secrets Streamlit sont aussi pris en charge. `GEMINI_API_KEY` est accepté comme alternative.
Le modèle est modifiable dans l'interface ou via `GEMINI_MODEL` ; sa disponibilité et les quotas dépendent du compte Google.

## Code et explication pour la présentation
- `app.py` : interface, clé et session Streamlit.
- `chatbot.py` : personnalités et classe `ChatbotWithRole`.
- `requirements.txt` : dépendances.
- `.streamlit/config.toml` : thème sombre.
- `tests/` : tests sans appel à Google.

Le menu choisit un **message système** (notebook 33). `MessagesPlaceholder` insère l'historique dans `ChatPromptTemplate` (notebook 35). La chaîne `prompt | llm | StrOutputParser()` produit la réponse. Les échanges sont des `HumanMessage` et `AIMessage` (notebook 31). `st.session_state` conserve le chatbot entre les réexécutions de Streamlit. `clear()` efface l'historique en conservant le rôle.

Le notebook d'origine utilise NVIDIA et Gradio ; ce projet utilise Gemini et Streamlit conformément au devoir. Les modules du cours `videos` et `chat_helpers` ne sont pas nécessaires.

La mémoire n'est pas enregistrée sur disque. Une nouvelle session la réinitialise. Tout l'historique est renvoyé au modèle : une conversation très longue peut dépasser ses limites. Le message système oriente le style sans le garantir parfaitement.

## Démonstration
1. Choisir **Brief** et envoyer « Bonjour, je m'appelle Amine ».
2. Demander « Quel est mon prénom ? » pour vérifier la mémoire.
3. Effacer la conversation, puis poser à nouveau la question : le prénom n'est plus dans le contexte.
4. Comparer « Explique l'intelligence artificielle » avec les trois rôles.

## Tests sans clé API
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
Ces tests utilisent un modèle simulé ; ils ne valident pas le service Google ni la qualité réelle des réponses Gemini.

## Références
- [Intégration Gemini officielle LangChain](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai)
- [Tests Streamlit](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest)


