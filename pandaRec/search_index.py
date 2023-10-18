"""A module for generating a search index from a list of descriptions
and save/ load the index to/ from a file."""
import re
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def lemmatize_no_stop_words(text: str) -> list[str]:
    """Lemmatizes the given text and removes stop words.
    Stop words are words that are very common and thus do not carry much meaning."""
    nltk.download("wordnet", quiet=True)
    nltk.download("omw-1.4", quiet=True)
    nltk.download("stopwords", quiet=True)
    wnl = WordNetLemmatizer()
    words = re.findall(r"\w*[a-zA-Z]\w*", text)
    return [
        wnl.lemmatize(word) for word in words if word not in stopwords.words("english")
    ]


def generate_search_index(descriptions: list[str]) -> dict[str, list[tuple[int, int]]]:
    """Generates a search index from the given list of descriptions."""
    # 1. Lemmatize the descriptions
    lemmatized_descriptions = [
        lemmatize_no_stop_words(description) for description in descriptions
    ]
    # 2. build the forward index, one list of (word, frequency) tuples per description
    frequency_per_description = [
        [(word, description.count(word)) for word in set(description)]
        for description in lemmatized_descriptions
    ]
    # 3. construct the inverted index, one list of (description_index, frequency) tuples per word
    frequency_per_word = {}
    for idx, description in enumerate(frequency_per_description):
        for word, count in description:
            if word not in frequency_per_word:
                frequency_per_word[word] = [(idx, count)]
            else:
                frequency_per_word[word].append((idx, count))
    return frequency_per_word


def save_search_index(search_index, path):
    """Saves the given search index to the given path."""
    with open(path, "wb") as file:
        pickle.dump(search_index, file)


def load_search_index(path):
    """Loads the search index from the given path."""
    with open(path, "rb") as file:
        return pickle.load(file)
