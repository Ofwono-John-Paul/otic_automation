from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

QDRANT_DIR = BASE_DIR / "qdrant_storage"
COLLECTION_NAME = "portfolio_knowledge"

MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 5


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded successfully.")


# ============================================================
# CONNECT TO LOCAL QDRANT
# ============================================================

print("\nConnecting to local Qdrant...")

client = QdrantClient(path=str(QDRANT_DIR))

print("Connected to Qdrant successfully.")


# ============================================================
# CHECK COLLECTION
# ============================================================

try:
    collection_info = client.get_collection(COLLECTION_NAME)

    print(f"\nCollection: {COLLECTION_NAME}")
    print(f"Vectors stored: {collection_info.points_count}")

except Exception as e:
    print("\nERROR: Could not access the Qdrant collection.")
    print(e)
    exit()


# ============================================================
# SEARCH FUNCTION
# ============================================================

def search_portfolio(question, top_k=TOP_K):

    # Convert question into embedding
    query_embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    # Search Qdrant
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
        with_payload=True
    )

    return results.points


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(question, results):

    print("\n" + "=" * 70)
    print(f"QUESTION: {question}")
    print("=" * 70)

    if not results:
        print("\nNo results found.")
        return

    for i, result in enumerate(results, start=1):

        payload = result.payload

        print(f"\nRESULT #{i}")
        print("-" * 70)

        print(f"Score   : {result.score:.4f}")
        print(f"Section : {payload.get('section', 'N/A')}")
        print(f"Title   : {payload.get('title', 'N/A')}")

        if payload.get("category"):
            print(f"Category: {payload.get('category')}")

        print(f"Source  : {payload.get('source', 'N/A')}")

        print("\nText:")
        print(payload.get("text", "No text available."))

    print("\n" + "=" * 70)


# ============================================================
# INTERACTIVE SEARCH
# ============================================================

print("\n" + "=" * 70)
print("PORTFOLIO QDRANT RETRIEVAL TEST")
print("=" * 70)

print("\nAsk questions about John's portfolio.")
print("Type 'exit' or 'quit' to stop.")

while True:

    question = input("\nYour question: ").strip()

    if not question:
        continue

    if question.lower() in ["exit", "quit"]:
        print("\nExiting retrieval test...")
        break

    try:

        results = search_portfolio(question)

        display_results(question, results)

    except Exception as e:

        print("\nERROR DURING SEARCH:")
        print(e)


# ============================================================
# CLOSE QDRANT
# ============================================================

client.close()

print("\nQdrant connection closed.")