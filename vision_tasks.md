# Computer Vision Tasks

## Overview

Computer vision is the field of AI that enables machines to interpret and understand visual information from images or videos. The three foundational tasks are **classification**, **detection**, and **segmentation**.

---

## 1. Image Classification

**What it does:** Assigns a single label to an entire image.

**Question it answers:** *"What is in this image?"*

**Output:** A category label (e.g., "flooded area", "fire", "collapsed building")

**Example:** Given a satellite image, the model outputs: `damaged` or `not damaged`

**Key characteristic:** The model does not care *where* in the image the object is — only *what* is present.

---

## 2. Object Detection

**What it does:** Identifies *what* objects are in an image and *where* they are, using bounding boxes.

**Question it answers:** *"What is in this image, and where exactly?"*

**Output:** A set of bounding boxes, each with a class label and a confidence score.

**Example:** Given a satellite image after an earthquake, the model draws boxes around each collapsed building and labels them.

**Key characteristic:** Provides location information (x, y, width, height of each detected object).

---

## 3. Image Segmentation

**What it does:** Labels every single pixel in the image with a class.

**Question it answers:** *"What category does each pixel belong to?"*

**Output:** A pixel-level mask — each pixel is assigned a class.

There are two main types:
- **Semantic segmentation:** Every pixel of the same class gets the same label (e.g., all water pixels = blue, all road pixels = gray)
- **Instance segmentation:** Distinguishes between individual objects of the same class (e.g., building #1 vs building #2)

**Example:** Given a flood satellite image, the model colors every flooded pixel in blue, every road pixel in gray, and every building pixel in red.

**Key characteristic:** Most detailed of the three tasks — provides shape-level information for every object.

---

![alt text](<how to make - visual selection (1).png>)

## Application to Natural Disasters

These tasks become especially powerful when applied to remote sensing data (satellite/aerial imagery) of disaster zones:

### Classification in Disaster Context
- Classifying satellite tiles as **damaged** vs **undamaged** after an earthquake
- Categorizing disaster type: flood, wildfire, hurricane damage
- Used in: **DisasterM3** benchmark for damage level classification

### Detection in Disaster Context
- Detecting and localizing **collapsed buildings** in post-earthquake imagery
- Identifying **displaced vehicles**, **debris fields**, or **flooded roads**
- Enables rapid damage mapping over large geographic areas

### Segmentation in Disaster Context
- Mapping the **exact flood extent** at pixel level from satellite imagery
- Delineating **burn scars** after wildfires
- Identifying **damaged vs intact roof structures** for insurance or aid assessment
- Used in: **EarthVQA** and related benchmarks for fine-grained scene understanding

### Why These Tasks Matter for Disaster Response
Remote sensing imagery can cover thousands of square kilometers. Automating visual analysis through these tasks allows humanitarian organizations to:
- Prioritize rescue operations to the most affected areas
- Estimate the scale of damage without sending personnel into dangerous zones
- Track disaster progression over time (temporal monitoring)
- Support resource allocation for recovery efforts
