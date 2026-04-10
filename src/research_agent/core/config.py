from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    #LLM
    ollama_base_url:str = "http://localhost:11434"
    ollama_model:str = "qwen3.5:9b"
    groq_api_key:str = ''
    groq_model:str = "llama-3.3-70b-versatile"
    use_ollama:bool = True
    
    #search
    tavily_api_key:str
    max_sub_queries:int = 5
    tavily_max_results:int = 3
    
    #vector store
    faiss_index_path:str = "./data/faiss_index"
    embed_model:str = 'nomic-embed-text'
    #FastAPI
    api_host:str = '0.0.0.0'
    api_port:int = 8080

    #checkpointing
    sqlite_db_path:str = "./data/checkpoints.db"
    
    class Config:
        env_file = ".env"
    @lru_cache()
    def get_settings() -> "Settings":
        return Settings()
    
    