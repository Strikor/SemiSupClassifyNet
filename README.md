# SemiSupClassifyNet

# RapidEyes - Incremental Unsupervised Image Clustering & Classification

A research effort to reduce human labeling demands by iteratively refining image embeddings and clusters in an **incremental** or **streaming** environment. This project uses **Siamese Triplet Networks**, **self-supervised warm-up (SimCLR)**, **HDBSCAN clustering**, and a novel **“gravity retraining”** process to organize unlabeled images with minimal manual intervention.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Key Features](#key-features)  
3. [Technical Overview](#technical-overview)  
4. [Usage](#usage)  
5. [File Structure](#file-structure)  
6. [Experiments & Results](#experiments--results)  
7. [Contributing](#contributing)  
8. [License](#license)

---

## Project Overview

Human-led image labeling is expensive and slow, but many real-world tasks can’t proceed without labeled datasets. **RapidEyes** addresses this issue by dynamically clustering large unlabeled image sets, refining cluster boundaries over time, and continuously improving a learned embedding representation to discover and classify new classes with limited human input. 

**Core Goals:**

- **Reduce Labeling Costs**: Exploit inherent structure in image data to cluster unlabeled samples.  
- **Online Streaming**: Assign new images on the fly and retrain embeddings as the dataset grows.  
- **Scalable Approach**: Combine self-supervised warm-up, metric learning, and an iterative “gravity” step for large-scale applications.

---

## Key Features

- **Self-Supervised Warm-Up (SimCLR)**: Learns initial image representations using a contrastive objective (NT-Xent loss).  
- **Siamese Triplet Network**: Fine-tunes the encoder via triplet loss, producing highly discriminative embeddings.  
- **HDBSCAN Clustering**: Discovers clusters without specifying the number of classes, automatically handling noise/outliers.  
- **Incremental Streaming**: Continuously accepts new images, assigning them to existing clusters or spawning new ones if needed.  
- **Gravity Retraining**: Iteratively updates embeddings by “pulling” images closer to their assigned cluster centers.  
- **Cluster Pruning**: Removes or merges clusters that remain too small or incoherent.  
- **Evaluation Metrics**: Monitors Adjusted Rand Index (ARI), Normalized Mutual Information (NMI), cluster purity, and multi-label accuracy.

---

## Technical Overview

### 1. **Self-Supervised Warm-Up (SimCLR)**  
- **Projection Head**: The encoder’s output is fed into a small “projection” MLP. This helps the model focus on semantic features while the projection layer handles specifics of contrastive optimization.  
- **NT-Xent Loss**: Normalized Temperature-scaled Cross-Entropy. It uses pairs of augmented images, pushing matching views together and pushing non-matching views apart in the embedding space.

### 2. **Siamese Triplet Network**  
- **Anchor-Positive-Negative**: We refine the encoder with a triplet loss—pulling anchor and positive close, while pushing the negative away.  
- **Unit-Sphere Normalization**: We often normalize embeddings to stabilize distances (focusing on angular separation rather than magnitude).

### 3. **HDBSCAN Clustering**  
- **Automatic Cluster Discovery**: Finds clusters of varied densities, naturally identifies outliers as noise (-1).  
- **Initial Baseline**: We cluster a subset (e.g., 5K unlabeled images) to bootstrap broad categories.

### 4. **Incremental / Streaming Logic**  
- **Assigning New Images**: For each incoming image, compute its embedding, locate the nearest centroid, and either add it to that cluster or create a new one if it’s too far from existing clusters.  
- **Gravity Retraining**: Periodically run a small training loop that “pulls” images closer to cluster centroids, refining the embedding space and improving classification consistency over time.  
- **Pruning**: Clusters that remain too small are flagged as noise or merged, reducing spurious outliers.

### 5. **Evaluation & Visualization**  
- **Metrics**: ARI and NMI gauge how well cluster assignments match true labels (if partially known).  
- **Multi-Label Purity**: Identifies one best cluster for each class and measures how many samples of that class end up in that cluster vs. elsewhere.  
- **Visualization**: We project embeddings to 2D using PCA (linear reduction), UMAP (non-linear manifold approximation), or t-SNE (probabilistic neighbor embedding) to visually inspect cluster separations.

---

## Usage

1. **Open `RapidEyes.ipynb`**: All code resides in a single Jupyter notebook.  
2. **Install Dependencies**:  
   ```bash
   pip install -r requirements.txt
3. **SimCLR Warm-Up**: Run initial cells that perform SimCLR training (NT-Xent) to get a base encoder.
4. **Triplet Loss Fine-Tuning**: Move on to the triplet training cells, refining embeddings with anchor-positive-negative logic.
5. **Initial Clustering**: Use HDBSCAN on a 5K subset from CIFAR-100 (or another dataset) to form coarse clusters.
6. **Streaming / Incremental**: Repeatedly add new images, run a “gravity” retrain cycle, and optionally prune small clusters.
7. **Evaluate**: Use the provided methods (e.g. evaluate_class_accuracy(manager), plot_class_accuracy(manager)) to measure cluster purity, ARI, and NMI.
8. **Visualize**: The final cells show how to run PCA, UMAP, and t-SNE to confirm cluster separations. 

---

File Structure
Since code is consolidated into a single Jupyter notebook, the repository might look like this:

bash
Copy
RapidEyes/
├── data/                      # (Optional) dataset folder
├── RapidEyes.ipynb            # The main notebook containing all code & experiments
├── requirements.txt           # Python dependencies
└── README.md

RapidEyes.ipynb includes:
  SimCLR Warm-Up
  Triplet Network Fine-Tuning
  HDBSCAN Clustering
  Incremental Streaming (gravity retrain, pruning, etc.)
  Evaluation & Visualization cells

---

**Experiments & Results**
1. **CIFAR-100 Subset**: Showed successful grouping of 10 chosen classes with minimal labeling required. ARI  improved from ~0.2 to ~0.4 after multiple gravity retrain cycles.
2. **Scalability**: The streaming approach handled incremental data efficiently, without re-running full clustering.
3. **Embedding Quality**: t-SNE and UMAP plots indicated well-separated clusters for major classes.

---

**License**
Distributed under the MIT License. See LICENSE for details.
Enjoy building your incremental, unsupervised clustering pipeline with RapidEyes!
