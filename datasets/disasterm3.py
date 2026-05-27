import json
import os
from typing import List, Dict

from datasets.base import BaseDataset


class DisasterM3Dataset(BaseDataset):
    """
    Dataset adapter for DisasterM3.

    Supports the following subsets/tasks:
        - bearing_body
        - building_damage_counting
        - disaster_type
        - road_damage_counting
        - landuse
        - relational_reasoning_qa
        - caption
        - recovery
    """

    # Tasks that use two images (pre + post disaster)
    BI_TEMPORAL_SUBSETS = [
        "bearing_body",
        "building_damage_counting",
        "disaster_type",
        "road_damage_counting",
        "caption",
        "recovery"
    ]

    # Tasks that use a single image
    SINGLE_IMAGE_SUBSETS = [
        "landuse",
        "relational_reasoning_qa"
    ]

    def load(self) -> List[Dict]:
        """
        Loads DisasterM3 samples from the subset JSON file.

        Returns:
            List of standardized sample dicts.
        """
        subset_json = os.path.join(self.data_root, f"{self.subset}.json")

        if not os.path.exists(subset_json):
            raise FileNotFoundError(f"Dataset file not found: {subset_json}")

        with open(subset_json, "r") as f:
            raw_data = json.load(f)

        self.data = []
        for idx, sample in enumerate(raw_data):
            parsed = self._parse_sample(idx, sample)
            self.data.append(parsed)

        print(f"Loaded {len(self.data)} samples from DisasterM3 subset: {self.subset}")
        return self.data

    def _parse_sample(self, idx: int, sample: Dict) -> Dict:
        """
        Converts a raw DisasterM3 sample into a standardized format.
        """
        parsed = {
            "id": f"{self.subset}_{idx}",
            "subset": self.subset,
            "question": sample.get("prompts", ""),
            "answer": sample.get("answers", sample.get("answer", "")),
            "options": sample.get("options_str", sample.get("option_str", "")),
        }

        # Handle bi-temporal (pre + post) images
        if self.subset in self.BI_TEMPORAL_SUBSETS:
            parsed["pre_image_path"] = os.path.join(
                self.data_root, "images", sample["pre_image_path"]
            )
            parsed["post_image_path"] = os.path.join(
                self.data_root, "images", sample["post_image_path"]
            )

        # Handle single image
        elif self.subset in self.SINGLE_IMAGE_SUBSETS:
            image_key = "pre_image_path" if "pre_image_path" in sample else "image_path"
            parsed["image_path"] = os.path.join(
                self.data_root, "images", sample[image_key].replace("\\", "/")
            )

        return parsed