import json
from pathlib import Path


class CandidateParser:

    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)

    def load_candidates(self):

        candidates = []

        with open(self.dataset_path, "r", encoding="utf-8") as file:
            for line in file:
                candidates.append(json.loads(line))

        return candidates