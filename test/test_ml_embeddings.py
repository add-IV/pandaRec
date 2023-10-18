from pandaRec.ml_embeddings import save_embeddings, load_embeddings


def test_save_load_embeddings(tmp_path):
    embeddings = [
        [1,2,3,4],
        [5,6,7,8]
    ]
    save_embeddings(embeddings, tmp_path / "embeddings.pickle")
    loaded_embeddings = load_embeddings(tmp_path / "embeddings.pickle")
    assert embeddings == loaded_embeddings
