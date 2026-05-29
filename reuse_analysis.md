# Reuse Analysis: MONITRS Dataset

## Introduction

MONITRS (Multimodal Observations of Natural Incidents Through Remote Sensing) presents a novel approach to disaster monitoring by combining temporal satellite imagery with natural language annotations derived from news articles.

This dataset addresses a critical gap in existing resources: the lack of fine-grained temporal understanding for disaster progression. MONITRS also introduces a scalable data curation pipeline that leverages public records and media coverage instead of relying solely on expert annotation.

This analysis identifies one reusable design pattern from MONITRS and explains how it integrates into the proposed modular evaluation framework.

---

## Reusable Design Pattern: The Temporal Event Expansion Pipeline

The most valuable pattern in MONITRS is its **Temporal Event Expansion** approach for dataset loading. This pattern separates three distinct concerns:

1. Event-level metadata aggregation
2. Temporal image sequence handling
3. Question-answer sample generation

MONITRS does not treat each image as an independent sample.The loading logic then expands this structure by creating one standardized sample per QA pair, while preserving references to the full temporal sequence.

![MONITRS Temporal Event Expansion Pipeline](https://github.com/user-attachments/assets/fd354fb3-5a5d-48a0-9c2a-bda68690a9b8)

This design achieves two important goals. First, it maintains the temporal context needed for reasoning about disaster progression. Second, it produces a flat list of samples compatible with standard evaluation pipelines that expect one prediction per question.

### Why This Pattern Is Reusable

Any disaster dataset involving temporal sequences, such as wildfire tracking, flood monitoring, or post-earthquake recovery, can adopt this same structure. The separation of event metadata from sample generation allows developers to modify one component without affecting the others.

For instance, adding a new sensor type or changing the QA format requires updates only to the parsing logic, not to the core loading interface.

---

## Integration with the Proposed Framework

This pattern fits naturally into the modular framework through the `BaseDataset` abstraction defined in `datasets/base.py`. The `MONITRSDataset` class implements the required `load()` method, which returns a list of standardized dictionaries. Each dictionary contains fields such as:

- `id`
- `question`
- `answer`
- `image_path` — points to a primary image for model input
- `image_paths` — stores the full temporal sequence

This dual-field approach allows the framework to support both single-image and multi-image models without code changes.

The pattern also aligns with the configuration-driven execution design. By specifying `dataset: monitrs` in a YAML config file, the framework automatically selects the appropriate adapter. The rest of the pipeline — model runner, evaluator, and experiment tracker — remains unchanged.

As a result, adding MONITRS support does not require rewriting evaluation logic or modifying model interfaces, which is exactly what the internship project aims to achieve.

---

## Conclusion

MONITRS introduces a reusable design pattern that separates event-level aggregation from sample-level expansion. This pattern addresses the unique challenge of temporal disaster monitoring while maintaining compatibility with standard evaluation workflows.

By implementing this pattern in `datasets/monitrs.py`, the proposed framework gains the ability to support temporal datasets without sacrificing modularity. Adopting such patterns enables researchers to benchmark models across diverse disaster scenarios with minimal engineering overhead.
