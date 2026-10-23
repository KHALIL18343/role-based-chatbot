"""Chatbot avec rôle et mémoire, adapté du notebook 35."""
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

PERSONAS = {
    "Brief": {
        "description": "Answers as briefly and concisely as possible.",
        "system": "You always answer as briefly and concisely as possible.",
    },
    "Curious": {
        "description": "Explores ideas and asks thoughtful follow-up questions.",
        "system": "You are incredibly curious. Respond with thoughtful reflections and a relevant follow-up question that playfully explores the subject.",
    },
    "Vocabulary-rich": {
        "description": "Uses advanced and uncommon vocabulary.",
        "system": "You respond using challenging and often under-utilized vocabulary words, even when your response could be made more simply. Keep answers accurate and understandable.",
    },
}

class ChatbotWithRole:
    def __init__(self, llm, system_message=""):
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_message),
            MessagesPlaceholder(variable_name="chat_conversation"),
        ])
        self.chat_chain = self.prompt | llm | StrOutputParser()
        self.chat_conversation = []

    def chat(self, prompt):
        if not prompt.strip():
            raise ValueError("Le message ne doit pas être vide.")
        user_message = HumanMessage(content=prompt.strip())
        # Conserver uniquement les échanges réussis dans la mémoire.
        response = self.chat_chain.invoke({
            "chat_conversation": [*self.chat_conversation, user_message]
        })
        if not response.strip():
            raise ValueError("Le modèle n'a retourné aucune réponse textuelle.")
        self.chat_conversation.extend([user_message, AIMessage(content=response)])
        return response

    def clear(self):
        self.chat_conversation.clear()

def create_chatbot(api_key, model, persona):
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(
        model=model, api_key=api_key, vertexai=False,
        temperature=1.0, timeout=60, max_retries=1,
    )
    system_message = PERSONAS[persona]["system"] + (
        " Respond in the user's language unless they request another language."
    )
    return ChatbotWithRole(llm, system_message)

