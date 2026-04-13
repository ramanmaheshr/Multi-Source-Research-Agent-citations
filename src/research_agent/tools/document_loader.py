import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from ..core.llm import get_embed_model
from ..core.config import get_settings


SPLITTER  = RecursiveCharacterTextSplitter(
    chunk_size=800,chunk_overlap=120, length_function=len
)

def ingest_documents(doc_dir:str) -> FAISS:
    docs = []
    for p in Path(doc_dir).rglob("*"):
        if p.suffix == ".pdf":
            loader = PyPDFLoader(str(p))
        elif p.suffix in (".txt",".md"):
            loader = TextLoader(str(p))
        else:
            continue
        docs.extend(loader.load())
        chunks = SPLITTER.split_documents(docs)
        vectorstore = FAISS.from_documents(chunks, get_embed_model())
        vectorstore.save_local(get_settings().faiss_index_path)
        return vectorstore
def load_vector_store() -> FAISS:
    s = get_settings()
    if not Path(s.faiss_index_path).exists():
        raise FileNotFoundError("FAISS index not found. Please run ingest_documents first.")
    return FAISS.load_local(s.faiss_index_path,get_embed_model(),allow_dangerous_deserialization=True)
    
            
        
    