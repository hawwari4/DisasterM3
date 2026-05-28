import json
import os
from typing import List, Dict

from datasets.base import BaseDataset


class MONITRSDataset(BaseDataset):
    """
    Dataset adapter for MONITRS (Multimodal Observations of Natural
    Incidents Through Remote Sensing).

    MONITRS contains over 10,000 FEMA disaster events with:
        - Temporal satellite image sequences (multiple timestamps per event)
        - Natural language captions derived from news articles
        - Geotagged locations
        - Question-answer pairs for disaster monitoring tasks

    Unlike DisasterM3 which uses bi-temporal (before/after) pairs,
    MONITRS provides full temporal sequences tracking disaster progression
    from initial impact through recovery.

    Expected dataset structure:
        MONITRS/
        ├── images/
        │   └── {event_id}/
        │       ├── {timestamp_1}.png
        │       ├── {timestamp_2}.png
        │       └── ...
        ├── train.json
        ├── val.json
        └── test.json

    Each JSON entry contains:
        {
            "event_id": "...",
            "disaster_type": "...",
            "location": {"lat": ..., "lon": ...},
            "timestamps": ["2021-05-01", "2021-05-07", ...],
            "image_paths": ["images/event_id/t1.png", ...],
            "caption": "...",
            "qa_pairs": [
                {"question": "...", "answer": "..."},
                ...
            ]
        }
    """

    SUPPORTED_SUBSETS = ["train", "val", "test"]

    def load(self) -> List[Dict]:
        """
        Loads MONITRS samples from the split JSON file.

        Returns:
            List of standardized sample dicts, one per QA pair.
        """
        if self.subset not in self.SUPPORTED_SUBSETS:
            raise ValueError(
                f"Invalid subset '{self.subset}'. "
                f"Choose from: {self.SUPPORTED_SUBSETS}"
            )

        split_json = os.path.join(self.data_root, f"{self.subset}.json")

        if not os.path.exists(split_json):
            raise FileNotFoundError(
                f"MONITRS split file not found: {split_json}"
            )

        with open(split_json, "r") as f:
            raw_data = json.load(f)

        self.data = []
        sample_idx = 0

        for event in raw_data:
            # Each event may have multiple QA pairs
            # We create one sample per QA pair
            qa_pairs = event.get("qa_pairs", [])

            # If no QA pairs, create a captioning-only sample
            if not qa_pairs:
                parsed = self._parse_event(sample_idx, event, question=None, answer=None)
                self.data.append(parsed)
                sample_idx += 1
            else:
                for qa in qa_pairs:
                    parsed = self._parse_event(
                        sample_idx,
                        event,
                        question=qa.get("question", ""),
                        answer=qa.get("answer", "")
                    )
                    self.data.append(parsed)
                    sample_idx += 1

        print(f"Loaded {len(self.data)} samples from MONITRS subset: {self.subset}")
        return self.data

    def _parse_event(self, idx: int, event: Dict, question: str, answer: str) -> Dict:
        """
        Converts a raw MONITRS event into a standardized sample format.

        Key difference from DisasterM3: MONITRS provides a full temporal
        sequence of images instead of just a before/after pair.
        """
        # Resolve full image paths
        image_paths = [
            os.path.join(self.data_root, p.replace("\\", "/"))
            for p in event.get("image_paths", [])
        ]

        parsed = {
            "id": f"monitrs_{self.subset}_{idx}",
            "dataset": "monitrs",
            "subset": self.subset,

            # Temporal image sequence (key difference from DisasterM3)
            "image_paths": image_paths,
            "timestamps": event.get("timestamps", []),

            # Use first image as primary, last as most recent post-disaster
            "image_path": image_paths[0] if image_paths else None,
            "latest_image_path": image_paths[-1] if len(image_paths) > 1 else None,

            # Event metadata
            "event_id": event.get("event_id", ""),
            "disaster_type": event.get("disaster_type", ""),
            "location": event.get("location", {}),

            # Text fields
            "caption": event.get("caption", ""),
            "question": question,
            "answer": answer,
        }

        return parsed
