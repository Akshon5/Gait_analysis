import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter

# -----------------------------------
# VIDEO INPUT
# -----------------------------------
video_path = "/Users/akshon/Downloads/demo (1).mp4"
cap = cv2.VideoCapture(video_path)


# MOG2 BACKGROUND SUBTRACTOR Applied on RAW frame (no preprocessing before)


fgbg = cv2.createBackgroundSubtractorMOG2(history=500,varThreshold=50,
    detectShadows=True
)

kernel       = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
merge_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))

# DATA STORES

motion_values       = []
lower_motion_values = []
lower_heights       = []
smooth_centroids    = []
symmetry_values     = []
confidence_flags    = []
recent_heights      = []   # tracks recent bounding box heights for stability

frame_count = 0
ALPHA       = 0.4   # exponential smoothing factor


# CONTOUR VALIDATION THRESHOLDS

MIN_AREA         = 8000   # full body blob must be large
MIN_ASPECT       = 1.3    # person is clearly taller than wide
MIN_SOLIDITY     = 0.25   # person blob is solid not scattered
MAX_JUMP         = 120    # max centroid jump before smoothing kicks in
STABLE_WINDOW    = 10     # frames to average height over
MIN_HEIGHT_RATIO = 0.5    # box must be >= 50% of recent average height

# -----------------------------------
# CONTOUR VALIDATOR
# Returns True if contour looks like a person
# Checks: area, aspect ratio, solidity
# All classical CV — no deep learning
# -----------------------------------
def is_valid_person_contour(cnt):
    area = cv2.contourArea(cnt)
    if area < MIN_AREA:
        return False

    x, y, w, h = cv2.boundingRect(cnt)

    # Aspect ratio — person is always taller than wide
    aspect_ratio = h / float(w) if w > 0 else 0
    if aspect_ratio < MIN_ASPECT:
        return False

    # Solidity — person blob should be reasonably solid
    # Scattered background blobs have low solidity
    hull      = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    solidity  = area / hull_area if hull_area > 0 else 0
    if solidity < MIN_SOLIDITY:
        return False

    return True

# -----------------------------------
# MAIN LOOP
# -----------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1


    fgmask = fgbg.apply(frame)
    fgmask_raw_save = fgmask.copy()


    if frame_count < 20:
        cv2.imshow("Motion Mask", fgmask)
        cv2.imshow("Tracking", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        continue


    # STEP 2: POST-MASK PREPROCESSING
    # Threshold → removes shadows (127), keeps foreground (255)
    # Open → removes small noise blobs
    # Close → fills gaps inside silhouette

    _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN,  kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    fgmask_clean_save = fgmask.copy()

    # STEP 3: WHOLE BODY MOTION VALUE

    motion_value = np.sum(fgmask > 0)
    motion_values.append(motion_value)


    # STEP 4: MERGE NEARBY CONTOURS

    merged_mask = cv2.dilate(fgmask, merge_kernel, iterations=2)
    merged_mask = cv2.erode(merged_mask, merge_kernel, iterations=1)
    merged_mask_save = merged_mask.copy()
    contours, _ = cv2.findContours(
        merged_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    # STEP 5: VALIDATE CONTOURS
    # Pick largest contour that passes all validation checks

    best_contour = None
    max_area     = 0

    for cnt in contours:
        if is_valid_person_contour(cnt):
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area     = area
                best_contour = cnt


    # STEP 6: STABILITY CHECK
    # Reject boxes that are too small vs recent history
    # Filters partial detections (just face, just feet)
    # when person is entering/exiting frame

    lower_motion    = 0
    lower_height    = 0
    raw_centroid    = None
    high_confidence = False

    if best_contour is not None:
        x, y, w, h = cv2.boundingRect(best_contour)

        # Check height stability
        if len(recent_heights) >= STABLE_WINDOW:
            avg_recent_h = np.mean(recent_heights[-STABLE_WINDOW:])
            if h < avg_recent_h * MIN_HEIGHT_RATIO:
                # Box too small — partial detection, reject
                best_contour = None

    if best_contour is not None:
        x, y, w, h = cv2.boundingRect(best_contour)
        recent_heights.append(h)


        split_y = y + int(h * 0.45)


        cv2.rectangle(frame, (x, y), (x + w, split_y), (0, 255, 0), 2)
        cv2.putText(frame, "Upper", (x, max(y - 5, 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


        cv2.rectangle(frame, (x, split_y), (x + w, y + h), (0, 255, 255), 2)
        cv2.putText(frame, "Lower", (x, split_y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        # Lower body mask crop — leg region only

        lower_mask_region = fgmask[split_y:y + h, x:x + w]
        lower_motion      = np.sum(lower_mask_region > 0)
        lower_height      = lower_mask_region.shape[0]

        # Raw centroid = center of full bounding box
        raw_centroid    = (x + w // 2, y + h // 2)
        high_confidence = True

    else:
        # No valid detection this frame
        recent_heights.append(
            recent_heights[-1] if recent_heights else 0
        )

    lower_motion_values.append(lower_motion)
    lower_heights.append(lower_height)
    confidence_flags.append(high_confidence)

    # STEP 7: CENTROID SMOOTHING
    # Exponential smoothing: new = alpha*raw + (1-alpha)*prev
    # Falls back to last known position on failed frames
    # Large jumps blended slowly (person re-entering frame)

    if len(smooth_centroids) == 0:
        if raw_centroid is not None:
            smooth_centroids.append(raw_centroid)
        else:
            smooth_centroids.append((0, 0))
    else:
        prev = smooth_centroids[-1]

        if raw_centroid is None:
            # No detection — hold last position
            smooth_centroids.append(prev)
        else:
            dist = np.linalg.norm(
                np.array(raw_centroid) - np.array(prev)
            )
            if dist > MAX_JUMP:
                # Large jump — person re-entering, blend slowly
                blended = (
                    int(ALPHA * raw_centroid[0] + (1 - ALPHA) * prev[0]),
                    int(ALPHA * raw_centroid[1] + (1 - ALPHA) * prev[1])
                )
                smooth_centroids.append(blended)
            else:
                # Normal exponential smoothing
                smoothed = (
                    int(ALPHA * raw_centroid[0] + (1 - ALPHA) * prev[0]),
                    int(ALPHA * raw_centroid[1] + (1 - ALPHA) * prev[1])
                )
                smooth_centroids.append(smoothed)


    # STEP 8: DRAW CENTROID + TRAJECTORY
    # Only draws on confident detections
    # Prevents garbage trajectory from bad frames
    # -----------------------------------
    current = smooth_centroids[-1]

    if current != (0, 0) and high_confidence:
        cv2.circle(frame, current, 5, (0, 0, 255), -1)

    for i in range(1, len(smooth_centroids)):
        prev_conf = confidence_flags[i - 1] if i - 1 < len(confidence_flags) else False
        curr_conf = confidence_flags[i]     if i     < len(confidence_flags) else False
        if prev_conf and curr_conf:
            if smooth_centroids[i] != (0, 0) and smooth_centroids[i-1] != (0, 0):
                cv2.line(frame,
                         smooth_centroids[i-1],
                         smooth_centroids[i],
                         (255, 0, 0), 2)

    # -----------------------------------
    # STEP 9: SYMMETRY
    # Left vs right pixel count in full mask
    # -----------------------------------
    fh, fw = fgmask.shape
    left_px  = np.sum(fgmask[:, :fw // 2] > 0)
    right_px = np.sum(fgmask[:, fw // 2:] > 0)
    symmetry_values.append(abs(left_px - right_px))

    # -----------------------------------
    # DISPLAY
    # -----------------------------------
    cv2.putText(frame, f"Motion: {motion_value}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame, f"Lower Motion: {lower_motion}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    status_text  = "Person: YES" if high_confidence else "Person: NO"
    status_color = (0, 255, 0)  if high_confidence else (0, 0, 255)
    cv2.putText(frame, status_text, (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)

    cv2.imshow("Motion Mask", fgmask)
    cv2.imshow("Tracking", frame)
    if frame_count == 50:
        base = "/Users/akshon/3rdsemproj/"
        np.save(base + "saved_frame.npy", frame)
        np.save(base + "saved_fgmask_raw.npy", fgmask_raw_save)
        np.save(base + "saved_fgmask_clean.npy", fgmask_clean_save)
        np.save(base + "saved_merged.npy", merged_mask_save)
        np.save(base + "saved_contour.npy",
                best_contour if best_contour is not None else np.array([]))
        np.save(base + "saved_split_y.npy", np.array([split_y]))
        print("Saved at frame 50")


    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# POST PROCESSING +GAIT METRICS


smooth_centroids = np.array(smooth_centroids)
valid_mask       = (smooth_centroids != [0, 0]).any(axis=1)
smooth_centroids = smooth_centroids[valid_mask]

motion_values       = np.array(motion_values)
lower_motion_values = np.array(lower_motion_values)


# SAVITZKY-GOLAY SMOOTHING
# Preserves peak shape better than moving average

if len(lower_motion_values) > 15:
    lower_motion_smooth = savgol_filter(lower_motion_values, 9, 3)
else:
    lower_motion_smooth = lower_motion_values


# GAIT METRIC 1: WALKING SPEED
# Mean horizontal displacement per frame (px/frame)

if len(smooth_centroids) > 1:
    dx            = np.diff(smooth_centroids[:, 0])
    walking_speed = np.mean(np.abs(dx))
else:
    walking_speed = 0


# GAIT METRIC 2: GAIT CYCLE FREQUENCY
# Peaks in lower body motion = full gait cycles (heel strike to heel strike)
# prominence=50 filters shallow noise peaks
# distance=15 prevents double counting same cycle

peaks, _ = find_peaks(
    lower_motion_smooth,
    distance=15,
    prominence=25
)
gait_cycle_freq = len(peaks) / len(lower_motion_smooth) if len(lower_motion_smooth) > 0 else 0

# -----------------------------------
# GAIT METRIC 3: STRIDE LENGTH
# Estimated from lower body bounding box width at each peak frame.
# At peak motion, legs are maximally spread — box width reflects stride span.
# avg_stride = mean of lower-body box widths at detected gait cycle peaks
# -----------------------------------
lower_heights = np.array(lower_heights)
stride_widths = []

if len(peaks) > 0 and best_contour is not None:
    x, y, w, h = cv2.boundingRect(best_contour)
    body_width = w  # last known bounding box width as reference

if len(peaks) > 0:
    for p in peaks:
        if p < len(lower_motion_values):
            # At peak, lower motion is high → legs maximally apart
            # Approximate stride as proportion of body width scaled by motion intensity
            motion_at_peak  = lower_motion_values[p]
            motion_max      = np.max(lower_motion_values) if np.max(lower_motion_values) > 0 else 1
            stride_estimate = (motion_at_peak / motion_max) * body_width if 'body_width' in dir() else 0
            stride_widths.append(stride_estimate)

avg_stride = float(np.mean(stride_widths)) if stride_widths else 0.0

"""# -----------------------------------
# GAIT METRIC 4: SYMMETRY
# -----------------------------------
symmetry_score = np.mean(symmetry_values) if symmetry_values else 0"""

# -----------------------------------
# GAIT METRIC 5: MOTION SMOOTHNESS
# -----------------------------------
motion_diff = np.diff(motion_values)
smoothness  = np.std(motion_diff) if len(motion_diff) > 0 else 0

# -----------------------------------
# PRINT RESULTS
# -----------------------------------
print("\GAIT METRICS")
print(f"Walking Speed       : {walking_speed:.4f}  px/frame")
print(f"Gait Cycle Freq     : {gait_cycle_freq/2:.4f}  cycles/frame")
print(f"Stride Length       : {avg_stride:.4f}  px")
"""print(f"Symmetry Score      : {symmetry_score:.4f}  (lower = more symmetric)")"""
print(f"Motion Smoothness   : {smoothness:.4f}  (lower = smoother)")
print(f"Gait Cycles Detected: {len(peaks)/2}")
print("\n")

# -----------------------------------
# GRAPH
# -----------------------------------
plt.figure(figsize=(10, 4))
plt.plot(lower_motion_smooth, label="Lower Body Motion (smoothed)", color='blue')
plt.plot(peaks, lower_motion_smooth[peaks], "rx", markersize=10, label="Detected Steps")
plt.legend()
plt.title("Step Detection via Lower Body Motion Signal")
plt.xlabel("Frame")
plt.ylabel("Foreground Pixel Count (Lower Body)")
plt.tight_layout()
plt.show()
