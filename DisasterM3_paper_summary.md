# DisasterM3 Paper Summary

## Problem Statement

When disasters like earthquakes, floods, or wildfires occur, rescue teams need to quickly understand what is damaged, where, and how badly. Satellites can capture images of affected areas almost immediately, but analyzing thousands of images manually is slow and impractical during an emergency.

AI models that can look at images and answer questions, called Vision-Language Models (VLMs), could help automate this analysis. However, these models are mostly trained on everyday photos like cities, animals, and landscapes. When shown disaster satellite imagery, they struggle. They don't understand disaster-specific concepts like "debris-covered road" or "partially destroyed building," and they have difficulty comparing before and after images to assess damage.

Existing disaster datasets were too limited to fix this problem. The only available one (FloodNet) covered a single hurricane with simple yes/no questions. No dataset existed that covered multiple disaster types, multiple sensor types, or complex reasoning tasks like counting damaged buildings or writing recovery reports.

---

## Solution

The authors built DisasterM3, a large-scale remote sensing dataset designed specifically for disaster analysis. It contains:

- **26,988 satellite image pairs**, where each pair shows the same location before and after a disaster
- **123,000 question-answer pairs** covering a wide range of disaster analysis tasks
- **36 real disaster events** across 5 continents and 10 disaster types (floods, earthquakes, wildfires, explosions, tsunamis, volcanoes, tornadoes, hurricanes, landslides, and conflict)
- **Two sensor types**: optical (standard camera) and SAR (radar, which can see through clouds and bad weather)

What makes DisasterM3 different from anything before it is the combination of scale, diversity, and task complexity. It covers 9 distinct tasks organized around 5 core capabilities a rescue team would actually need:

1. **Recognition**: What type of disaster occurred? What structures are affected?
2. **Counting**: How many buildings are destroyed? What percentage of roads are flooded?
3. **Localization**: Draw exact outlines around damaged buildings or flooded roads
4. **Reasoning**: Describe spatial relationships between damaged objects
5. **Report Generation**: Write a full disaster description and provide immediate and long-term recovery advice

---

## Experiments

The paper tested 14 different VLMs on the DisasterM3 benchmark, including open-source models (LLaVA, Qwen2.5-VL, InternVL3, Kimi-VL), commercial models (GPT-4o, GPT-4.1, Claude-3), and remote sensing specialized models (GeoChat, TeoChat, EarthDial).

The main findings were:

**Even the best models struggle.** GPT-4.1 achieved only ~42% average accuracy on disaster tasks. To put this in perspective, random guessing scores 20% on some tasks, meaning even the best model is not dramatically better than chance on certain tasks.

**Bigger models perform better.** InternVL3 showed a clear trend: the 78B version (39.3%) outperformed the 14B (35.7%) and 8B (31.3%) versions. Larger models handle complex reasoning better.

**Remote sensing models are worse than general models.** Surprisingly, models specifically trained on satellite imagery (like GeoChat at 10.7%) performed worse than general-purpose VLMs. This shows that disaster understanding requires more than just satellite image knowledge; it needs disaster-specific training data.

**SAR images are much harder.** All models performed significantly worse on radar (SAR) images compared to optical ones. Increasing model size didn't help much here either, showing that SAR imagery remains an open challenge.

**Fine-tuning on DisasterM3 works well.** When four models were fine-tuned using the DisasterM3 training set, performance improved significantly across all tasks, with gains of up to +10.4% on QA tasks, +2.15 points on report generation (on a 0 to 5 scale), and +40.8% on segmentation accuracy. Fine-tuning also made models more stable across different ways of phrasing the same question.

**Counting remains tricky.** One fine-tuned model actually got worse at counting damaged buildings, which is a sign of overfitting, where the model memorizes training examples instead of learning the general skill.

---

*Summary written based on personal reading of: Wang et al., "DisasterM3: A Remote Sensing Vision-Language Dataset for Disaster Damage Assessment and Response", NeurIPS 2025.*
