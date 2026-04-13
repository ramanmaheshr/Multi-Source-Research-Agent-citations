from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel
from .config import get_settings

import logging 

logger = logging.getLogger(__name__)


def get_llm(temperature:float = 0.0) -> BaseChatModel:
    settings = get_settings()
    if settings.use_ollama:
        try:
            llm = ChatOllama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=temperature
            )
            #quick health check 
            llm.invoke("hi")
            logger.info("Ollama connection successful")
            return llm
        except Exception as e:
            logging.warning(f"Ollama connection failed: {e} Switching to Groq")
    
    #fallback to groq
    return ChatGroq(
        model=settings.groq_model,
        temperature=temperature,
        api_key=settings.groq_api_key
    )

def get_embed_model():
    from langchain_ollama.embeddings import OllamaEmbeddings
    s=get_settings()
    return OllamaEmbeddings(
        model=s.embed_model,
        base_url=s.ollama_base_url
    )
    