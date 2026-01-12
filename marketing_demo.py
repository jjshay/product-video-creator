#!/usr/bin/env python3
"""Product Video Creator - Marketing Demo"""
import time
import sys

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.align import Align
    from rich import box
except ImportError:
    print("Run: pip install rich")
    sys.exit(1)

console = Console()

def pause(s=1.5):
    time.sleep(s)

def step(text):
    console.print(f"\n[bold white on #1a1a2e]  {text}  [/]\n")
    pause(0.8)

# INTRO
console.clear()
console.print()
intro = Panel(
    Align.center("[bold yellow]PRODUCT VIDEO CREATOR[/]\n\n[white]Ken Burns Videos from Product Photos[/]"),
    border_style="cyan",
    width=60,
    padding=(1, 2)
)
console.print(intro)
pause(2)

# STEP 1
step("STEP 1: LOAD PRODUCT IMAGES (8 CROPS)")

console.print("[dim]$[/] python create_video.py [cyan]./artwork_crops/[/]\n")
pause(1)

images = [
    ("artwork_full.jpg", "3000x2400", "Main shot"),
    ("artwork_top_left.jpg", "1000x1000", "Detail"),
    ("artwork_center.jpg", "1200x1200", "Texture"),
    ("artwork_signature.jpg", "800x400", "Signature"),
]

for name, size, desc in images:
    console.print(f"  [green]>[/] {name} [dim]({size}) - {desc}[/]")
    pause(0.1)

console.print(f"  [dim]... 4 more loaded[/]")
console.print(f"\n  [cyan]8 images loaded successfully[/]")
pause(1.5)

# STEP 2
step("STEP 2: BUILD VIDEO TIMELINE (45 SECONDS)")

timeline = Table(box=box.ROUNDED, width=55)
timeline.add_column("Segment", style="white")
timeline.add_column("Duration", justify="center")
timeline.add_column("Effect", style="dim")

timeline.add_row("Opening (Full Art)", "5s", "Zoom in")
timeline.add_row("Detail Shots (4x)", "16s", "Pan & zoom")
timeline.add_row("Quote Overlay", "3s", "Fade text")
timeline.add_row("Texture Detail", "4s", "Pan across")
timeline.add_row("Full Art Reveal", "5s", "Zoom out")
timeline.add_row("Authenticity Badge", "4s", "Fade COA")
timeline.add_row("Closing + CTA", "8s", "Logo + text")
timeline.add_row("[bold]TOTAL[/]", "[bold]45s[/]", "")

console.print(timeline)
pause(1.5)

# STEP 3
step("STEP 3: COMPUTE KEN BURNS MOTION")

motions = [
    ("Segment 1", "Zoom 1.0x → 1.3x"),
    ("Segment 2", "Pan X: 0 → +200px"),
    ("Segment 3", "Zoom 1.0x → 1.4x"),
    ("Segment 4", "Pan Y: 0 → +150px"),
    ("Segment 5", "Zoom 1.5x → 1.0x"),
]

for seg, motion in motions:
    console.print(f"  [green]>[/] {seg}: [cyan]{motion}[/]")
    pause(0.15)

console.print(f"  [dim]... 3 more segments computed[/]")
pause(1)

# STEP 4
step("STEP 4: ADD TEXT OVERLAYS")

overlays = [
    ("Art Quote", "\"Own a piece of history\""),
    ("Artist Name", "Pablo Picasso (1881-1973)"),
    ("Title", "Woman with Yellow Hair, 1931"),
    ("CTA", "View Listing →"),
]

for name, text in overlays:
    console.print(f"  [green]>[/] {name}: [cyan]{text}[/]")
    pause(0.2)

pause(1)

# STEP 5
step("STEP 5: RENDER VIDEO (FFMPEG)")

console.print("  [dim]Resolution:[/] 1920x1080 (Full HD)")
console.print("  [dim]Frame Rate:[/] 30 fps")
console.print("  [dim]Codec:[/]      H.264 (libx264)\n")

# Progress bar
total_frames = 1350
for i in range(0, 101, 5):
    bar_len = int(i / 100 * 35)
    bar = "[green]" + "█" * bar_len + "[/][dim]" + "░" * (35 - bar_len) + "[/]"
    frames = int(i / 100 * total_frames)
    console.print(f"\r  {bar} [cyan]{i}%[/] ({frames}/{total_frames})    ", end="")
    time.sleep(0.08)

console.print("\n\n  [green]Video encoding complete[/]")
pause(1)

# STEP 6
step("STEP 6: PLATFORM OPTIMIZATION")

versions = [
    ("eBay/Web", "1920x1080", "24.2 MB"),
    ("Instagram Reel", "1080x1920", "18.7 MB"),
    ("Facebook", "1280x720", "12.4 MB"),
    ("Thumbnail GIF", "1280x720", "2.1 MB"),
]

for platform, res, size in versions:
    console.print(f"  [green]>[/] {platform}: [dim]{res}, {size}[/]")
    pause(0.2)

pause(1)

# STEP 7
step("STEP 7: VIDEO COMPLETE")

output = Panel(
    Align.center(
        "[bold green]VIDEO CREATED[/]\n\n"
        "[bold]Output:[/] ./output/product_video_*.mp4\n"
        "[bold]Files:[/]  4 videos + preview GIF\n"
        "[bold]Time:[/]   23.4 seconds"
    ),
    title="[bold yellow]COMPLETE[/]",
    border_style="green",
    width=45
)
console.print(output)
pause(2)

# FOOTER
console.print()
footer = Panel(
    Align.center(
        "[dim]FFmpeg + OpenCV + Ken Burns Engine[/]\n"
        "[bold cyan]github.com/jjshay/product-video-creator[/]"
    ),
    title="[dim]Product Video Creator v1.4[/]",
    border_style="dim",
    width=50
)
console.print(footer)
pause(3)
