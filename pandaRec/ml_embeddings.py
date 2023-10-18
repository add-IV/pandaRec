import torch


def save_embeddings(embeddings, path):
    torch.save(embeddings, path)


def load_embeddings(path) -> torch.Tensor:
    return torch.load(path)
