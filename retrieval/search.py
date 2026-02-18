from pathlib import Path
from typing import List

import chromadb
from sentence_transformers import SentenceTransformer

from retrieval.logging_config import setup_logging
logger = setup_logging("retrieval.search")



# =========================
# Paths and configuration
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = PROJECT_ROOT / "index"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "statistical_knowledge"

_embedder = None

def get_embedder():
    global _embedder
    if _embedder is None:
        logger.info("Loading embedding model: %s", EMBEDDING_MODEL_NAME)
        _embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _embedder



# =========================
# Search logic
# =========================

def semantic_search(query: str, k: int = 3) -> List[str]:

    if not isinstance(query, str) or not query.strip():
        logger.error("Invalid query received: %r", query)
        raise ValueError("Query must be a non-empty string")

    client = chromadb.PersistentClient(path=str(INDEX_PATH))

    try:
        logger.info("Loading Chroma collection: %s", COLLECTION_NAME)
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        logger.exception("Failed to load collection")
        raise RuntimeError("Vector index not found. Run build_index.py first.")

    embedder = get_embedder()

    embedding = embedder.encode(query)
    if hasattr(embedding, "ndim") and embedding.ndim > 1:
        embedding = embedding[0]

    query_embedding = embedding.tolist()

    try:
        logger.info("Running semantic search")
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
        )
    except Exception as e:
        logger.exception("Chroma query failed")
        raise RuntimeError(f"Semantic search failed: {e}")

    docs = results.get("documents")

    if not docs or not docs[0]:
        logger.warning("No results found")
        return []

    logger.info("Semantic search returned %d results", len(docs[0]))

    return docs[0]

# =========================
# CLI entry point
# =========================

if __name__ == "__main__":
    query = "How should I interpret a negative coefficient in a regression model?"

    print(f"Query:\n{query}\n")
    print("Results:\n")

    hits = semantic_search(query)

    for i, text in enumerate(hits, start=1):
        print(f"--- Result {i} ---")
        print(text.strip())
        	

