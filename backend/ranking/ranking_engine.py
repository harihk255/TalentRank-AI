from datetime import datetime


class RankingEngine:

    def __init__(self):
        self.must_have_skills = [
            "python", "embeddings", "sentence transformers", "retrieval",
            "ranking", "vector database", "faiss", "pinecone", "weaviate",
            "qdrant", "milvus", "elasticsearch", "opensearch", "bm25",
            "llm", "fine-tuning", "lora", "qlora", "rag", "nlp",
            "recommendation system", "search"
        ]

        self.good_locations = [
            "pune", "noida", "hyderabad", "mumbai", "delhi",
            "gurgaon", "bangalore", "bengaluru", "india"
        ]

        self.bad_consulting_companies = [
            "tcs", "infosys", "wipro", "accenture", "cognizant",
            "capgemini", "hcl", "tech mahindra", "mindtree"
        ]

    def normalize(self, text):
        if text is None:
            return ""
        return str(text).lower().strip()

    def skill_score(self, candidate):
        skills = candidate.get("skills", [])
        score = 0
        matched = []

        for skill in skills:
            name = self.normalize(skill.get("name", ""))
            proficiency = self.normalize(skill.get("proficiency", ""))
            duration = skill.get("duration_months", 0)
            endorsements = skill.get("endorsements", 0)

            for required in self.must_have_skills:
                if required in name or name in required:
                    matched.append(skill.get("name", ""))

                    if proficiency == "expert":
                        score += 10
                    elif proficiency == "advanced":
                        score += 8
                    elif proficiency == "intermediate":
                        score += 5
                    else:
                        score += 2

                    score += min(duration / 12, 3)
                    score += min(endorsements / 20, 2)

        return min(score, 100), matched

    def career_score(self, candidate):
        profile = candidate.get("profile", {})
        career = candidate.get("career_history", [])

        score = 0
        notes = []

        yoe = profile.get("years_of_experience", 0)

        if 6 <= yoe <= 8:
            score += 30
        elif 5 <= yoe <= 9:
            score += 25
        elif 4 <= yoe <= 10:
            score += 15
        else:
            score += 5

        title = self.normalize(profile.get("current_title", ""))

        if "ai" in title or "ml" in title or "machine learning" in title:
            score += 25
            notes.append("AI/ML title")
        elif "data scientist" in title or "nlp" in title:
            score += 22
            notes.append("relevant AI/data title")
        elif "backend" in title or "software" in title or "data engineer" in title:
            score += 15
            notes.append("strong engineering background")
        else:
            score += 5
            notes.append("less relevant current title")

        consulting_count = 0

        for job in career:
            company = self.normalize(job.get("company", ""))
            industry = self.normalize(job.get("industry", ""))
            description = self.normalize(job.get("description", ""))

            if any(c in company for c in self.bad_consulting_companies):
                consulting_count += 1

            if any(word in description for word in ["ranking", "retrieval", "search", "recommendation", "embedding", "ml model", "nlp"]):
                score += 15
                notes.append("career history shows ranking/retrieval/ML work")

            if "product" in industry or "software" in industry or "ai" in industry or "ml" in industry:
                score += 8

        if career and consulting_count == len(career):
            score -= 25
            notes.append("mostly consulting background")

        return max(0, min(score, 100)), notes

    def signal_score(self, candidate):
        signals = candidate.get("redrob_signals", {})
        profile = candidate.get("profile", {})

        score = 0
        notes = []

        if signals.get("open_to_work_flag", False):
            score += 20
            notes.append("open to work")

        notice = signals.get("notice_period_days", 90)

        if notice <= 30:
            score += 20
            notes.append("short notice period")
        elif notice <= 60:
            score += 12
        else:
            score += 5
            notes.append("long notice period")

        response_rate = signals.get("recruiter_response_rate", 0)

        if response_rate >= 0.7:
            score += 20
            notes.append("high recruiter response rate")
        elif response_rate >= 0.4:
            score += 12
        else:
            score += 5
            notes.append("low recruiter response rate")

        github = signals.get("github_activity_score", -1)

        if github >= 60:
            score += 15
            notes.append("strong GitHub activity")
        elif github >= 20:
            score += 8

        interview_rate = signals.get("interview_completion_rate", 0)

        if interview_rate >= 0.7:
            score += 15
        elif interview_rate >= 0.4:
            score += 8

        location = self.normalize(profile.get("location", ""))
        country = self.normalize(profile.get("country", ""))

        if country == "india":
            score += 10
            if any(loc in location for loc in self.good_locations):
                score += 5
                notes.append("preferred India location")
        elif signals.get("willing_to_relocate", False):
            score += 6
        else:
            notes.append("outside India and not willing to relocate")

        return min(score, 100), notes

    def final_score(self, candidate):
        skill_score, matched_skills = self.skill_score(candidate)
        career_score, career_notes = self.career_score(candidate)
        signal_score, signal_notes = self.signal_score(candidate)

        final = (
            skill_score * 0.45 +
            career_score * 0.35 +
            signal_score * 0.20
        )

        reasoning = self.create_reasoning(
            candidate,
            final,
            matched_skills,
            career_notes,
            signal_notes
        )

        return round(final / 100, 6), reasoning

    def create_reasoning(self, candidate, score, matched_skills, career_notes, signal_notes):
        profile = candidate.get("profile", {})
        signals = candidate.get("redrob_signals", {})

        title = profile.get("current_title", "Candidate")
        yoe = profile.get("years_of_experience", 0)
        company = profile.get("current_company", "unknown company")
        location = profile.get("location", "unknown location")
        notice = signals.get("notice_period_days", "unknown")
        response_rate = signals.get("recruiter_response_rate", 0)

        skill_text = ", ".join(matched_skills[:3]) if matched_skills else "limited direct AI retrieval skills"

        reason = (
            f"{title} with {yoe} years experience at {company}; "
            f"matched skills include {skill_text}. "
            f"Based in {location}, notice period {notice} days, "
            f"recruiter response rate {response_rate:.0%}."
        )

        return reason

    def rank_candidates(self, candidates):
        results = []

        for candidate in candidates:
            score, reasoning = self.final_score(candidate)

            results.append({
                "candidate_id": candidate.get("candidate_id"),
                "score": score,
                "reasoning": reasoning
            })

        results.sort(key=lambda x: (-x["score"], x["candidate_id"]))

        top_100 = results[:100]

        for index, row in enumerate(top_100):
            row["rank"] = index + 1

        return top_100