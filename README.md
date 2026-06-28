# Human Gait Analysis using Classical Computer Vision

A classical Computer Vision pipeline for extracting gait characteristics from walking videos using foreground segmentation, contour analysis, centroid tracking, temporal signal processing, and gait cycle detection.

Unlike deep learning-based approaches, this project relies entirely on traditional image processing techniques, making it lightweight, interpretable, and computationally efficient.

---

## Project Overview

Human gait refers to the pattern of movement during walking. The objective of this project is to analyze a person's walking motion by isolating lower-limb movement and converting it into a temporal motion signal for gait cycle detection.

The pipeline processes side-view walking videos and extracts meaningful gait information including:

- Walking Speed
- Gait Cycle Frequency
- Estimated Stride Length
- Motion Smoothness
- Number of Detected Gait Cycles

The entire implementation is built using classical Computer Vision techniques without any machine learning or pose estimation models.

---

## Features

- Background subtraction using MOG2
- Morphological noise removal
- Human contour validation
- Upper and lower body segmentation
- Centroid tracking with exponential smoothing
- Temporal lower-body motion signal generation
- Savitzky-Golay signal smoothing
- Peak-based gait cycle detection
- Gait metric estimation
- Motion visualization and trajectory tracking

---

## Processing Pipeline
Video Input

↓

Foreground Segmentation (MOG2)

↓

Morphological Filtering

↓

Contour Detection & Validation

↓

Upper-Lower Body Segmentation

↓

Lower Body Motion Extraction

↓

Temporal Motion Signal Generation

↓

Savitzky-Golay Signal Smoothing

↓

Peak Detection

↓

Gait Metric Computation

---

## Gait Metrics

The project computes several gait-related parameters:

- Walking Speed (pixel/frame)
- Gait Cycle Frequency
- Estimated Stride Length
- Motion Smoothness
- Number of Gait Cycles Detected

---

## Technologies Used

- Python
- OpenCV
- NumPy
- SciPy
- Matplotlib

---

## Repository Structure
human_gait_analysis/

│

├── dataset/

├── outputs/

├── gait_analysis.py

├── requirements.txt

├── README.md

└── sample_results/
---

## Installation

```bash
git clone https://github.com/Sukhmani4124/human_gait_analysis.git

cd human_gait_analysis

pip install -r requirements.txt
```

---

## Running the Project

```bash
python gait_analysis.py
```

Update the input video path inside the script before execution.

---

## Sample Output

The application displays:

- Real-time person tracking
- Upper and lower body segmentation
- Smoothed centroid trajectory
- Lower-body motion waveform
- Detected gait cycle peaks
- Computed gait metrics

---

## Future Improvements

- Pixel-to-real-world distance calibration
- Multi-person gait analysis
- Automatic gait anomaly detection
- Real-time webcam support
- Cross-view gait analysis

---

## Acknowledgements

This project was developed as part of a Computer Vision course using only classical image processing techniques and temporal signal analysis.
