# VLM Evaluation Methodology

## Nature of Evaluation Data
VLMs are evaluated on datasets containing:
- **Image:** visual input (e.g. satellite imagery)
- **Question:** text prompt about the image
- **Ground Truth Answer:** human-annotated correct answer
- **Model Prediction:** what the VLM outputs

Answers are either **closed-ended** (yes/no, multiple choice, fixed categories) or **open-ended** (free text, counts, descriptions).

---

## Core Evaluation Tasks

| Task | Description |
|---|---|
| **VQA** | Model answers questions about image content |
| **Damage Assessment** | Classifies damage level: none / minor / major / destroyed |
| **Counting / Reasoning** | Model counts or reasons about objects in the image |
| **Captioning** | Model generates a free-text description of the image |

---

## Key Metrics

## Classification Tasks (closed-ended)
- **Accuracy:** % of correct predictions
- **F1-Score:** balances Precision and Recall; essential when classes are imbalanced
- **Precision / Recall:** measures false positives vs false negatives

## Text Generation Tasks (open-ended)
- **BLEU:** measures n-gram overlap between prediction and ground truth
- **ROUGE:** recall-focused overlap metric; common for longer answers
- **METEOR:** accounts for synonyms and paraphrasing; more flexible than BLEU

## Numerical Tasks
- **MAE (Mean Absolute Error):** average difference between predicted and actual counts

---

## Evaluation Pipeline

```
Dataset (image + question + ground truth)
        ↓
VLM generates prediction
        ↓
Prediction compared to ground truth
        ↓
Metrics computed and logged
```

---

## Key Challenges
- **Open-ended answers** are hard to score automatically; paraphrases score low on BLEU despite being correct
- **Class imbalance:** disaster datasets have far more "undamaged" than "destroyed" samples; accuracy alone is misleading
- **Cross-dataset generalization:** models trained on one disaster type often underperform on others

## Evaluation Methodology Summary

<div align="center">
  <img src="https://github.com/user-attachments/assets/d6a11a30-a4da-4ea3-81a6-2ecf89bc05c7" width="500">
</div>
