# Reuse Analysis — EarthVQA

## Overview of EarthVQA

EarthVQA (AAAI 2024) is a remote sensing Visual Question Answering dataset containing:
- 6,000 satellite images with corresponding semantic segmentation masks
- 208,593 QA pairs focused on relational reasoning
- Tasks: object counting, spatial relation reasoning, and comprehensive scene analysis
- Dataset structure:

```
EarthVQA/
├── Train/
│   ├── images_png/
│   └── masks_png/
├── Val/
│   ├── images_png/
│   └── masks_png/
├── Test/
│   └── images_png/
├── Train_QA.json
├── Val_QA.json
└── Test_QA.json
```

---

## Identified Reusable Design Pattern: JSON-based QA Loading

### What the pattern is

EarthVQA stores all questions and answers in structured JSON files (`Train_QA.json`, `Val_QA.json`, `Test_QA.json`), each paired with an image filename. This is the same pattern used by DisasterM3, where each subset is stored as a `.json` file containing a list of samples with image paths, questions, and answers.

The shared pattern looks like:

```
JSON file
  └── list of samples
        ├── image_path (or pre/post image paths)
        ├── question / prompt
        └── answer / ground truth
```

### Why this pattern is reusable

This JSON-based loading pattern is dataset-agnostic. Both EarthVQA and DisasterM3 follow it, which means the same loading logic can be abstracted into `BaseDataset` and reused across both datasets with minimal changes.

The only differences between the two are:
- Key names (`"prompts"` in DisasterM3 vs `"question"` in EarthVQA)
- Single image (EarthVQA) vs bi-temporal images (DisasterM3)
- Presence of segmentation masks in EarthVQA (not present in DisasterM3)

---

## How It Fits Into the Proposed Framework

The `BaseDataset` class defined in `datasets/base.py` already anticipates this pattern:

```python
class BaseDataset(ABC):
    def load(self) -> List[Dict]:
        raise NotImplementedError
```

An `EarthVQADataset` adapter can be implemented by simply:
1. Reading the JSON file for the chosen split (Train/Val/Test)
2. Mapping EarthVQA-specific keys to the standardized format
3. Returning a list of dicts with consistent keys: `id`, `image_path`, `question`, `answer`

```python
class EarthVQADataset(BaseDataset):
    def load(self) -> List[Dict]:
        split_json = os.path.join(self.data_root, f"{self.subset}_QA.json")
        with open(split_json, "r") as f:
            raw_data = json.load(f)

        self.data = []
        for idx, sample in enumerate(raw_data):
            self.data.append({
                "id": f"earthvqa_{idx}",
                "image_path": os.path.join(self.data_root, self.subset, "images_png", sample["image"]),
                "question": sample["question"],
                "answer": sample["answer"],
            })
        return self.data
```

This adapter slots directly into the framework without modifying any other component — the model runner and evaluator remain untouched, which is exactly the decoupling goal of the proposed architecture.

---

## Summary

| Aspect | Detail |
|---|---|
| Reusable pattern | JSON-based QA loading with image path references |
| Found in | EarthVQA (`Train_QA.json`, `Val_QA.json`, `Test_QA.json`) |
| Also used in | DisasterM3 (`bearing_body.json`, `caption.json`, etc.) |
| How it fits | Directly maps to `BaseDataset.load()` interface |
| Benefit | New datasets can be added without touching model or evaluator code |
