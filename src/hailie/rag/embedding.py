import csv
import os
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

# ========= CONFIG =========

DOCS_DIR = "docs"              # folder with your PDFs / TXTs
OUT_CSV = "embeddings.csv"     # single CSV output
MODEL_NAME = "BAAI/bge-small-en-v1.5"

# Chunking params (tunable)
MAX_WORDS = 280                # ~short paragraph / chunk
MIN_WORDS = 40                 # avoid tiny scraps

# ==========================


def load_text_from_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    parts = []
    for page in reader.pages:
        text = page.extract_text() or ""
        parts.append(text)
    return "\n".join(parts)


def load_text_from_txt(path: Path) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def chunk_text(text: str, max_words: int = MAX_WORDS, min_words: int = MIN_WORDS):
    """
    Simple word-based chunking:
    - Splits on whitespace
    - Builds chunks up to max_words
    - Drops very tiny trailing chunks < min_words
    """
    words = text.split()
    chunks = []
    current = []

    for w in words:
        current.append(w)
        if len(current) >= max_words:
            chunks.append(" ".join(current))
            current = []

    if len(current) >= min_words:
        chunks.append(" ".join(current))

    return chunks


def iter_documents(docs_dir: str):
    """
    Yields (doc_id, path, text) for each supported file.
    """
    root = Path(docs_dir)
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        ext = path.suffix.lower()
        if ext == ".pdf":
            text = load_text_from_pdf(path)
        elif ext in {".txt", ".md"}:
            text = load_text_from_txt(path)
        else:
            continue  # skip unsupported
        text = normalize_whitespace(text)
        if text.strip():
            doc_id = path.stem
            yield doc_id, str(path), text


def main():
    # Load embedding model
    print(f"Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    rows = []

    for doc_id, path, full_text in iter_documents(DOCS_DIR):
        chunks = chunk_text(full_text)
        if not chunks:
            continue

        print(f"Embedding {len(chunks)} chunks from: {path}")

        # Encode all chunks at once for speed
        embeddings = model.encode(
            chunks,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        # Store: doc_id, chunk_id, path, chunk_text, embedding_vector (as JSON-ish string)
        for i, (chunk_text, emb) in enumerate(zip(chunks, embeddings)):
            emb_str = " ".join(f"{x:.6f}" for x in emb.tolist())
            rows.append(
                {
                    "doc_id": doc_id,
                    "chunk_id": i,
                    "path": path,
                    "text": chunk_text,
                    "embedding": emb_str,
                }
            )

    # Write single CSV
    if rows:
        fieldnames = ["doc_id", "chunk_id", "path", "text", "embedding"]
        with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} chunks to {OUT_CSV}")
    else:
        print("No documents processed. Check DOCS_DIR or file types.")


if __name__ == "__main__":
    main()
