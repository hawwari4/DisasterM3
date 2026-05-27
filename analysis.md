# DisasterM3 Repository Analysis

## 1. Current Repository Structure

```
DisasterM3/
├── disaster_m3/
│   ├── pyscripts/
│   │   ├── run_vllm.py        # Main inference script
│   │   └── models.py          # Model configurations
│   └── eval/                  # Evaluation scripts
├── data/                      # Dataset JSON files + images
├── results/                   # Output predictions
└── README.md
```

---

## 2. Code Organization Analysis

### What exists
- `models.py` — defines model configs for QwenVL, InternVL, and Llava
- `run_vllm.py` — handles data loading, inference, and saving results
- Evaluation scripts handle metric computation per task

### Key observations
- All logic lives in two main scripts with no separation of concerns
- Dataset loading, prompt formatting, model execution, and result saving are all mixed inside `run_vllm.py`
- No base classes or abstractions for datasets or evaluators
- No configuration file system (YAML/JSON) — all parameters passed as CLI arguments
- No experiment tracking integration

---

## 3. Is the Framework Tied to a Specific Dataset?

**Yes — heavily tied to DisasterM3.**

The clearest evidence is in `get_messages_from_data()` in `run_vllm.py`:

```python
if subset in ["bearing_body", "building_damage_counting", "disaster_type", ...]:
    # DisasterM3-specific logic
elif subset in ["landuse", "relational_reasoning_qa"]:
    # More DisasterM3-specific logic
elif subset in ["caption", "recovery"]:
    # More DisasterM3-specific logic
else:
    raise ValueError('Unknown subset {}'.format(subset))
```

Every branch is hardcoded for DisasterM3 subsets. To add a new dataset like EarthVQA or MONITRS, you would need to:
- Add new `elif` branches inside this function
- Hardcode new prompt templates in `prompt_libs`
- Manually handle new image path formats
- Modify the main script logic

This means **the dataset and the execution logic are tightly coupled** — changing one requires modifying the other.

---

## 4. Identified Limitations

| Limitation | Impact |
|---|---|
| No dataset abstraction | Cannot plug in a new dataset without editing core scripts |
| No model abstraction layer | Model configs exist but aren't called through a unified interface |
| No evaluator abstraction | Evaluation logic is scattered and not reusable |
| No config-driven execution | Experiment setup requires CLI args, not a clean config file |
| No experiment tracking | Results saved as raw `.jsonl` files, no comparison dashboard |
| Hardcoded prompt templates | Prompts are embedded in the script, not configurable |

---

## 5. Proposed Modular Redesign

### Core Principle
```
Dataset → Model Runner → Evaluator → Experiment Tracker
```

### Proposed Structure
```
framework/
├── configs/                  # YAML config files per experiment
├── datasets/
│   ├── base.py               # Abstract BaseDataset class
│   ├── disasterm3.py         # DisasterM3 adapter
│   ├── earthvqa.py           # EarthVQA adapter
│   └── monitrs.py            # MONITRS adapter
├── models/
│   ├── base.py               # Abstract BaseModel class
│   ├── qwen_runner.py        # QwenVL runner
│   └── internvl_runner.py    # InternVL runner
├── evaluation/
│   ├── base.py               # Abstract BaseEvaluator class
│   ├── vqa.py                # VQA metrics (Accuracy, F1)
│   └── damage_assessment.py  # Damage-specific metrics
├── experiments/
│   ├── runner.py             # Orchestrates the pipeline
│   └── tracker.py            # MLflow / W&B integration
└── main.py                   # Entry point — reads config and runs
```

### How this resolves dataset/model coupling

Currently:
- Dataset format is assumed inside `run_vllm.py`
- Adding a dataset = editing the core script

After redesign:
- Each dataset implements `BaseDataset.load()` independently
- The runner calls `dataset.load()` without knowing which dataset it is
- Switching datasets = changing one line in a YAML config file

```yaml
# Example config
dataset: earthvqa
model: qwen_runner
evaluator: vqa
tracker: mlflow
```

### What is reused from DisasterM3
- `models.py` model config classes (QwenVL, InternVL, Llava) → adapted into model runners
- Prompt template structure → moved into dataset adapters
- vLLM inference engine usage → kept as-is inside model runners

### What limitations are being addressed
- Tight dataset coupling → resolved via `BaseDataset` abstraction
- No config system → resolved via YAML-driven execution
- No experiment tracking → resolved via MLflow/W&B integration
- Mixed concerns in one script → resolved by separating into dataset / model / evaluator layers
