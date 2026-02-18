
"""
Builds the semantic index from the statistical knowledge base.

This is the step that transforms human-written statistical explanations
into something the system can search.

Each markdown file is split into chunks, embedded, and stored in Chroma.

This only needs to be run when the knowledge base changes.

The index is persisted locally.
"""

from pathlib import Path
import uuid
import logging

import chromadb
from sentence_transformers import SentenceTransformer

# ===== CONFIG =====

KB_DIR = Path("kb")
INDEX_DIR = Path("index")
COLLECTION_NAME = "statistical_knowledge"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ===== LOGGING SETUP =====

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("retrieval.build_index")


"""
Split long KB files into overlapping chunks.

Overlap is intentional. It preserves context across chunk boundaries,
which improves retrieval quality later.

This is a simple sliding window, not sentence-aware on purpose.
Statistical explanations tend to be compact already.
"""

def split_text(text: str):

    assert CHUNK_OVERLAP < CHUNK_SIZE, "CHUNK_OVERLAP must be smaller than CHUNK_SIZE"

    chunks = []

    start = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - CHUNK_OVERLAP

    return chunks


"""
Read all markdown files from the knowledge base and build the vector index.

This function:

- loads KB files
- splits them into chunks
- generates embeddings
- stores everything in Chroma

If anything fails here, the retrieval pipeline will not work.

This is the foundation of the explainer.
"""

def build_index():

    logger.info("Starting index build")
    logger.info("KB directory: %s", KB_DIR.resolve())

    if not KB_DIR.exists():
        raise FileNotFoundError(f"KB directory not found: {KB_DIR}")

    md_files = sorted(KB_DIR.glob("*.md"))

    logger.info("Found %d KB files", len(md_files))

    if not md_files:
        raise ValueError("No .md files found in KB directory")

    texts = []
    metadatas = []

    for path in md_files:

        try:

            text = path.read_text(encoding="utf-8", errors="replace").strip()

        except Exception as e:

            logger.error("Failed to read file %s: %s", path.name, e)
            continue

        if not text:

            logger.warning("Skipping empty KB file: %s", path.name)
            continue

        chunks = split_text(text)

        logger.debug("File %s split into %d chunks", path.name, len(chunks))

        for chunk in chunks:

            texts.append(chunk)
            metadatas.append({"source": path.name})

    logger.info("Generated %d total text chunks", len(texts))

    if not texts:
        raise RuntimeError("No valid KB content found to index")

    logger.info("Loading embedding model: %s", EMBEDDING_MODEL_NAME)

    try:

        embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)

    except Exception as e:

        logger.exception("Failed to load embedding model")
        raise RuntimeError(f"Embedding model load failed: {e}")

    logger.info("Generating embeddings...")

    try:

        embeddings = embedder.encode(texts)

    except Exception as e:

        logger.exception("Embedding generation failed")
        raise RuntimeError(f"Embedding failed: {e}")

    logger.info("Embeddings generated successfully")

    INDEX_DIR.mkdir(exist_ok=True)

    logger.info("Opening Chroma index at: %s", INDEX_DIR.resolve())

    client = chromadb.PersistentClient(path=str(INDEX_DIR))

    try:

        collection = client.get_or_create_collection(name=COLLECTION_NAME)

    except Exception as e:

        logger.exception("Failed to access Chroma collection")
        raise RuntimeError(f"Collection error: {e}")

    ids = [str(uuid.uuid4()) for _ in texts]

    logger.info("Writing %d documents to Chroma", len(ids))

    try:

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )

    except Exception as e:

        logger.exception("Failed to write documents to Chroma")
        raise RuntimeError(f"Chroma write failed: {e}")

    count = collection.count()

    logger.info("Index build complete. Documents stored: %d", count)

    if count == 0:
        raise RuntimeError("Index built but collection is empty")


# ===== ENTRYPOINT =====
# Entry point for manual execution.
# This allows rebuilding the index from the command line.

if __name__ == "__main__":

    try:

        build_index()

    except Exception:

        logger.exception("Index build failed")

        raise
