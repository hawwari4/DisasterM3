# DisasterM3 Repository Analysis

## 1. Current Repository Structure

```
DisasterM3/
├── README.md
├── __init__.py
├── models/
│   └── __init__.py
├── pyscripts/
│   ├── __init__.py
│   └── run_vllm.py
├── analysis.md
├── evaluation_methodology.md
└── vision_tasks.md
```
The repository contains only two functional files. `models/models.py` defines three model configuration classes (`QwenVL`, `InternVL`, `Llava`) and a `build_model_config()` factory function. `pyscripts/run_vllm.py` is a monolithic script that handles everything else: dataset loading, prompt construction, model inference, and result saving, all in one place.

---

## 2. Code Organization Analysis

The model abstraction in `models.py` is the strongest part of the codebase. It defines a clean abstract base class `ModelConfig` with three concrete implementations. Each class configures vLLM engine arguments and implements `get_prompt_from_question(messages)` to convert a standard message list into a model-specific prompt. Adding a new model only requires adding one new class.

The problem lives in `run_vllm.py`. It handles prompt templates, dataset loading, batch construction, model initialization, the inference loop, result saving, and post-processing, all in roughly 200 lines with no separation between concerns. This makes it impossible to extend or test any one part without touching the entire script.

---

## 3. Is the Framework Tied to a Specific Dataset?

The framework is completely tied to DisasterM3. The coupling appears in three specific places.

**Hardcoded subset names.** The function `get_messages_from_data()` checks for DisasterM3-specific task names by string comparison. A different dataset would fall through all branches without matching anything.

```python
if subset in ["bearing_body", "building_damage_counting", "disaster_type", "road_damage_counting"]:
    ...
elif subset in ["landuse", "relational_reasoning_qa"]:
    ...
elif subset in ["caption", "recovery"]:
    ...
```

**Hardcoded field names.** Inside each branch, the function reads DisasterM3-specific JSON keys directly. A dataset like EarthVQA or MONITRS uses different field names and would cause a `KeyError` crash immediately.

```python
data_dict["pre_image_path"]
data_dict["post_image_path"]
data_dict["prompts"]
data_dict["options_str"]
```

**Hardcoded image paths.** The image directory structure is assumed globally and is specific to how DisasterM3 organizes its files.

```python
image_path = join(f"{PROJECT_ROOT}/data", "images", data_dict["pre_image_path"])
```

To add another dataset without redesigning the code, a developer would need to add new `elif` branches, manually map the new dataset's field names, write new prompt templates, and adjust the path logic. Every new dataset requires editing the core script, which is not a scalable design.

---

## 4. Identified Limitations

| # | Limitation | Impact |
|---|---|---|
| 1 | Dataset coupling | Cannot run any dataset other than DisasterM3 without modifying core code. |
| 2 | No evaluation layer | Metrics are never computed. The framework only saves raw prediction files. |
| 3 | No configuration system | All parameters are CLI arguments with no reproducible experiment configs. |
| 4 | No experiment tracking | Results are flat `.jsonl` files with no structured logging or metadata. |
| 5 | Monolithic script | Seven responsibilities in one file makes testing or extending any part difficult. |

---

## 5. Proposed Modular Redesign

The redesign separates all responsibilities into independent modules following a clean pipeline.

```
Dataset -> Model Runner -> Evaluator -> Experiment Tracker
```

### Target Structure

```
framework/
├── configs/
├── datasets/
│   ├── base.py
│   ├── disasterm3.py
│   └── earthvqa.py
├── models/
│   ├── base.py
│   └── qwen_runner.py
├── evaluation/
│   ├── base.py
│   └── vqa.py
├── experiments/
│   ├── runner.py
│   └── tracker.py
└── main.py
```

### How the Coupling Is Resolved

A `BaseDataset` abstract class is introduced with two methods. `load()` reads the dataset's own file format and `get_messages()` returns a standardized message list. The rest of the pipeline never sees dataset-specific field names. Adding a new dataset means creating one new class file without touching any other code.

```python
class BaseDataset(ABC):
    def load(self) -> List[Dict]:
        raise NotImplementedError

    def get_messages(self, item: Dict) -> List[Dict]:
        raise NotImplementedError
```

The same pattern applies to models and evaluators through `BaseModelRunner` and `BaseEvaluator`. Switching models or tasks requires only changing the YAML configuration file, not the scripts.

### What Is Reused from DisasterM3

The three model config classes and their `get_prompt_from_question()` methods are directly reused inside the new runner wrappers. The vLLM inference loop and partial-resume logic are kept as-is. The prompt templates are moved into each dataset class rather than stored globally.

