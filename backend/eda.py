import json
from pathlib import Path

# Dataset Path
DATASET_PATH = Path("datasets/candidates.jsonl")

# Check Dataset Exists
if DATASET_PATH.exists():
    print("✅ Dataset found!")
else:
    print("❌ Dataset not found!")
    exit()

# Read Dataset
candidates = []

with open(DATASET_PATH, "r", encoding="utf-8") as file:
    for line in file:
        candidates.append(json.loads(line))

# Dataset Information
print(f"Total Candidates : {len(candidates)}")

# First Candidate
print(candidates[0])

# Top Level Keys
for key in candidates[0]:
    print(key)