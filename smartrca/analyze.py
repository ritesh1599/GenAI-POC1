import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llm_client import ask_llm


# -------------------------
# 1. Load embedding model
# -------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Directory to persist FAISS index and metadata
FAISS_DIR = "faiss_store"
FAISS_INDEX_FILE = os.path.join(FAISS_DIR, "kb_index.faiss")
FAISS_META_FILE = os.path.join(FAISS_DIR, "kb_chunks.pkl")


# -------------------------
# 2. Helper: Chunk text
# -------------------------
def chunk_text(text, chunk_size=512, overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    return splitter.split_text(text)


# -------------------------
# 3. Helper: Embeddings
# -------------------------
def get_embeddings(text_chunks):
    return [embedding_model.encode(chunk) for chunk in text_chunks]


# -------------------------
# 4. Helper: Save FAISS index
# -------------------------
def save_faiss_index(index, chunks):
    os.makedirs(FAISS_DIR, exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_FILE)
    with open(FAISS_META_FILE, "wb") as f:
        pickle.dump(chunks, f)


# -------------------------
# 5. Helper: Load FAISS index
# -------------------------
def load_faiss_index():
    if os.path.exists(FAISS_INDEX_FILE) and os.path.exists(FAISS_META_FILE):
        index = faiss.read_index(FAISS_INDEX_FILE)
        with open(FAISS_META_FILE, "rb") as f:
            chunks = pickle.load(f)
        return index, chunks
    return None, None


# -------------------------
# 6. Helper: Create FAISS index
# -------------------------
def create_faiss_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index


# -------------------------
# 7. Helper: Retrieval
# -------------------------
def retrieve_chunks(query, index, chunks, top_k=3):
    query_embedding = embedding_model.encode([query])
    D, I = index.search(np.array(query_embedding).astype("float32"), top_k)
    return [chunks[i] for i in I[0]]


# -------------------------
# 8. Main Function (Phase 2 RAG)
# -------------------------
def analyze_text_log(text):
    # Step A: Chunk the input log
    log_chunks = chunk_text(text)

    # Step B: Try to load persisted FAISS index
    kb_index, kb_chunks = load_faiss_index()

    # Step C: If not available, build from scratch using rag_docs/
    if kb_index is None:
        kb_text = ""
        if os.path.exists("rag_docs"):
            for f in os.listdir("rag_docs"):
                with open(os.path.join("rag_docs", f), "r", encoding="utf-8") as fh:
                    kb_text += fh.read() + "\n"

        kb_chunks = chunk_text(kb_text) if kb_text else []
        if kb_chunks:
            kb_embeddings = get_embeddings(kb_chunks)
            kb_index = create_faiss_index(kb_embeddings)
            save_faiss_index(kb_index, kb_chunks)

    # Step D: Retrieve context for each log chunk
    context_chunks = []
    if kb_index:
        for lc in log_chunks:
            top_chunks = retrieve_chunks(lc, kb_index, kb_chunks)
            context_chunks.extend(top_chunks)

    # Step E: Build final prompt
    final_context = (
        "Relevant Knowledge:\n" + "\n".join(context_chunks) + "\n\nLog:\n" + text
        if context_chunks
        else text
    )

    # Step F: Call LLM
    return ask_llm(final_context)
