from pandarec.search_index import (
    lemmatize_no_stop_words,
    generate_search_index,
    save_search_index,
    load_search_index,
)

def test_lemmatize_no_stop_words():
    assert lemmatize_no_stop_words("I am a test") == ["I", "test"]
    assert lemmatize_no_stop_words("I am a test") != ["I", "am", "a", "test"]
    assert lemmatize_no_stop_words("I am a test") != ["I", "am", "a", "test", "test"]

def test_generate_search_index():
    descriptions = ["I am a test", "I am another test", "I, too, am a test magically"]
    search_index = generate_search_index(descriptions)
    assert search_index["I"] == [(0, 1), (1, 1), (2, 1)]
    assert search_index["test"] == [(0, 1), (1, 1), (2, 1)]
    assert search_index["another"] == [(1, 1)]
    assert search_index["magically"] == [(2, 1)]

def test_save_load_search_index(tmp_path):
    descriptions = ["I am a test", "I am another test", "I, too, am a test magically"]
    search_index = generate_search_index(descriptions)
    save_search_index(search_index, tmp_path / "search_index.pickle")
    loaded_search_index = load_search_index(tmp_path / "search_index.pickle")
    assert search_index == loaded_search_index
