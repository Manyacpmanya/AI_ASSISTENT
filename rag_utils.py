from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def split_text(text, chunk_size=100):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def create_embeddings(chunks):
    return model.encode(chunks)

def build_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index

def retrieve_chunks(index, query_embedding, k=3):
    D, I = index.search(np.array([query_embedding]), k)
    return I[0]
