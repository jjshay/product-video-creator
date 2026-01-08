#!/usr/bin/env python3
"""
Product Video Generator - Ken Burns Style
Creates high-end art gallery videos from product crops
Uploads to Google Drive PRODUCT VIDEOS folder
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
import pandas as pd
from colorsys import rgb_to_hsv

# Google Drive folder for PRODUCT VIDEOS
PRODUCT_VIDEOS_FOLDER_ID = '1xHTK9cYGEzqxZAogl3m-dMj9zDCmKTQr'

# Directories
OUTPUT_DIR = Path("/Users/johnshay/3DSELLERS/product_videos")
CROPS_DIR = Path("/Users/johnshay/3DSELLERS/processed_crops")
AUTHENTICITY_IMAGE = Path("/Users/johnshay/3DSELLERS/authenticity_slide.jpg")

# Video settings
VIDEO_DURATION = 45  # seconds (increased from 35)
FPS = 30
WIDTH = 1920
HEIGHT = 1080

# Inspiring quotes for art buyers
ART_QUOTES = [
    "Own a piece of history",
    "Invest in timeless art",
    "Elevate your space",
    "Curated for collectors",
    "Authenticated & verified",
    "Limited edition excellence",
    "Art that tells a story",
    "Museum-quality artwork",
    "Collectible masterpiece",
    "Gallery-worthy investment",
    "Rare find for discerning collectors",
    "Transform your walls",
    "Certified authentic artwork",
    "Hand-signed by the artist",
    "Ready to display",
    "Professionally curated",
    "A statement piece",
    "Timeless pop culture art"
]


def get_drive_service():
    """Authenticate and return Google Drive service"""
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


def get_average_brightness(image):
    """Calculate average brightness of image (0-1)"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Get average brightness
    avg_brightness = np.mean(gray) / 255.0

    return avg_brightness


def get_text_color(image, region=None):
    """
    Determine optimal text color (white or black) based on background
    region: (x1, y1, x2, y2) tuple to check specific area
    """
    if region:
        x1, y1, x2, y2 = region
        roi = image[y1:y2, x1:x2]
    else:
        # Check center region
        h, w = image.shape[:2]
        roi = image[h//3:2*h//3, w//3:2*w//3]

    brightness = get_average_brightness(roi)

    # Return white for dark backgrounds, black for light backgrounds
    if brightness < 0.5:
        return (255, 255, 255)  # White
    else:
        return (0, 0, 0)  # Black


def apply_ken_burns_effect(image, start_zoom=1.0, end_zoom=1.3, pan_direction='random'):
    """
    Apply Ken Burns effect to image
    Returns list of frames with smooth zoom and pan
    """
    frames = []
    duration = 4  # 4 seconds per image
    total_frames = FPS * duration

    h, w = image.shape[:2]

    # Determine pan direction
    if pan_direction == 'random':
        import random
        directions = ['topleft', 'topright', 'bottomleft', 'bottomright', 'center']
        pan_direction = random.choice(directions)

    for i in range(total_frames):
        progress = i / total_frames

        # Calculate current zoom
        current_zoom = start_zoom + (end_zoom - start_zoom) * progress

        # Calculate new dimensions
        new_w = int(w * current_zoom)
        new_h = int(h * current_zoom)

        # Resize image
        resized = cv2.resize(image, (new_w, new_h))

        # Calculate pan offset based on direction
        if pan_direction == 'topleft':
            pan_x = int((new_w - w) * progress)
            pan_y = int((new_h - h) * progress * 0.5)
        elif pan_direction == 'topright':
            pan_x = int((new_w - w) * (1 - progress))
            pan_y = int((new_h - h) * progress * 0.5)
        elif pan_direction == 'bottomleft':
            pan_x = int((new_w - w) * progress)
            pan_y = int((new_h - h) * (1 - progress * 0.5))
        elif pan_direction == 'bottomright':
            pan_x = int((new_w - w) * (1 - progress))
            pan_y = int((new_h - h) * (1 - progress * 0.5))
        else:  # center
            pan_x = int((new_w - w) * 0.5)
            pan_y = int((new_h - h) * 0.5)

        # Crop to original dimensions
        try:
            frame = resized[pan_y:pan_y+h, pan_x:pan_x+w]

            # Ensure correct size
            if frame.shape[:2] != (h, w):
                frame = cv2.resize(frame, (w, h))

            frames.append(frame)
        except:
            # Fallback to center crop if something goes wrong
            frames.append(cv2.resize(image, (w, h)))

    return frames


def add_text_overlay(frame, text, position='center', font_scale=1.5):
    """
    Add text overlay to frame with automatic color detection
    position: 'top', 'center', 'bottom'
    """
    h, w = frame.shape[:2]

    # Determine text region based on position
    if position == 'top':
        text_y = h // 6
        region = (0, 0, w, h//3)
    elif position == 'bottom':
        text_y = 5 * h // 6
        region = (0, 2*h//3, w, h)
    else:  # center
        text_y = h // 2
        region = (0, h//3, w, 2*h//3)

    # Get optimal text color
    text_color = get_text_color(frame, region)

    # Add semi-transparent background for better readability
    overlay = frame.copy()

    if position == 'top':
        cv2.rectangle(overlay, (0, 0), (w, h//4), (0, 0, 0), -1)
        alpha = 0.4
    elif position == 'bottom':
        cv2.rectangle(overlay, (0, 3*h//4), (w, h), (0, 0, 0), -1)
        alpha = 0.4
    else:
        cv2.rectangle(overlay, (w//6, h//3), (5*w//6, 2*h//3), (0, 0, 0), -1)
        alpha = 0.3

    frame = cv2.addWeighted(frame, 1-alpha, overlay, alpha, 0)

    # Add text
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, font_scale, 3)[0]
    text_x = (w - text_size[0]) // 2

    # Add shadow for depth
    shadow_offset = 3
    cv2.putText(frame, text, (text_x + shadow_offset, text_y + shadow_offset),
                font, font_scale, (0, 0, 0), 3, cv2.LINE_AA)

    # Add main text
    cv2.putText(frame, text, (text_x, text_y),
                font, font_scale, text_color, 3, cv2.LINE_AA)

    return frame


def resize_to_video_dimensions(image):
    """Resize image to 1920x1080 maintaining aspect ratio"""
    h, w = image.shape[:2]

    # Calculate scaling
    scale = min(WIDTH / w, HEIGHT / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    # Resize
    resized = cv2.resize(image, (new_w, new_h))

    # Create black canvas
    canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    # Center image on canvas
    x_offset = (WIDTH - new_w) // 2
    y_offset = (HEIGHT - new_h) // 2

    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized

    return canvas


def create_product_video(sku, crops_dir=CROPS_DIR, output_dir=OUTPUT_DIR):
    """
    Create video for a specific SKU using its cropped images
    """
    print(f"\n{'='*70}")
    print(f"CREATING VIDEO FOR SKU: {sku}")
    print(f"{'='*70}")

    # Find all crops for this SKU (excluding stock images)
    sku_folder = crops_dir / sku

    if not sku_folder.exists():
        print(f"❌ No crops found for SKU: {sku}")
        return None

    # Get all cropped images (PNG and JPG files, excluding thumbnail)
    crop_files = []
    for pattern in ["*.png", "*.jpg", "*.jpeg"]:
        for crop_file in sorted(sku_folder.glob(pattern)):
            if "THUMBNAIL" not in crop_file.name and "stock" not in crop_file.name.lower():
                crop_files.append(crop_file)

    print(f"Found {len(crop_files)} cropped images (excluding stock)")

    if len(crop_files) == 0:
        print(f"❌ No valid crops found for SKU: {sku}")
        return None

    # Prepare output
    output_dir.mkdir(exist_ok=True)
    temp_video = output_dir / f"{sku}_temp.mp4"
    final_video = output_dir / f"{sku}.mp4"

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(temp_video), fourcc, FPS, (WIDTH, HEIGHT))

    # Calculate timing
    seconds_per_crop = (VIDEO_DURATION - 3) / len(crop_files)  # Save 3 seconds for authenticity

    print(f"Duration per crop: {seconds_per_crop:.1f} seconds")

    # Process each crop with Ken Burns effect
    import random
    for idx, crop_file in enumerate(crop_files):
        print(f"  Processing {crop_file.name}...")

        # Load image
        img = cv2.imread(str(crop_file))
        if img is None:
            continue

        # Resize to video dimensions
        img = resize_to_video_dimensions(img)

        # Apply Ken Burns effect
        frames = apply_ken_burns_effect(img, start_zoom=1.0, end_zoom=1.3)

        # Add text overlay to some frames (middle of clip)
        if idx % 2 == 0:  # Add quote to every other clip
            quote = random.choice(ART_QUOTES)
            start_frame = len(frames) // 3
            end_frame = 2 * len(frames) // 3

            for i in range(start_frame, end_frame):
                frames[i] = add_text_overlay(frames[i], quote, position='bottom')

        # Write frames
        for frame in frames:
            out.write(frame)

    # Add authenticity slide (3 seconds)
    print("  Adding authenticity slide...")
    if AUTHENTICITY_IMAGE.exists():
        auth_img = cv2.imread(str(AUTHENTICITY_IMAGE))
        auth_img = resize_to_video_dimensions(auth_img)

        # Hold for 3 seconds
        for _ in range(FPS * 3):
            out.write(auth_img)

    out.release()

    # Convert to H.264 for better compatibility
    print("  Converting to H.264...")
    convert_to_h264(temp_video, final_video)

    # Clean up temp file
    if temp_video.exists():
        temp_video.unlink()

    print(f"✅ Video created: {final_video}")

    return final_video


def convert_to_h264(input_file, output_file):
    """Convert video to H.264 for better compatibility"""
    command = [
        'ffmpeg',
        '-i', str(input_file),
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-movflags', '+faststart',
        '-y',
        str(output_file)
    ]

    subprocess.run(command, capture_output=True)


def upload_to_drive(video_file, sku):
    """Upload video to Google Drive PRODUCT VIDEOS folder"""
    print(f"  Uploading to Google Drive...")

    try:
        service = get_drive_service()

        file_metadata = {
            'name': f"{sku}.mp4",
            'parents': [PRODUCT_VIDEOS_FOLDER_ID]
        }

        media = MediaFileUpload(
            str(video_file),
            mimetype='video/mp4',
            resumable=True
        )

        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        print(f"✅ Uploaded to Google Drive: {file.get('webViewLink')}")
        return file.get('id')

    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None


def process_all_products():
    """Process all products from Google Sheets"""
    print(f"\n{'='*70}")
    print("PRODUCT VIDEO GENERATOR - KEN BURNS STYLE")
    print(f"{'='*70}\n")

    # Read products from Google Sheets CSV export
    # (You can integrate with Google Sheets API or use CSV export)

    # For now, scan the crops directory for SKUs
    if not CROPS_DIR.exists():
        print(f"❌ Crops directory not found: {CROPS_DIR}")
        return

    # Get all SKU folders
    sku_folders = [d for d in CROPS_DIR.iterdir() if d.is_dir()]

    print(f"Found {len(sku_folders)} products to process\n")

    processed = 0
    for sku_folder in sku_folders:
        sku = sku_folder.name

        try:
            # Create video
            video_file = create_product_video(sku)

            if video_file and video_file.exists():
                # Upload to Google Drive
                upload_to_drive(video_file, sku)
                processed += 1

        except Exception as e:
            print(f"❌ Error processing {sku}: {e}")
            continue

    print(f"\n{'='*70}")
    print(f"✅ COMPLETED: {processed}/{len(sku_folders)} videos created")
    print(f"{'='*70}")


if __name__ == "__main__":
    # Move authenticity image to 3DSELLERS directory if not there
    if not AUTHENTICITY_IMAGE.exists():
        import shutil
        source = Path("/Users/johnshay/authenticity_slide.jpg")
        if source.exists():
            shutil.copy(source, AUTHENTICITY_IMAGE)

    # Process all products
    process_all_products()
