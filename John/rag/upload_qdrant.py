from pathlib import Path
import json

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

EMBEDDINGS_FILE = BASE_DIR / "portfolio_embeddings.json"

QDRANT_DIR = BASE_DIR / "qdrant_storage"

COLLECTION_NAME = "portfolio_knowledge"

VECTOR_SIZE = 384


# ============================================================
# LOAD EMBEDDINGS
# ============================================================

print("\nLoading portfolio embeddings...")

with open(
    EMBEDDINGS_FILE,
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)

print(f"Loaded {len(data)} embedded chunks.")


# ============================================================
# CONNECT TO LOCAL QDRANT
# ============================================================

print("\nStarting Qdrant local mode...")

client = QdrantClient(
    path=str(QDRANT_DIR)
)

print(f"Qdrant storage: {QDRANT_DIR}")


# ============================================================
# CREATE COLLECTION
# ============================================================

existing_collections = [
    collection.name
    for collection in client.get_collections().collections
]


if COLLECTION_NAME in existing_collections:

    print(
        f"\nCollection '{COLLECTION_NAME}' already exists."
    )

else:

    print(
        f"\nCreating collection '{COLLECTION_NAME}'..."
    )

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )

    print("Collection created successfully.")


# ============================================================
# PREPARE POINTS
# ============================================================

print("\nPreparing vectors...")

points = []

for item in data:

    payload = {
        "chunk_id": item["chunk_id"],
        "section": item["section"],
        "title": item["title"],
        "source": item["source"],
        "text": item["text"]
    }

    # Preserve category if present
    if "category" in item:
        payload["category"] = item["category"]

    point = PointStruct(
        id=item["chunk_id"],
        vector=item["embedding"],
        payload=payload
    )

    points.append(point)


# ============================================================
# UPLOAD TO QDRANT
# ============================================================

print(
    f"\nUploading {len(points)} vectors to Qdrant..."
)

client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print("Vectors uploaded successfully.")


# ============================================================
# VERIFY COLLECTION
# ============================================================

collection_info = client.get_collection(
    collection_name=COLLECTION_NAME
)

print("\n" + "=" * 60)
print("QDRANT SETUP COMPLETED")
print("=" * 60)

print(f"Collection : {COLLECTION_NAME}")
print(f"Vectors    : {collection_info.points_count}")
print(f"Vector size: {VECTOR_SIZE}")
print("Distance   : COSINE")
print(f"Storage    : {QDRANT_DIR}")

# CLOSE CLIENT

client.close()

print("\nQdrant local database is ready.")