"""
Extract 6 icons from a screenshot, remove background, recolor to teal.

Input: Screenshot with gold outline icons on dark purple background
Output: 6 individual transparent PNGs recolored to target color
"""

import cv2
import numpy as np
from PIL import Image
import sys
import os


def extract_icons(input_path, output_dir, target_color=(13, 148, 136)):
    """
    Extract icons from screenshot, make transparent, recolor.

    Args:
        input_path: Path to screenshot PNG
        output_dir: Directory to save extracted icons
        target_color: RGB tuple for recoloring (default: teal #0d9488)
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not load image at {input_path}")
        sys.exit(1)

    print(f"Image loaded: {img.shape[1]}x{img.shape[0]}")

    # Convert to HSV for gold color isolation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Isolate everything that isn't the dark purple background.
    # Convert to grayscale and threshold: purple bg is dark, icons are bright.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # The purple background is dark (~30-60), icons are bright (~140-255)
    # Use Otsu's method to find the optimal threshold automatically
    _, mask_binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Clean up with morphological close (fill small holes) then open (remove specks)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask_binary = cv2.morphologyEx(mask_binary, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask_binary = cv2.morphologyEx(mask_binary, cv2.MORPH_OPEN, kernel, iterations=1)

    # Binary alpha: fully opaque or fully transparent, no gradients
    soft_alpha = mask_binary

    # Use same mask for contour detection
    mask = mask_binary

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get bounding boxes, filter by size and aspect ratio
    # Icons are roughly square; text labels are wide and flat
    min_area = 500
    bboxes = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        aspect = w / max(h, 1)
        # Keep regions that are somewhat square (aspect 0.4 to 2.5) and large enough
        if area > min_area and 0.4 < aspect < 2.5 and h > 80:
            bboxes.append((x, y, w, h))

    print(f"Found {len(bboxes)} candidate regions")

    # Merge nearby bounding boxes (icons may have disconnected parts)
    def merge_boxes(boxes, gap=30):
        """Merge bounding boxes that are within `gap` pixels of each other."""
        if not boxes:
            return boxes

        merged = True
        while merged:
            merged = False
            new_boxes = []
            used = set()
            for i, (x1, y1, w1, h1) in enumerate(boxes):
                if i in used:
                    continue
                mx, my, mw, mh = x1, y1, w1, h1
                for j, (x2, y2, w2, h2) in enumerate(boxes):
                    if j <= i or j in used:
                        continue
                    # Check if boxes are close enough to merge
                    if (x2 < mx + mw + gap and x2 + w2 > mx - gap and
                        y2 < my + mh + gap and y2 + h2 > my - gap):
                        # Merge
                        nx = min(mx, x2)
                        ny = min(my, y2)
                        nmx = max(mx + mw, x2 + w2)
                        nmy = max(my + mh, y2 + h2)
                        mx, my, mw, mh = nx, ny, nmx - nx, nmy - ny
                        used.add(j)
                        merged = True
                new_boxes.append((mx, my, mw, mh))
                used.add(i)
            boxes = new_boxes
        return boxes

    bboxes = merge_boxes(bboxes, gap=40)
    print(f"After merging: {len(bboxes)} icon regions")

    # Sort: top row first (by y), then left to right (by x)
    bboxes.sort(key=lambda b: (b[1] // 80, b[0]))

    # Print bounding box info for debugging
    for i, (x, y, w, h) in enumerate(bboxes):
        print(f"  Icon {i+1}: pos=({x},{y}) size={w}x{h}")

    # Extract each icon
    padding = 15
    icon_names = [
        "tension-relief",
        "stress-relief",
        "cellular-homeostasis",
        "deep-meditation",
        "performance-recovery",
        "elevated-mood"
    ]

    for i, (x, y, w, h) in enumerate(bboxes):
        # Add padding
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(img.shape[1], x + w + padding)
        y2 = min(img.shape[0], y + h + padding)

        # Crop the soft alpha region
        icon_alpha = soft_alpha[y1:y2, x1:x2]

        # Create RGBA image
        height, width = icon_alpha.shape
        rgba = np.zeros((height, width, 4), dtype=np.uint8)

        # Set target color everywhere, use soft alpha for transparency
        rgba[:, :, 0] = target_color[0]  # R
        rgba[:, :, 1] = target_color[1]  # G
        rgba[:, :, 2] = target_color[2]  # B
        rgba[:, :, 3] = icon_alpha       # A (smooth anti-aliased)

        # Save
        name = icon_names[i] if i < len(icon_names) else f"icon-{i+1}"
        out_path = os.path.join(output_dir, f"{name}.png")
        pil_img = Image.fromarray(rgba, 'RGBA')
        pil_img.save(out_path)
        print(f"Saved: {out_path} ({width}x{height})")

    print(f"\nDone! {len(bboxes)} icons extracted to {output_dir}")


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else None
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"

    if not input_path:
        print("Usage: python extract_icons.py <screenshot_path> [output_dir]")
        sys.exit(1)

    extract_icons(input_path, output_dir)
