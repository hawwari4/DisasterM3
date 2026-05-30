# Execution Notes: DisasterM3 Benchmark Script

**Date**: 2025-05-30

**Environment**: Google Colab (T4 GPU, 16GB VRAM)

**Dataset**: Kingdrone-Junjue/DisasterM3 (Hugging Face)

**Script**: `disaster_m3/pyscripts/run_vllm.py`

---

## Summary

The DisasterM3 environment was successfully set up on Google Colab. The official repository was cloned and 5 real samples were loaded from the Hugging Face dataset using streaming mode. Proper input messages for Qwen2.5-VL were constructed and the 3B model was successfully loaded in float16 precision. Inference was run on a test sample and the correct answer matching the ground truth was obtained, proving the pipeline logic works end-to-end.

---

## Dependencies Installed

- `transformers` (dev branch)
- `vllm==0.6.3`
- `torch`
- `datasets`

---

## Execution Results

### GPU Detection

![GPU Info](https://github.com/user-attachments/assets/8d51fcde-8b33-4aad-af7b-480e285b1c87)

### Model Loading

![Model Loaded](https://github.com/user-attachments/assets/dbbbeaa7-35f8-4df7-b724-8da1d19082f1)

### Inference Output

![Result](https://github.com/user-attachments/assets/f6b8e543-9171-4e28-ada0-8cd0ab61db86)


## Issues & Limitations

1. Full-scale inference is blocked by severe hardware constraints, as VLMs require 24GB or more of GPU VRAM to process high-resolution satellite images, far exceeding standard cloud free tiers.
2. The 41GB dataset size and lack of built-in streaming support make local or constrained environment execution impractical without manual workarounds.
3. The original codebase is tightly coupled to DisasterM3's specific file structure and hardcoded paths, requiring significant refactoring to support modular, configuration-driven evaluation across multiple datasets.
