#!/usr/bin/env python3
"""
Product Video Creator - Showcase Demo
Ken Burns style marketing videos from product photos.

Run: python showcase.py
"""

import time
import sys

# Colors for terminal output
class Colors:
    GOLD = '\033[93m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.GOLD}{'='*70}")
    print(f" {text}")
    print(f"{'='*70}{Colors.END}\n")

def print_step(step, text):
    print(f"{Colors.CYAN}[STEP {step}]{Colors.END} {Colors.BOLD}{text}{Colors.END}")

def main():
    print(f"\n{Colors.GOLD}{Colors.BOLD}")
    print("    ╔═══════════════════════════════════════════════════════════════╗")
    print("    ║            PRODUCT VIDEO CREATOR - LIVE DEMO                  ║")
    print("    ║          Ken Burns Style Marketing Videos                     ║")
    print("    ╚═══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")

    time.sleep(1)

    # Input
    print(f"   {Colors.BOLD}INPUT:{Colors.END} 8 product detail images")
    print(f"   {Colors.DIM}Full artwork + 7 detail crops from art-crop-system{Colors.END}")
    print()
    time.sleep(0.5)

    # Step 1: Video Settings
    print_step(1, "VIDEO CONFIGURATION")
    print()

    settings = [
        ('Resolution', '1920 x 1080 (Full HD)'),
        ('Frame Rate', '30 fps'),
        ('Duration', '45 seconds'),
        ('Total Frames', '1,350'),
        ('Format', 'MP4 (H.264)'),
        ('Audio', 'Optional background music'),
    ]

    for label, value in settings:
        time.sleep(0.15)
        print(f"   {label:<15} {Colors.CYAN}{value}{Colors.END}")

    print()
    time.sleep(0.5)

    # Step 2: Timeline
    print_step(2, "VIDEO TIMELINE")
    print()

    segments = [
        ('Opening', '0-5s', 'Full artwork', 'Zoom 1.0x → 1.3x'),
        ('Detail 1', '5-9s', 'Top left', 'Pan left → right'),
        ('Detail 2', '9-13s', 'Top right', 'Pan right → left'),
        ('Detail 3', '13-17s', 'Center texture', 'Slow zoom in'),
        ('Quote', '17-20s', '"Own a piece of history"', 'Text overlay'),
        ('Signature', '20-24s', 'Artist signature', 'Hold + zoom'),
        ('Full Reveal', '24-29s', 'Complete artwork', 'Zoom out'),
        ('Auth Badge', '29-33s', 'Certificate overlay', 'Fade in'),
        ('Detail 4', '33-37s', 'Bottom detail', 'Final pan'),
        ('Closing', '37-45s', 'Logo + CTA', 'Fade to black'),
    ]

    print(f"   {'Segment':<12} {'Time':<10} {'Content':<25} {'Effect':<20}")
    print(f"   {'-'*70}")

    for name, time_range, content, effect in segments:
        time.sleep(0.1)
        print(f"   {name:<12} {time_range:<10} {content:<25} {effect}")

    print()
    time.sleep(0.5)

    # Step 3: Ken Burns Engine
    print_step(3, "KEN BURNS EFFECT ENGINE")
    print()

    print(f"   Calculating motion paths for each segment...")
    print()

    for i, (name, _, _, effect) in enumerate(segments[:5], 1):
        time.sleep(0.2)
        print(f"   Segment {i}: {name}")
        print(f"   ├─ Effect: {effect}")
        print(f"   ├─ Keyframes: Start → End interpolation")
        print(f"   └─ Easing: ease-in-out (smooth motion)")
        print()

    print(f"   {Colors.DIM}... (5 more segments){Colors.END}")
    print()
    time.sleep(0.5)

    # Step 4: Text Overlays
    print_step(4, "TEXT OVERLAYS")
    print()

    overlays = [
        ('"Own a piece of history"', '17-20s', 'Center, fade in/out'),
        ('Artist: Shepard Fairey', '24-29s', 'Lower third'),
        ('Certificate of Authenticity', '29-33s', 'Badge overlay'),
        ('www.gallery.com', '37-45s', 'Closing CTA'),
    ]

    for text, timing, position in overlays:
        time.sleep(0.2)
        print(f"   {Colors.GOLD}\"{text}\"{Colors.END}")
        print(f"   └─ {timing} | {position}")
        print()

    time.sleep(0.5)

    # Step 5: Rendering
    print_step(5, "RENDERING VIDEO")
    print()

    print(f"   Rendering 1,350 frames...")
    print()

    # Progress bar simulation
    for pct in [10, 25, 50, 75, 100]:
        time.sleep(0.3)
        bar_filled = pct // 5
        bar_empty = 20 - bar_filled
        bar = f"{Colors.GREEN}{'█' * bar_filled}{Colors.END}{'░' * bar_empty}"
        frames = int(1350 * pct / 100)
        print(f"\r   [{bar}] {pct:>3}% ({frames}/1350 frames)", end='')

    print()
    print()

    print(f"   {Colors.GREEN}✓{Colors.END} Video rendered: product_video.mp4")
    print(f"   {Colors.GREEN}✓{Colors.END} File size: 28.4 MB")
    print(f"   {Colors.GREEN}✓{Colors.END} Duration: 45 seconds")
    print()
    time.sleep(0.5)

    # Summary
    print_header("VIDEO CREATION COMPLETE")

    print(f"   {Colors.BOLD}Output:{Colors.END}")
    print(f"   ┌─────────────────────────────────────────────────────────────┐")
    print(f"   │ {Colors.CYAN}product_video.mp4{Colors.END}                                         │")
    print(f"   │                                                             │")
    print(f"   │ Resolution:      1920 x 1080 (Full HD)                     │")
    print(f"   │ Duration:        45 seconds                                 │")
    print(f"   │ Frame Rate:      30 fps                                     │")
    print(f"   │ File Size:       28.4 MB                                    │")
    print(f"   │ Segments:        10 Ken Burns sequences                     │")
    print(f"   │ Text Overlays:   4 branded messages                         │")
    print(f"   └─────────────────────────────────────────────────────────────┘")
    print()
    print(f"   {Colors.BOLD}Key Features:{Colors.END}")
    print(f"   • Professional Ken Burns pan & zoom effects")
    print(f"   • Smooth 30fps motion with easing")
    print(f"   • Customizable text overlays and quotes")
    print(f"   • Auto-matched background colors")
    print(f"   • Batch processing for multiple products")
    print(f"   • Google Drive upload integration")
    print()
    print(f"   {Colors.GOLD}Perfect for eBay listings, social media, and galleries{Colors.END}")
    print()
    print(f"   {Colors.BOLD}GitHub:{Colors.END} github.com/jjshay/product-video-creator")
    print()

if __name__ == "__main__":
    main()
