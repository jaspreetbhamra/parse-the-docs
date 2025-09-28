from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_index(text: str):
    lines = [line for line in text.splitlines() if line.strip()]
    embeddings = model.encode(lines, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, lines, embeddings


def semantic_search(query: str, index, lines, embeddings, k=5):
    q_emb = model.encode([query], convert_to_numpy=True)
    docs, indexes = index.search(q_emb, k)
    return [
        {"score": float(docs[0][i]), "snippet": lines[indexes[0][i]]}
        for i in range(len(indexes[0]))
    ]
