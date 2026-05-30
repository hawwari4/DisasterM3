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

![GPU Info](assets/screenshots/colab_gpu_info.png)

### Model Loading

![Model Loaded](assets/screenshots/model_loading_success.png)

### Inference Output

![Result](assets/screenshots/inference_result.png)
