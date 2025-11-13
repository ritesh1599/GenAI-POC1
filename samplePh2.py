import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# -------------------------
# 1. Load embedding model
# -------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")  # light & fast, 384-dim

# -------------------------
# 2. Example documents (chunks)
# -------------------------
docs = [
    "AWS Glue is a fully managed ETL service.",
    "Apache Spark can run out of memory if executors are not configured properly.",
    "Vector databases like FAISS are used to store embeddings for fast retrieval.",
    "Out of memory errors in Spark often occur due to skewed data or large shuffles.",
    "RAG (Retrieval Augmented Generation) improves LLM answers by adding context."
]

# -------------------------
# 3. Convert docs → embeddings
# -------------------------
embeddings = model.encode(docs, convert_to_numpy=True)

# -------------------------
# 4. Create FAISS index
# -------------------------
dimension = embeddings.shape[1]  # e.g., 384
index = faiss.IndexFlatL2(dimension)  # L2 distance
index.add(embeddings)  # store vectors

print(f"FAISS index created with {index.ntotal} documents")

# -------------------------
# 5. Query → retrieve similar docs
# -------------------------
query = "Why does Spark crash due to memory issues?"
query_vec = model.encode([query], convert_to_numpy=True)

k = 2  # top 2 nearest chunks
distances, indices = index.search(query_vec, k)

print("\n🔎 Query:", query)
print("📌 Retrieved docs:")
for i, idx in enumerate(indices[0]):
    print(f"  {i+1}. {docs[idx]} (distance={distances[0][i]:.4f})")
