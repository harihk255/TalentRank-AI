import csv
from pathlib import Path


class SubmissionService:

    def __init__(self, output_path):
        self.output_path = Path(output_path)

    def save_submission(self, ranked_candidates):
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["candidate_id", "rank", "score", "reasoning"])

            for candidate in ranked_candidates:
                writer.writerow([
                    candidate["candidate_id"],
                    candidate["rank"],
                    candidate["score"],
                    candidate["reasoning"]
                ])

        print(f"✅ Submission saved to: {self.output_path}")