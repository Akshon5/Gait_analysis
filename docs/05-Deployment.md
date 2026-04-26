# Gait Analysis System using Computer Vision

## Overview

The Gait Analysis System is a computer vision-based application designed to analyze human walking patterns from video input. The system extracts meaningful gait parameters such as walking speed, stride length, gait cycle frequency, and motion smoothness using classical image processing and signal processing techniques.

This project focuses on building an efficient, lightweight, and interpretable solution without relying on deep learning, making it suitable for academic and low-resource environments.

---

## Problem Statement

Traditional gait analysis systems often require specialized hardware such as motion capture sensors or expensive clinical setups. This creates limitations in accessibility and usability.

The goal of this project is to develop a video-based gait analysis system that:
- Works with standard video input  
- Requires no specialized hardware  
- Provides quantitative gait metrics  
- Is easy to deploy and use  

---

## Methodology

The system follows a structured pipeline:

1. Video Input & Frame Extraction  
2. Background Subtraction (MOG2)  
3. Preprocessing (Thresholding & Morphological Operations)  
4. Contour Detection & Validation  
5. Bounding Box Generation  
6. Body Segmentation (Upper & Lower Body)  
7. Centroid Tracking  
8. Motion Signal Extraction  
9. Signal Smoothing (Savitzky-Golay Filter)  
10. Peak Detection  
11. Gait Parameter Calculation  

This pipeline allows the system to transform raw video into structured gait insights.

---

## Results

The system successfully detects walking patterns and generates a motion signal representing lower body movement. Peaks in this signal correspond to gait cycles, enabling accurate step detection.

The following parameters are computed:
- Walking Speed  
- Gait Cycle Frequency  
- Stride Length  
- Motion Smoothness  
- Number of Gait Cycles  

The results demonstrate that classical computer vision techniques can effectively analyze gait patterns under controlled conditions.

---

## Deployment

One of the key highlights of this project is its deployment as a web-based application using Streamlit.

Live Application:  
https://gait-analysis-cv-frontend-mhuw9emsbppgw6oqpm5bbe.streamlit.app/

### Features of the Deployed System:
- Upload walking video directly from browser  
- Toggle visualization options (bounding box, trajectory, etc.)  
- Real-time processing and visualization  
- Interactive dashboard for gait metrics  
- Graphical representation of motion signal  

This deployment makes the system easily accessible, user-friendly, and platform-independent.

---

## User Interface

The application provides a clean and intuitive interface with:
- A control panel for input and settings  
- Visualization area for processed frames  
- Dashboard for gait metrics  
- Motion signal graph for analysis  

This ensures that even non-technical users can interact with the system easily.

---

## Project Report

The project is supported by a detailed technical report that includes:

- Literature Survey of existing gait analysis methods  
- System Architecture and Design Diagrams  
- Implementation details and workflow  
- Experimental results and analysis  
- Validation of objectives  
- Conclusions and future scope  

The report ensures proper documentation of both theoretical and practical aspects of the system.

---

## Limitations

While the system performs well under controlled conditions, some limitations exist:

- Sensitive to lighting variations  
- Performance may degrade with background noise  
- Limited robustness to occlusions  
- Works best with a single subject  

---

## Future Scope

The system can be further improved by:

- Integrating deep learning-based pose estimation  
- Supporting real-time webcam input  
- Enhancing robustness to complex environments  
- Adding multi-person tracking  
- Deploying on mobile platforms  

---

## Conclusion

The Gait Analysis System demonstrates that meaningful gait insights can be extracted using classical computer vision techniques. The combination of efficient processing, interpretable outputs, and web-based deployment makes it a practical and accessible solution.

This project serves as a strong foundation for further advancements in automated gait analysis systems.