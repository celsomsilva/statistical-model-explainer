import numpy as np
import chromadb
from pathlib import Path

import retrieval.search as search_mod


class FakeEmbedder:
    def __init__(self, *args, **kwargs):
        pass

    def encode(self, texts, **kwargs):
        # accepts str or list[str]
        if isinstance(texts, str):
            texts = [texts]
        # fixed 384-d vector (same size as MiniLM)
        return np.stack([np.ones(384, dtype=np.float32) for _ in texts], axis=0)


def test_kb_has_markdown_files():
    root = Path(__file__).resolve().parents[1]
    kb = root / "kb"
    md_files = list(kb.rglob("*.md"))
    assert len(md_files) > 0


def test_search_returns_documents(monkeypatch, tmp_path):
    # creates a temporary index for the test

    index_path = tmp_path / "index"
    client = chromadb.PersistentClient(path=str(index_path))
    collection = client.get_or_create_collection(name="statistical_knowledge")

    # adds fake docs with fake embeddings
    docs = ["AIC compares models by balancing fit and complexity.", "Coefficients can be positive or negative."]
    embeddings = FakeEmbedder().encode(docs)
    collection.add(
        documents=docs,
        embeddings=[v.tolist() for v in embeddings],
        ids=["d1", "d2"],
    )

    # monkeypatch so search uses our temporary index and fake embedder
    monkeypatch.setattr(search_mod, "INDEX_PATH", index_path)
    monkeypatch.setattr(search_mod, "SentenceTransformer", FakeEmbedder)

    hits = search_mod.semantic_search("What is AIC?", k=2)
    assert isinstance(hits, list)
    assert len(hits) > 0

