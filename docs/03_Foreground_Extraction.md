# Foreground Extraction using Background Subtraction

## Introduction

Foreground extraction is a crucial step in any gait analysis system. Before we can analyze how a person walks, we first need to isolate the moving subject from the background. This ensures that irrelevant information such as static objects, lighting variations, or environmental noise does not interfere with motion analysis.

In this project, we use background subtraction techniques to extract the human silhouette from video frames. This processed output becomes the foundation for further steps like feature extraction and gait pattern analysis.

---

## What is Background Subtraction?

Background subtraction is a computer vision technique used to separate moving objects (foreground) from a static scene (background).

The basic idea is simple:

- Maintain a model of the background
- Compare each incoming frame with this model
- Identify pixels that differ significantly → mark them as foreground

This works especially well for surveillance-style or static camera setups, which is ideal for gait analysis.

---

## Method Used: MOG2 (Mixture of Gaussians)

We use the **MOG2 (Mixture of Gaussians Version 2)** algorithm provided by OpenCV.

### Why MOG2?

- Adapts to gradual lighting changes
- Handles dynamic backgrounds (like moving leaves or shadows)
- Automatically updates the background model over time
- Detects shadows (optional feature)

Instead of treating each pixel as static, MOG2 models each pixel as a mixture of Gaussian distributions, allowing flexibility in real-world conditions.

---

## Implementation Steps

### 1. Initialize Background Subtractor

```python
import cv2

backSub = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=16,
    detectShadows=True
)
```

### 2. Process Video Frames

Each frame from the input video is passed through the subtractor:

```python
ret, frame = cap.read()
fgMask = backSub.apply(frame)
```

- `fgMask` contains the extracted foreground
- White pixels → moving object
- Black pixels → background

### 3. Post-processing

Raw masks often contain noise. To improve quality:

```python
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel)
fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, kernel)
```

**Purpose:**
- Opening removes small noise
- Closing fills gaps in the detected object

### 4. Extract Silhouette

We focus on the largest contour (assumed to be the person):

```python
contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    largest_contour = max(contours, key=cv2.contourArea)
    mask = cv2.drawContours(
        np.zeros_like(fgMask),
        [largest_contour],
        -1,
        255,
        thickness=cv2.FILLED
    )
```

This produces a clean silhouette of the walking subject.

---

## Output

After processing, we obtain:

- ✅ Binary foreground mask
- ✅ Clean human silhouette
- ✅ Reduced background noise

This output is then used for:

- Pose estimation
- Gait cycle detection
- Feature extraction

---

## Challenges and Limitations

While effective, background subtraction has some limitations:

- Sensitive to sudden lighting changes
- Shadows may be detected as part of the foreground
- Requires a relatively static camera
- Struggles with overlapping objects

To mitigate these:

- Morphological operations are applied
- Shadow detection is enabled in MOG2
- Proper threshold tuning is used

---

## Conclusion

Foreground extraction using background subtraction provides a reliable and efficient way to isolate the walking subject in gait analysis. By using MOG2 and applying post-processing techniques, we achieve a clean representation of human motion that is suitable for further analysis.

This step acts as the gateway between raw video input and meaningful gait insights, making it one of the most critical components of the pipeline.