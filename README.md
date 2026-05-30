<h2 align="center">
  <img
    src="https://github.com/Junjue-Wang/resources/blob/main/DisasterM3/icon.png?raw=true"
    alt="Disaster icon"
    height="50"
    style="vertical-align:-16px;"
  />
  DisasterM3: A Remote Sensing Vision-Language Dataset for Disaster Damage Assessment and Response
</h2>

<h5 align="center">
<a href="https://junjue-wang.github.io/homepage/">Junjue Wang*</a>,
<a href="https://weihaoxuan.com">Weihao Xuan*</a>,
Heli Qi,
<a href="https://ryuzhihao123.github.io">Zhihao Liu</a>,
Kunyi Liu, Yuhan Wu,
<a href="https://chrx97.com/">Hongruixuan Chen</a>,
<a href="https://jtrneo.github.io/">Jian Song</a>,
Junshi Xia,
<a href="https://zhuozheng.top/">Zhuo Zheng</a>,
<a href="https://naotoyokoya.com/">Naoto Yokoya†</a>
</h5>

<h5 align="center">* Equal Contributions &nbsp;&nbsp; † Corresponding Author</h5>

<p align="center">
  <a href="https://arxiv.org/abs/2505.21089"><strong>Paper</strong></a> &nbsp;|&nbsp;
  <a href="https://forms.gle/APQpmyuThh28HsJdA"><strong>Dataset</strong></a>
</p>

<div align="center">
  <img src="https://github.com/Junjue-Wang/resources/blob/main/DisasterM3/task_taxonomy.png?raw=true">
</div>

---

## Highlights

DisasterM3 includes 26,988 bi-temporal satellite images and 123k instruction pairs across 5 continents, with three core characteristics:

1. **Multi-hazard**: 36 historical disaster events with significant impacts, categorized into 10 common natural and man-made disasters.
2. **Multi-sensor**: Extreme weather during disasters often hinders optical sensor imaging, making it necessary to combine Synthetic Aperture Radar (SAR) imagery for post-disaster scenes.
3. **Multi-task**: 9 disaster-related visual perception and reasoning tasks, harnessing the full potential of VLM reasoning ability.

---

## News

- **2025/10/23** Released the DisasterM3 [instruct set](https://forms.gle/APQpmyuThh28HsJdA).
- **2025/10/17** Released the DisasterM3 [benchmark set](https://forms.gle/APQpmyuThh28HsJdA).
- **2025/09/22** Preparing the dataset and code.
- **2025/09/22** Paper accepted at **NeurIPS 2025**.

---

## Prerequisites

- Python 3.10+
- GPU with 24GB+ VRAM (for 7B models) or 80GB+ (for 78B models)
- 50+ GB free disk space

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Junjue-Wang/DisasterM3.git
cd DisasterM3

# Create and activate environment
conda create -n disasterm3 python=3.11 -y
conda activate disasterm3
```

---

## Benchmark

Run the following script to benchmark the DisasterM3 dataset.

**Qwen2.5-VL:**
```bash
python disaster_m3/pyscripts/run_vllm.py \
  --model_id Qwen/Qwen2.5-VL-7B-Instruct \
  --subset bearing_body
```

**InternVL3:**
```bash
python disaster_m3/pyscripts/run_vllm.py \
  --model_id OpenGVLab/InternVL3-78B \
  --subset report
```

---

## Dataset Download

```python
from datasets import load_dataset

ds = load_dataset("Kingdrone-Junjue/DisasterM3", split="test[:5]", streaming=True)
```

---

## Citation

If you use DisasterM3 in your research, please cite:

```bibtex
@article{wang2025disasterm3,
  title={DisasterM3: A Remote Sensing Vision-Language Dataset for Disaster Damage Assessment and Response},
  author={Wang, Junjue and Xuan, Weihao and Qi, Heli and Liu, Zhihao and Liu, Kunyi and Wu, Yuhan and Chen, Hongruixuan and Song, Jian and Xia, Junshi and Zheng, Zhuo and Yokoya, Naoto},
  booktitle={Proceedings of the Neural Information Processing Systems},
  year={2025}
}
```

---

## Acknowledgments

This dataset builds upon the following open datasets:

- **xBD dataset** by Ritwik Gupta — [Paper](https://openaccess.thecvf.com/content_CVPRW_2019/html/cv4gc/Gupta_Creating_xBD_A_Dataset_for_Assessing_Building_Damage_from_Satellite_CVPRW_2019_paper.html) | [Dataset](https://xview2.org/dataset) | License: CC BY-NC-SA 4.0
- **BRIGHT dataset** by Hongruixuan Chen — [Repository](https://github.com/ChenHongruixuan/BRIGHT) | License: CC BY-NC 4.0

---

## License

All images and annotations in DisasterM3 are available for **academic use only. Commercial use is prohibited.**

<a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Junjue-Wang/DisasterM3&type=Date)](https://www.star-history.com/#Junjue-Wang/DisasterM3&Date)
