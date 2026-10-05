from pathlib import Path
import json

from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "portfolio_chunks.json"
OUTPUT_FILE = BASE_DIR / "portfolio_embeddings.json"

MODEL_NAME = "all-MiniLM-L6-v2"


# ============================================================
# LOAD MODEL
# ============================================================

print("\nLoading embedding model...")
print(f"Model: {MODEL_NAME}")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded successfully.")


# ============================================================
# LOAD CHUNKS
# ============================================================

print("\nLoading portfolio chunks...")

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as file:

    chunks = json.load(file)


print(f"Loaded {len(chunks)} chunks.")


# ============================================================
# PREPARE TEXT
# ============================================================

texts = [
    chunk["text"]
    for chunk in chunks
]


# ============================================================
# GENERATE EMBEDDINGS
# ============================================================

print("\nGenerating embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    normalize_embeddings=True
)


# ============================================================
# ADD EMBEDDINGS TO CHUNKS
# ============================================================

embedded_chunks = []

for chunk, embedding in zip(chunks, embeddings):

    embedded_chunk = {
        "chunk_id": chunk["chunk_id"],
        "section": chunk["section"],
        "title": chunk["title"],
        "source": chunk["source"],
        "text": chunk["text"],
        "embedding": embedding.tolist()
    }

    # Preserve category if it exists
    if "category" in chunk:
        embedded_chunk["category"] = chunk["category"]

    embedded_chunks.append(embedded_chunk)


# ============================================================
# SAVE EMBEDDINGS
# ============================================================

print("\nSaving embeddings...")

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        embedded_chunks,
        file,
        indent=2,
        ensure_ascii=False
    )


# ============================================================
# INFORMATION
# ============================================================

vector_size = len(embeddings[0])

print("\n" + "=" * 60)
print("EMBEDDING COMPLETED")
print("=" * 60)

print(f"Chunks embedded : {len(embedded_chunks)}")
print(f"Vector size     : {vector_size}")
print(f"Model           : {MODEL_NAME}")
print(f"Output file     : {OUTPUT_FILE}")

print("\nExample vector:")
print(embeddings[0][:10])

print("\nDone!")