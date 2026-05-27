# Evaluation Methodology for Vision Language Models (VLMs)

## What is a Vision Language Model (VLM)?

A Vision Language Model (VLM) is an AI model that can process both **images** and **text** together. Unlike a regular language model that only reads text, a VLM can:
- Look at an image
- Understand a question about it
- Generate a text answer

**Example:**
- Input: satellite image of a flooded area + question: *"Is this area affected by flooding?"*
- Output: *"Yes, approximately 60% of the visible area shows signs of flooding."*

---

## Nature of Evaluation Data

### What does evaluation data look like?

VLMs are evaluated using datasets that contain:

| Component | Description | Example |
|---|---|---|
| **Image** | The visual input | Satellite photo after earthquake |
| **Question** | A text question about the image | "How many buildings are damaged?" |
| **Ground Truth Answer** | The correct human-annotated answer | "7 buildings" |
| **Model Answer** | What the VLM actually outputs | "6 buildings" |

### Types of answers

**Closed-ended answers** — limited set of possible answers:
- Yes / No
- Multiple choice (A, B, C, D)
- Fixed categories (none / mild / severe / destroyed)

**Open-ended answers** — free text responses:
- Descriptive sentences
- Counts or numbers
- Short phrases

---

## Evaluation Tasks for VLMs

### 1. Visual Question Answering (VQA)
The model is asked a question about an image and must produce an answer.
- *"What type of disaster occurred here?"*
- *"Is the bridge intact or collapsed?"*

### 2. Image Captioning
The model generates a free-text description of an image.
- *"Describe what you see in this satellite image."*

### 3. Damage Assessment
The model classifies the level of damage visible in an image.
- Categories: `no damage` / `minor damage` / `major damage` / `destroyed`

### 4. Counting / Reasoning
The model counts objects or reasons about quantities.
- *"How many vehicles are stranded in the flooded road?"*

---

## Evaluation Metrics

Metrics are how we measure how good or bad a model's answer is compared to the correct answer.

### For Closed-ended / Classification Tasks

#### Accuracy
The simplest metric — percentage of correct answers.
```
Accuracy = (Number of correct answers) / (Total number of questions) × 100
```
**Example:** Model answered 85 out of 100 questions correctly → Accuracy = 85%

#### Precision, Recall and F1-Score
Used when classes are imbalanced (e.g. very few "destroyed" buildings vs many "intact" ones).

- **Precision:** Of all the times the model said "damaged", how often was it right?
- **Recall:** Of all truly damaged buildings, how many did the model catch?
- **F1-Score:** The balance between Precision and Recall

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

### For Open-ended / Text Generation Tasks

#### BLEU Score (Bilingual Evaluation Understudy)
Measures how much the model's answer overlaps with the reference answer word by word.
- Score ranges from 0 to 1 (higher = better)
- **Limitation:** Doesn't handle paraphrasing well

**Example:**
- Ground truth: *"The building is severely damaged"*
- Model output: *"The structure is heavily destroyed"*
- BLEU score would be LOW even though the meaning is the same

#### ROUGE Score
Similar to BLEU but focuses on recall — how much of the reference answer appears in the model's output.
- Commonly used for longer text answers

#### METEOR
More flexible than BLEU — accounts for synonyms and paraphrasing.
- Better for evaluating descriptive answers

### For Counting / Numerical Tasks

#### Mean Absolute Error (MAE)
Measures the average difference between predicted and actual numbers.
```
MAE = average of |predicted - actual|
```
**Example:** Model predicted 5 damaged buildings, actual was 7 → error = 2

---

## Evaluation Pipeline (How it Works in Practice)

```
Dataset (images + questions + ground truth answers)
        ↓
VLM Model receives image + question
        ↓
Model generates answer
        ↓
Answer compared to ground truth
        ↓
Metrics computed (Accuracy, F1, BLEU, etc.)
        ↓
Results logged and compared across models
```

---

## Challenges in VLM Evaluation

### 1. Open-ended answers are hard to evaluate automatically
A model saying *"the road is flooded"* and *"there is water covering the road"* mean the same thing but score differently with simple metrics like BLEU.

### 2. Class imbalance in disaster datasets
In real disaster imagery, most areas are undamaged. This means a model that always says "no damage" can still achieve high accuracy — but it's useless in practice. F1-score helps address this.

### 3. Subjectivity in annotations
Human annotators may disagree on the level of damage. This introduces noise into the ground truth labels.

### 4. Cross-dataset generalization
A model that performs well on one disaster dataset (e.g. floods in Europe) may perform poorly on another (e.g. earthquakes in Asia) due to differences in geography, image resolution, and disaster type.

---

## Summary

| Task Type | Common Metrics |
|---|---|
| Classification / Damage Assessment | Accuracy, F1-Score, Precision, Recall |
| Visual Question Answering (closed) | Accuracy |
| Visual Question Answering (open) | BLEU, ROUGE, METEOR |
| Counting / Numerical | MAE, Accuracy |
| Captioning | BLEU, ROUGE, METEOR |
