from backend.parser.candidate_parser import CandidateParser
from backend.parser.job_parser import JobParser
from backend.ranking.ranking_engine import RankingEngine
from backend.services.submission_service import SubmissionService


def main():

    print("Loading candidates...")

    candidate_parser = CandidateParser("datasets/candidates.jsonl")
    candidates = candidate_parser.load_candidates()

    print(f"Loaded {len(candidates)} candidates.")

    print("Loading job description...")

    job_parser = JobParser("datasets/job_description.docx")
    job_description = job_parser.load_job_description()

    print("Job description loaded.")

    print("Ranking candidates...")

    ranking_engine = RankingEngine()
    ranked_candidates = ranking_engine.rank_candidates(candidates)

    print(f"Top {len(ranked_candidates)} candidates selected.")

    submission = SubmissionService("exports/submission.csv")
    submission.save_submission(ranked_candidates)

    print("\n✅ Project completed successfully!")


if __name__ == "__main__":
    main()