"""Pruebas unitarias del filtrado final de relevancia."""

import unittest

from services.song_service import SongService


class EmbeddingStub:
    def __init__(self):
        self.queries = []

    def generate(self, query):
        self.queries.append(query)
        return [0.0] * 384


class RepositoryStub:
    def __init__(self, results):
        self.results = results
        self.calls = []

    def search(self, embedding, query):
        self.calls.append((embedding, query))
        return self.results


class SongServiceSearchTests(unittest.TestCase):
    def search_scores(self, scores):
        results = [{"titulo": str(score), "similitud": score} for score in scores]
        repository = RepositoryStub(results)
        service = SongService(repository=repository, embeddings=EmbeddingStub())
        return service.search("consulta"), repository, results

    def test_keeps_only_scores_at_or_above_acceptable_threshold(self):
        cases = [
            ([0.5992, 0.5870, 0.3754, 0.3233, 0.3154], [0.5992, 0.5870]),
            ([0.7044, 0.3295, 0.2866, 0.2750], [0.7044]),
            ([0.4122, 0.3390, 0.3132, 0.2972, 0.2698], [0.4122]),
            ([0.4689, 0.4535], [0.4689, 0.4535]),
            ([0.3999, 0.3233, 0.1], []),
        ]
        for scores, expected in cases:
            with self.subTest(scores=scores):
                actual, _, _ = self.search_scores(scores)
                self.assertEqual([song["similitud"] for song in actual], expected)

    def test_sorts_descending_and_caps_results_without_mutating_repository_rows(self):
        actual, _, original = self.search_scores([0.41, 0.8, 0.5, 0.6, 0.42, 0.9])
        self.assertEqual([song["similitud"] for song in actual], [0.9, 0.8, 0.6, 0.5, 0.42])
        self.assertEqual([song["similitud"] for song in original], [0.41, 0.8, 0.5, 0.6, 0.42, 0.9])

    def test_normalizes_percentage_scores_on_copies(self):
        actual, _, original = self.search_scores([59.92, 40])
        self.assertEqual([song["similitud"] for song in actual], [0.5992, 0.4])
        self.assertEqual([song["similitud"] for song in original], [59.92, 40])

    def test_ignores_invalid_scores(self):
        actual, _, _ = self.search_scores([None, "invalid", float("nan"), float("inf"), 0.4])
        self.assertEqual([song["similitud"] for song in actual], [0.4])

    def test_blank_query_does_not_call_embedding_or_repository(self):
        embeddings = EmbeddingStub()
        repository = RepositoryStub([])
        service = SongService(repository=repository, embeddings=embeddings)
        self.assertEqual(service.search("  "), [])
        self.assertEqual(embeddings.queries, [])
        self.assertEqual(repository.calls, [])


if __name__ == "__main__":
    unittest.main()
