import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle


def get_lemmatized_no_stop_words(text: str) -> list[str]:
    nltk.download("wordnet")
    nltk.download("omw-1.4")
    nltk.download("stopwords")
    wnl = WordNetLemmatizer()
    return [
        wnl.lemmatize(word)
        for word in re.findall(r"\w*[a-zA-Z]\w*", text)
        if word not in stopwords.words("english")
    ]


def generate_search_index(list_of_searchables: list[str]) -> dict[str, list[tuple[int, int]]]:
    lemmatized_searchables = [
        get_lemmatized_no_stop_words(searchable) for searchable in list_of_searchables
    ]
    # forward index
    frequency_per_searchable = [
        [(word, searchable.count(word)) for word in set(searchable)]
        for searchable in lemmatized_searchables
    ]
    # inverted index
    frequency_per_word = {}
    for searchable in frequency_per_searchable:
        for idx, (word, count) in enumerate(searchable):
            if word not in frequency_per_word:
                frequency_per_word[word] = [(idx, count)]
            else:
                frequency_per_word[word].append((idx, count))
    return frequency_per_word

def save_search_index(search_index, path):
    with open(path, "wb") as file:
        pickle.dump(search_index, file)

def load_search_index(path):
    with open(path, "rb") as file:
        return pickle.load(file)