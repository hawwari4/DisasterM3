import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datasets.monitrs import MONITRSDataset

# Create fake MONITRS data for testing
fake_data = [{
    "event_id": "test_flood_001",
    "disaster_type": "flood",
    "location": {"lat": 44.9, "lon": -93.2},
    "timestamps": ["2021-05-01", "2021-05-07"],
    "image_paths": ["test/t1.png", "test/t2.png"],
    "caption": "Test flood event",
    "qa_pairs": [
        {"question": "What happened?", "answer": "Flooding"},
        {"question": "When?", "answer": "May 2021"}
    ]
}]

# Save fake data
os.makedirs("tests/fake_monitrs", exist_ok=True)
with open("tests/fake_monitrs/train.json", "w") as f:
    json.dump(fake_data, f)

# Test loading
dataset = MONITRSDataset(data_root="tests/fake_monitrs", subset="train")
samples = dataset.load()

print(f"✓ Loaded {len(samples)} samples")
for s in samples[:2]:  # Print first 2
    print(f"  ID: {s['id']}, Q: {s['question'][:50]}...")
