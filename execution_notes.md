# Execution Notes — DisasterM3

## Environment

- OS: Windows 11
- Python: 3.11
- Hardware: Local CPU machine (no GPU)

---

## Attempted Execution

The README provides two example commands to run the benchmark:

```bash
# Qwen2.5 VL example
python disaster_m3/pyscripts/run_vllm.py --model_id Qwen/Qwen2.5-VL-7B-Instruct --subset bearing_body

# InternVL3 example
python disaster_m3/pyscripts/run_vllm.py --model_id OpenGVLab/InternVL3-78B --subset report
```

---

## Step 1: Locate Dependencies

The first step was to find a `requirements.txt` or any dependency file in the repo.

```bash
dir -Recurse *.txt
dir -Recurse *.toml
```

**Result:** No dependency files found anywhere in the repository.

**Issue:** The repository does not include a `requirements.txt`, `pyproject.toml`, or `setup.py`. There is no documented way to install the required packages.

---

## Step 2: Identify Required Dependencies from Source Code

By reading `run_vllm.py` and `models.py`, the following dependencies were identified manually:

| Package | Purpose |
|---|---|
| `vllm` | Core inference engine for running VLMs |
| `torch` | Deep learning framework |
| `transformers` | Model loading and tokenizers |
| `Pillow` | Image loading and processing |
| `tqdm` | Progress bars |
| `numpy` | Numerical operations |
| `torchvision` | Image transforms |
| `qwen_vl_utils` | Qwen-specific vision utilities |
| `decord` | Video frame extraction |

---

## Step 3: Attempt to Install Core Dependency

```bash
pip install vllm
```

**Result:** Installation fails on Windows. `vllm` is a Linux-only package and requires CUDA-compatible GPU hardware.

---

## Reproducibility Limitations

Full execution of the DisasterM3 benchmark is **not reproducible** on a standard local machine due to the following reasons:

### 1. No requirements file
The repository does not include any dependency specification file. Users must manually identify and install packages by reading the source code.

**Proposed fix:** Add a `requirements.txt` to the root of the repo.

### 2. Linux + GPU only
`vllm` — the core inference engine — only supports Linux with CUDA-compatible GPUs. Running on Windows or a CPU-only machine is not possible.

**Minimum hardware required:**
- Linux OS
- NVIDIA GPU with at least 40GB VRAM (for 7B models)
- For 78B models: 4x NVIDIA H100 GPUs

### 3. Dataset requires manual request
The DisasterM3 dataset (26,988 satellite images) is not included in the repo. It must be requested via a Google Form:
- https://forms.gle/APQpmyuThh28HsJdA

Without the dataset, no script can run even if all dependencies are installed.

### 4. No data directory structure documented
The `run_vllm.py` script expects data at:
```
PROJECT_ROOT/data/images/
PROJECT_ROOT/data/{subset}.json
```
But this structure is never documented in the README.

### 5. Model weights not included
Models like `Qwen2.5-VL-7B-Instruct` (15GB+) must be downloaded separately from HuggingFace. This requires:
- A HuggingFace account
- Sufficient disk space (15–150GB depending on model)

---

## README Issues Found

The current README is missing:

- List of required dependencies and how to install them
- Hardware requirements
- Data directory structure after downloading the dataset
- Python version requirement
- Steps to download model weights

---

## README Update

The following section should be added to `README.md` under a new **Installation** heading:

```markdown
## Installation

### Requirements
- Linux OS
- Python >= 3.9
- NVIDIA GPU with >= 40GB VRAM (for 7B models)

### Install dependencies
pip install torch torchvision transformers vllm Pillow tqdm numpy decord qwen-vl-utils

### Data setup
After downloading the dataset, place it as follows:
DisasterM3/
└── data/
    ├── bearing_body.json
    ├── images/
    │   ├── pre_*.png
    │   └── post_*.png
```

---

## Summary

| Step | Result |
|---|---|
| Find requirements file | ❌ Does not exist |
| Install vllm on Windows | ❌ Linux only |
| Access dataset | ❌ Requires form request |
| Run benchmark script | ❌ Blocked by above issues |
| Read and understand source code | ✅ Completed |
