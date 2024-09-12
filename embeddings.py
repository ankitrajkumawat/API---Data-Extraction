import openai
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


def split_into_chunks(content, max_chunk_size=512):
    chunks = []
    words = content.split()
    chunk = []
    for word in words:
        chunk.append(word)
        if len(chunk) >= max_chunk_size:
            chunks.append(" ".join(chunk))
            chunk = []
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks


def find_relevant_response(question: str, stored_content: str) -> str:
    stored_content_chunks = split_into_chunks(stored_content)
    print( "stored_content_chunks")
    stored_content_embedding = model.encode(stored_content_chunks)
    print("stored_content_embedding")
    question_embedding = model.encode(question, convert_to_tensor=True)
    print("question_embedding")
    # Compare the user's question embedding with each document's embedding
    similarities = []
    for content, content_txt in zip(stored_content_embedding, stored_content_chunks):
        print("before simscore")
        similarity_score = cosine_similarity(
            [question_embedding],
            [content]
        )[0][0]  # Get the similarity score
        print("aftersimscore")
        similarities.append((similarity_score, content_txt))

    # Sort by similarity score in descending order
    similarities.sort(key=lambda x: x[0], reverse=True)

    # Get the most relevant document based on similarity
    most_relevant_doc = similarities[0][1] if similarities else None

    if most_relevant_doc:
        response = most_relevant_doc
    else:
        response = "No relevant document found"

    return response
