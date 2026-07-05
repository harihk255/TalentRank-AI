import csv
import json
from pathlib import Path


class DashboardExportService:

    def __init__(self, candidates_path, submission_path, output_path):
        self.candidates_path = Path(candidates_path)
        self.submission_path = Path(submission_path)
        self.output_path = Path(output_path)

    def load_candidates(self):
        candidates = {}

        with open(self.candidates_path, "r", encoding="utf-8") as file:
            for line in file:
                candidate = json.loads(line)
                candidates[candidate["candidate_id"]] = candidate

        return candidates

    def load_submission(self):
        rows = []

        with open(self.submission_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                rows.append(row)

        return rows

    def export_dashboard_data(self):
        candidates = self.load_candidates()
        submission_rows = self.load_submission()

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8", newline="") as file:
            fieldnames = [
                "candidate_id",
                "rank",
                "score",
                "name",
                "title",
                "company",
                "experience",
                "location",
                "country",
                "skills",
                "open_to_work",
                "notice_period",
                "github_score",
                "response_rate",
                "profile_views",
                "saved_by_recruiters",
                "reasoning"
            ]

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for row in submission_rows:
                candidate_id = row["candidate_id"]
                candidate = candidates.get(candidate_id, {})

                profile = candidate.get("profile", {})
                signals = candidate.get("redrob_signals", {})
                skills = candidate.get("skills", [])

                skill_names = [skill.get("name", "") for skill in skills]
                skill_text = ", ".join(skill_names[:10])

                writer.writerow({
                    "candidate_id": candidate_id,
                    "rank": row["rank"],
                    "score": row["score"],
                    "name": profile.get("anonymized_name", ""),
                    "title": profile.get("current_title", ""),
                    "company": profile.get("current_company", ""),
                    "experience": profile.get("years_of_experience", ""),
                    "location": profile.get("location", ""),
                    "country": profile.get("country", ""),
                    "skills": skill_text,
                    "open_to_work": signals.get("open_to_work_flag", ""),
                    "notice_period": signals.get("notice_period_days", ""),
                    "github_score": signals.get("github_activity_score", ""),
                    "response_rate": signals.get("recruiter_response_rate", ""),
                    "profile_views": signals.get("profile_views_received_30d", ""),
                    "saved_by_recruiters": signals.get("saved_by_recruiters_30d", ""),
                    "reasoning": row["reasoning"]
                })

        print(f"✅ Dashboard data exported to: {self.output_path}")