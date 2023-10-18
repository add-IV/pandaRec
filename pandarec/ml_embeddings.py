"""util functions for saving and loading embeddings"""
import torch


def save_embeddings(embeddings, path):
    """Save embeddings to a file."""
    torch.save(embeddings, path)


def load_embeddings(path) -> torch.Tensor:
    """Load embeddings from a file."""
    return torch.load(path)
