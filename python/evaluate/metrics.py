from nltk.translate.bleu_score import sentence_bleu
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def bleu_score(expected, actual):
    return sentence_bleu([expected.split()], actual.split()) if actual else 0

def exact_match(expected, actual):
    return int(expected.strip() == actual.strip())

def semantic_similarity(expected, actual):
    if not actual:
        return 0
    emb1 = model.encode(expected)
    emb2 = model.encode(actual)
    return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))

