#!/usr/bin/env python3
"""
Product Video Creator Demo
Demonstrates Ken Burns video generation concept.

Run: python demo.py
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow")
    from PIL import Image, ImageDraw, ImageFont, ImageFilter


def print_header(text):
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}\n")


# Art quotes for video overlays
ART_QUOTES = [
    "Own a piece of history",
    "Invest in timeless art",
    "Elevate your space",
    "Museum-quality artwork",
    "Certified authentic",
    "Limited edition excellence"
]


def create_sample_artwork():
    """Create sample artwork crops"""
    print("Creating sample artwork images...")

    crops = {}

    # Main artwork
    main = Image.new('RGB', (800, 1000), '#F5F5F5')
    draw = ImageDraw.Draw(main)
    draw.ellipse([100, 150, 400, 450], fill='#E74C3C')
    draw.rectangle([350, 400, 700, 800], fill='#3498DB')
    draw.polygon([(400, 100), (650, 350), (200, 400)], fill='#F1C40F')
    draw.text((650, 950), "Artist '24", fill='#2C3E50')
    crops['full'] = main

    # Top left detail
    crops['top_left'] = main.crop((0, 0, 400, 500))

    # Top right detail
    crops['top_right'] = main.crop((400, 0, 800, 500))

    # Signature detail
    crops['signature'] = main.crop((500, 850, 800, 1000))

    # Center detail
    crops['center'] = main.crop((200, 300, 600, 700))

    for name, img in crops.items():
        print(f"   Created: {name} ({img.size[0]}x{img.size[1]})")

    return crops


def simulate_ken_burns_frame(image, zoom, pan_x, pan_y, frame_size=(1920, 1080)):
    """Simulate a single Ken Burns frame"""
    w, h = image.size
    target_w, target_h = frame_size

    # Calculate zoomed size
    zoom_w = int(w * zoom)
    zoom_h = int(h * zoom)

    # Calculate crop area based on pan
    crop_x = int((zoom_w - target_w) * pan_x)
    crop_y = int((zoom_h - target_h) * pan_y)

    # Clamp values
    crop_x = max(0, min(crop_x, zoom_w - target_w))
    crop_y = max(0, min(crop_y, zoom_h - target_h))

    return {
        'zoom': zoom,
        'pan_x': pan_x,
        'pan_y': pan_y,
        'crop_area': (crop_x, crop_y, crop_x + target_w, crop_y + target_h)
    }


def visualize_video_timeline():
    """Show the video timeline structure"""
    print_header("VIDEO TIMELINE (45 seconds)")

    segments = [
        ("Opening", 5, "Full artwork zoom in", "1.0 → 1.3x zoom"),
        ("Detail 1", 4, "Top left corner", "Pan left to right"),
        ("Detail 2", 4, "Top right corner", "Pan right to left"),
        ("Detail 3", 4, "Center texture", "Slow zoom in"),
        ("Quote", 3, '"Own a piece of history"', "Text overlay"),
        ("Detail 4", 4, "Signature closeup", "Hold + subtle zoom"),
        ("Full Art", 5, "Complete artwork", "Zoom out reveal"),
        ("Auth Badge", 4, "Authenticity seal", "Fade in overlay"),
        ("Detail 5", 4, "Bottom detail", "Final pan"),
        ("Closing", 8, "Logo + CTA", "Fade to black"),
    ]

    total = 0
    print(f"{'Segment':<12} {'Time':<8} {'Content':<25} {'Effect':<20}")
    print("-" * 70)

    for name, duration, content, effect in segments:
        time_range = f"{total}s-{total+duration}s"
        print(f"{name:<12} {time_range:<8} {content:<25} {effect:<20}")
        total += duration

    print("-" * 70)
    print(f"{'TOTAL':<12} {total}s")


def simulate_frame_generation(crops):
    """Simulate generating video frames"""
    print_header("FRAME GENERATION SIMULATION")

    fps = 30
    duration = 45
    total_frames = fps * duration

    print(f"Video settings:")
    print(f"   Resolution: 1920x1080")
    print(f"   FPS: {fps}")
    print(f"   Duration: {duration} seconds")
    print(f"   Total frames: {total_frames}")
    print()

    # Simulate Ken Burns parameters for each segment
    segments = [
        ("Opening", 150, crops['full'], 1.0, 1.3, 0.5, 0.3),
        ("Detail 1", 120, crops['top_left'], 1.2, 1.4, 0.0, 0.5),
        ("Detail 2", 120, crops['top_right'], 1.3, 1.5, 1.0, 0.5),
        ("Detail 3", 120, crops['center'], 1.1, 1.4, 0.5, 0.5),
        ("Quote", 90, crops['full'], 1.2, 1.2, 0.5, 0.5),
        ("Detail 4", 120, crops['signature'], 1.5, 1.8, 0.5, 0.5),
        ("Full Art", 150, crops['full'], 1.3, 1.0, 0.5, 0.5),
        ("Auth Badge", 120, crops['full'], 1.0, 1.0, 0.5, 0.5),
        ("Detail 5", 120, crops['top_left'], 1.2, 1.3, 0.5, 0.8),
        ("Closing", 240, crops['full'], 1.0, 1.0, 0.5, 0.5),
    ]

    print("Segment breakdown:")
    for name, frames, _, start_zoom, end_zoom, start_pan, end_pan in segments:
        print(f"\n   {name} ({frames} frames):")
        print(f"      Zoom: {start_zoom}x → {end_zoom}x")
        print(f"      Pan: {start_pan:.1f} → {end_pan:.1f}")

        # Show first and last frame params
        frame_1 = simulate_ken_burns_frame(crops['full'], start_zoom, start_pan, 0.5)
        frame_n = simulate_ken_burns_frame(crops['full'], end_zoom, end_pan, 0.5)
        print(f"      Frame 1 crop: {frame_1['crop_area']}")
        print(f"      Frame {frames} crop: {frame_n['crop_area']}")


def create_storyboard(crops):
    """Create a visual storyboard"""
    print_header("CREATING STORYBOARD")

    # Create 4x2 grid storyboard
    cell_w, cell_h = 400, 225
    storyboard = Image.new('RGB', (cell_w * 4, cell_h * 2 + 100), '#1a1a1a')
    draw = ImageDraw.Draw(storyboard)

    # Add title
    draw.text((20, 20), "PRODUCT VIDEO STORYBOARD", fill='#FFFFFF')
    draw.text((20, 50), "Ken Burns Style - 45 seconds", fill='#888888')

    frames = [
        ("1. Opening", crops['full']),
        ("2. Detail", crops['top_left']),
        ("3. Detail", crops['top_right']),
        ("4. Center", crops['center']),
        ("5. Quote", crops['full']),
        ("6. Signature", crops['signature']),
        ("7. Full Art", crops['full']),
        ("8. Closing", crops['full']),
    ]

    for i, (label, img) in enumerate(frames):
        row = i // 4
        col = i % 4

        x = col * cell_w
        y = 100 + row * cell_h

        # Resize and paste
        thumb = img.copy()
        thumb.thumbnail((cell_w - 20, cell_h - 30))
        paste_x = x + (cell_w - thumb.size[0]) // 2
        paste_y = y + 20

        storyboard.paste(thumb, (paste_x, paste_y))

        # Add label
        draw.text((x + 10, y + 5), label, fill='#FFFFFF')

    return storyboard


def save_outputs(crops, storyboard):
    """Save demo outputs"""
    print_header("SAVING OUTPUTS")

    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)

    # Save storyboard
    storyboard.save(output_dir / "storyboard.jpg", quality=95)
    print("   Saved: storyboard.jpg")

    # Save sample crops
    for name, crop in crops.items():
        filename = f"sample_{name}.jpg"
        crop.save(output_dir / filename, quality=95)
        print(f"   Saved: {filename}")

    # Create a "poster" frame
    poster = crops['full'].copy()
    poster = poster.resize((1920, int(1920 * poster.size[1] / poster.size[0])))
    poster_draw = ImageDraw.Draw(poster)
    poster_draw.rectangle([0, poster.size[1]-100, poster.size[0], poster.size[1]], fill='#000000')
    poster_draw.text((50, poster.size[1]-70), "PLAY VIDEO", fill='#FFFFFF')
    poster.save(output_dir / "video_poster.jpg", quality=95)
    print("   Saved: video_poster.jpg")

    return output_dir


def main():
    print_header("PRODUCT VIDEO CREATOR - DEMO")

    print("This demo shows how Ken Burns videos are generated")
    print("from product photos. (Actual video requires OpenCV/FFmpeg)\n")

    # Create sample images
    crops = create_sample_artwork()

    # Show timeline
    visualize_video_timeline()

    # Simulate frame generation
    simulate_frame_generation(crops)

    # Create storyboard
    storyboard = create_storyboard(crops)

    # Save outputs
    output_dir = save_outputs(crops, storyboard)

    print_header("SUMMARY")
    print("Demo created:")
    print("   - Storyboard showing video sequence")
    print("   - Sample product crops")
    print("   - Video poster frame")
    print(f"\nOutput: {output_dir}/")

    print_header("TO CREATE REAL VIDEOS")
    print("1. Install FFmpeg: brew install ffmpeg")
    print("2. Install OpenCV: pip install opencv-python")
    print("3. Run: python create_product_videos.py")

    print_header("DEMO COMPLETE")


if __name__ == "__main__":
    main()
