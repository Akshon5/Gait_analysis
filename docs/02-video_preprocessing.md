# Video Preprocessing for Gait Analysis (Dashboard Output)

In this blog, I explain the complete preprocessing pipeline used in my Human Gait Analysis project.

Unlike a simple single-output system, my implementation generates **four synchronized video outputs**, displayed together in a dashboard format. Each video represents a different stage of preprocessing.

This multi-view visualization helps in understanding how raw data transforms step-by-step into a clean silhouette.

---

# The Four Video Outputs

My system produces the following four outputs simultaneously:

1. Original Video with ROI Detection (Green Boxes)
2. Grayscale / Enhanced Frame
3. Binary Silhouette (Black Background)
4. Final Foreground Overlay (Red Mask on Original Frame)

Each is explained below.

---

# 1. Original Video with ROI Detection (Green Boxes)

This is the raw video frame with detected regions highlighted using green bounding boxes.

### What Are These Green Boxes?

The green boxes represent **Region of Interest (ROI)** detected using contour detection after background subtraction.

### How Are They Formed?

1. Background subtraction identifies moving areas.
2. Thresholding converts frame to binary.
3. Contours are detected.
4. The largest contour (human body) is selected.
5. A bounding rectangle is drawn around it.

This technique is called:

**Foreground Detection + Contour-Based Bounding Box Extraction**

### Purpose

- Identifies the walking subject
- Tracks movement
- Eliminates irrelevant background regions

---

# 2. Grayscale / Contrast Enhanced Frame

The second video shows the grayscale version of the frame.

Sometimes Histogram Equalization is applied to improve contrast.

### Why This Step?

- Reduces color complexity
- Focuses only on intensity values
- Improves background subtraction accuracy
- Makes silhouette detection more stable under lighting variations

This step prepares the frame for reliable thresholding.

---

# 3. Binary Silhouette (Black Background)

This is the most important preprocessing output.

The frame is converted into a **binary image**:

- White → Human body
- Black → Background

### How Is It Generated?

1. Background subtraction
2. Thresholding
3. Morphological Opening (remove noise)
4. Morphological Closing (fill holes)

Elliptical kernels are used to maintain natural human body shape.

This produces a clean silhouette.

---

# 4. Final Foreground Overlay (Red Mask)

The fourth video overlays the detected foreground onto the original frame using a red mask.

### Why This Is Useful

- Visually verifies correct human detection
- Helps debug segmentation errors
- Shows alignment between original frame and extracted foreground

This confirms that preprocessing is working correctly.

---

# Why Use a 4-Video Dashboard?

Instead of showing only final silhouette, this dashboard:

- Demonstrates transparency in processing
- Helps debug errors
- Improves presentation clarity
- Makes viva explanation easier
- Shows full pipeline visually

It proves that preprocessing is not random — it is systematic and step-by-step.

---

# Summary of Techniques Used

The preprocessing pipeline uses classical Computer Vision techniques:

- Frame resizing
- Background subtraction
- Thresholding
- Contour detection
- Bounding box extraction
- Morphological operations
- Mask overlay

No deep learning segmentation was used.

This keeps the system lightweight, computationally efficient, and syllabus-aligned.

---

# Conclusion

The four synchronized video outputs clearly demonstrate how raw walking footage transforms into a structured, clean silhouette ready for gait feature extraction.

Preprocessing ensures:

- Noise reduction
- Accurate human isolation
- Stable feature extraction
- Improved gait recognition reliability

In the next blog, I will explain how features are extracted from the final silhouette.