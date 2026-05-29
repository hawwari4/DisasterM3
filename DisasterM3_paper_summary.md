# DisasterM3 Paper Summary

## Problem Statement

When disasters like earthquakes, floods, or wildfires occur, rescue teams need to quickly understand what is damaged, where, and how badly. Satellites can capture images of affected areas almost immediately, but analyzing thousands of images manually is slow and impractical during an emergency.

AI models that can look at images and answer questions, called Vision-Language Models (VLMs), could help automate this analysis. However, these models are mostly trained on everyday photos like cities, animals, and landscapes. As a result, when shown disaster satellite imagery, they struggle to understand concepts like debris-covered roads or partially destroyed buildings, and have difficulty comparing before and after images to assess damage.

Unfortunately, existing disaster datasets were too limited to fix this problem. FloodNet, the only available one, covered a single hurricane with simple yes/no questions. In short, no dataset existed that covered multiple disaster types, multiple sensor types, or complex reasoning tasks like counting damaged buildings or writing recovery reports.

---

## Solution

To address this gap, the authors created DisasterM3, a large-scale remote sensing dataset designed specifically for disaster analysis. It contains 26,988 bi-temporal satellite image pairs showing the same location before and after a disaster, along with 123,000 question-answer pairs covering a wide range of analysis tasks.

The data spans 36 real disaster events across five continents and ten disaster types, including floods, earthquakes, wildfires, explosions, and tsunamis. It also includes two sensor types: optical cameras for clear weather conditions and SAR radar for cloudy or smoky environments where optical images are unavailable.

Crucially, the dataset is organized around what rescue teams actually need, covering nine distinct tasks built on five core capabilities: recognizing disaster type and affected structures, counting damaged objects, localizing damage through segmentation, reasoning about spatial relationships, and generating full disaster reports with recovery advice.

---

## Experiments and Key Findings

The authors evaluated 14 different VLMs on the DisasterM3 benchmark, including open-source models like LLaVA and Qwen2.5-VL, commercial models like GPT-4o and GPT-4.1, and remote sensing specialized models like GeoChat and TeoChat. The results revealed several important patterns.

1. Even the best models struggle with disaster tasks. GPT-4.1 achieved only about 42% average accuracy, which is not dramatically better than random guessing on some tasks.
2. Larger models generally perform better, as shown by InternVL3, where the 78B version outperformed smaller versions.
3. Models trained on satellite imagery performed worse than general-purpose VLMs, indicating that disaster understanding requires more than just satellite image knowledge.
4. All models performed significantly worse on SAR radar images compared to optical images, showing that cross-sensor understanding remains an open challenge.
5. Fine-tuning on DisasterM3 leads to substantial improvements across all tasks, with gains up to 10.4% on question answering, 2.15 points on report generation, and 40.8% on segmentation accuracy.

These results demonstrate that DisasterM3 not only identifies current model limitations but also provides the data needed to build better disaster-response AI systems.
