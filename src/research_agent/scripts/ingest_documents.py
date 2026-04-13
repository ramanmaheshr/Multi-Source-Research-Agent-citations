import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from research_agent.tools.document_loader import ingest_documents
from research_agent.core.config import get_settings
if __name__ == '__main__':
    doc_dir = './data/docs'
    Path(doc_dir).mkdir(parents=True, exist_ok=True)
    s = get_settings()
    print(f'Ingesting documents from {doc_dir} ...')
    store = ingest_documents(doc_dir)
    print(f'Done. Index saved to {s.faiss_index_path}')