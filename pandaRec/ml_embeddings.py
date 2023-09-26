from sentence_transformers import SentenceTransformer
import torch

def generate_embeddings_sentence_transformers(list_of_searchables: list[str]):
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
    return model.encode(list_of_searchables, convert_to_tensor=True)


def save_embeddings(embeddings, path):
    torch.save(embeddings, path)

def load_embeddings(path) -> torch.Tensor:
    return torch.load(path)
