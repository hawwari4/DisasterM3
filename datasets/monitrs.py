# datasets/monitrs.py
import json
import os
from typing import List, Dict
from datasets.base import BaseDataset


class MONITRSDataset(BaseDataset):
    """
    Dataset adapter for MONITRS (Multimodal Observations of Natural Incidents 
    Through Remote Sensing).
    
    Supports temporal disaster monitoring with multiple satellite images 
    per event and QA pairs derived from news articles.
    
    Expected JSON structure per event:
    {
        "event_id": "flood_2021_001",
        "disaster_type": "flood",
        "location": {"lat": 44.9, "lon": -93.2},
        "timestamps": ["2021-05-01", "2021-05-07", "2021-05-14"],
        "image_paths": ["images/flood_001/t1.png", "t2.png", "t3.png"],
        "caption": "Severe flooding observed in Minnesota...",
        "qa_pairs": [
            {"question": "When did flooding begin?", "answer": "May 1st"},
            {"question": "Is recovery visible?", "answer": "Yes, by May 14"}
        ]
    }
    """
    
    # MONITRS subsets/tasks (adapt based on actual dataset structure)
    SUPPORTED_SUBSETS = ["train", "val", "test", "temporal_qa", "damage_tracking"]
    
    def load(self) -> List[Dict]:
        """
        Loads MONITRS samples from the subset JSON file.
        
        Returns:
            List of standardized sample dicts compatible with framework.
        """
        # Determine JSON file path
        subset_json = os.path.join(self.data_root, f"{self.subset}.json")
        if not os.path.exists(subset_json):
            raise FileNotFoundError(f"MONITRS file not found: {subset_json}")
        
        # Load raw data
        with open(subset_json, "r") as f:
            raw_data = json.load(f)
        
        self.data = []
        
        # MONITRS: One event can have multiple QA pairs → create one sample per QA
        for idx, event in enumerate(raw_data):
            qa_pairs = event.get("qa_pairs", [])
            
            # If no QA pairs, create a default sample from caption
            if not qa_pairs:
                parsed = self._parse_event(idx, event, 
                                          question=event.get("caption", ""),
                                          answer="")
                self.data.append(parsed)
            else:
                # Create one sample per QA pair
                for qa_idx, qa in enumerate(qa_pairs):
                    parsed = self._parse_event(
                        idx * 100 + qa_idx,  # unique ID per sample
                        event,
                        question=qa.get("question", ""),
                        answer=qa.get("answer", "")
                    )
                    self.data.append(parsed)
        
        print(f"Loaded {len(self.data)} samples from MONITRS subset: {self.subset}")
        return self.data
    
    def _parse_event(self, sample_idx: int, event: Dict, 
                     question: str, answer: str) -> Dict:
        """
        Converts a raw MONITRS event + QA pair into standardized format.
        
        Key design: MONITRS has temporal image sequences, so we store:
        - image_paths: full list of temporal images
        - image_path: primary image (first in sequence) for model input
        - latest_image_path: most recent image for recovery analysis
        """
        image_paths = event.get("image_paths", [])
        
        parsed = {
            # Unique identifier
            "id": f"monitrs_{self.subset}_{sample_idx}",
            "subset": self.subset,
            
            # QA content
            "question": question,
            "answer": answer,
            "options": event.get("options", ""),  # if multiple choice exists
            
            # Temporal image handling (MONITRS-specific)
            "image_paths": [
                os.path.join(self.data_root, "images", p.replace("\\", "/"))
                for p in image_paths
            ] if image_paths else [],
            
            # Primary image for model input (first in sequence)
            "image_path": os.path.join(
                self.data_root, "images", 
                image_paths[0].replace("\\", "/")
            ) if image_paths else "",
            
            # Latest image for recovery/temporal analysis
            "latest_image_path": os.path.join(
                self.data_root, "images",
                image_paths[-1].replace("\\", "/")
            ) if len(image_paths) > 1 else "",
            
            # Metadata
            "event_id": event.get("event_id", f"event_{sample_idx}"),
            "disaster_type": event.get("disaster_type", "unknown"),
            "location": event.get("location", {}),
            "timestamps": event.get("timestamps", []),
            "caption": event.get("caption", ""),
        }
        
        return parsed