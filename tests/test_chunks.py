import unittest

from benchmark import build_chunks, rank_candidates


class ChunkingTests(unittest.TestCase):
    def test_chunks_cover_source_without_exceeding_size(self):
        text = "0123456789"
        chunks = build_chunks(text, size=6, stride=4)
        self.assertEqual(chunks, [(0, 6, "012345"), (4, 10, "456789")])

    def test_retrieval_stays_inside_context_contract(self):
        # Candidate 2 scores highest globally but belongs to another contract.
        self.assertEqual(rank_candidates([0.1, 0.8, 0.99], [0, 1]).tolist(), [1, 0])

    def test_empty_document_has_no_candidates(self):
        self.assertEqual(build_chunks(""), [])


if __name__ == "__main__":
    unittest.main()
