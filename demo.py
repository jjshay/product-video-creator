#!/usr/bin/env python3
"""
Product Video Creator Demo
Demonstrates Ken Burns video generation with rich visual output.

Run: python demo.py
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow")
    from PIL import Image, ImageDraw

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


def print_header(text: str) -> None:
    if RICH_AVAILABLE:
        console.print()
        console.rule(f"[bold gold1]{text}[/bold gold1]", style="gold1")
        console.print()
    else:
        print(f"\n{'='*60}\n {text}\n{'='*60}\n")


def show_banner() -> None:
    if RICH_AVAILABLE:
        banner = """
[bold cyan]╔═══════════════════════════════════════════════════════════════════╗
║[/bold cyan] [bold gold1] ____                _            _    __     ___     _            [/bold gold1][bold cyan]║
║[/bold cyan] [bold gold1]|  _ \ _ __ ___   __| |_   _  ___| |_  \ \   / (_) __| | ___  ___  [/bold gold1][bold cyan]║
║[/bold cyan] [bold gold1]| |_) | '__/ _ \ / _` | | | |/ __| __|  \ \ / /| |/ _` |/ _ \/ _ \ [/bold gold1][bold cyan]║
║[/bold cyan] [bold gold1]|  __/| | | (_) | (_| | |_| | (__| |_    \ V / | | (_| |  __/ (_) |[/bold gold1][bold cyan]║
║[/bold cyan] [bold gold1]|_|   |_|  \___/ \__,_|\__,_|\___|\__|    \_/  |_|\__,_|\___|\___/ [/bold gold1][bold cyan]║
║[/bold cyan]                                                                       [bold cyan]║
║[/bold cyan]              [bold white]Ken Burns Style Videos from Still Images[/bold white]              [bold cyan]║
╚═══════════════════════════════════════════════════════════════════╝[/bold cyan]
"""
        console.print(banner)
    else:
        print("\n" + "="*60 + "\n  PRODUCT VIDEO CREATOR\n" + "="*60)


def create_sample_artwork() -> Dict[str, Image.Image]:
    print_header("CREATING SAMPLE ARTWORK")

    artwork = Image.new('RGB', (800, 1000), '#FAFAFA')
    draw = ImageDraw.Draw(artwork)
    draw.ellipse([100, 150, 400, 450], fill='#E74C3C')
    draw.rectangle([350, 400, 700, 800], fill='#3498DB')
    draw.polygon([(400, 100), (650, 350), (200, 400)], fill='#F1C40F')
    draw.text((650, 950), "Artist '24", fill='#2C3E50')

    w, h = artwork.size
    crops = {
        'full': artwork.copy(),
        'top_left': artwork.crop((0, 0, w//2, h//2)),
        'top_right': artwork.crop((w//2, 0, w, h//2)),
        'center': artwork.crop((w//4, h//4, 3*w//4, 3*h//4)),
        'signature': artwork.crop((int(w*0.6), int(h*0.85), w, h)),
    }

    if RICH_AVAILABLE:
        table = Table(title="🖼️ Generated Crops", box=box.ROUNDED)
        table.add_column("Crop", style="cyan")
        table.add_column("Size", style="gold1")
        table.add_column("Use")
        for name, crop in crops.items():
            table.add_row(name, f"{crop.size[0]}x{crop.size[1]}", "Video segment")
        console.print(table)
    else:
        for name, crop in crops.items():
            print(f"  {name}: {crop.size}")

    return crops


def visualize_timeline() -> None:
    print_header("VIDEO TIMELINE")

    segments = [
        ("Opening", 5, "gold1"), ("Detail 1", 4, "cyan"), ("Detail 2", 4, "cyan"),
        ("Detail 3", 4, "cyan"), ("Quote", 3, "magenta"), ("Signature", 4, "cyan"),
        ("Full Art", 5, "gold1"), ("Badge", 4, "green"), ("Closing", 8, "gold1"),
    ]

    if RICH_AVAILABLE:
        timeline = ""
        for name, dur, color in segments:
            timeline += f"[{color}]{'█' * (dur * 2)}[/{color}]"
        console.print(f"  {timeline}\n")

        table = Table(title="🎬 Video Segments", box=box.ROUNDED)
        table.add_column("#", width=3)
        table.add_column("Segment", style="cyan")
        table.add_column("Duration")
        table.add_column("Visual")

        for i, (name, dur, color) in enumerate(segments, 1):
            bar = f"[{color}]{'█' * dur}[/{color}]{'░' * (8 - dur)}"
            table.add_row(str(i), name, f"{dur}s", bar)
        console.print(table)

        total = sum(s[1] for s in segments)
        console.print(f"\n[dim]Total: {total}s @ 30fps = {total * 30} frames[/dim]")
    else:
        for name, dur, _ in segments:
            print(f"  {name}: {dur}s")


def simulate_rendering(crops: Dict[str, Image.Image]) -> None:
    print_header("FRAME GENERATION")

    total_frames = 45 * 30

    if RICH_AVAILABLE:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                      BarColumn(), TaskProgressColumn(), console=console) as progress:
            task = progress.add_task("[gold1]Rendering...", total=100)
            for i in range(100):
                time.sleep(0.02)
                progress.update(task, advance=1, description=f"[gold1]Frame {int(i * 13.5)}/{total_frames}")

        table = Table(title="🎥 Ken Burns Keyframes", box=box.ROUNDED)
        table.add_column("Frame", justify="right")
        table.add_column("Zoom")
        table.add_column("Effect")

        keyframes = [(0, "1.0x", "Start"), (150, "1.3x", "Zoom in"), (600, "2.0x", "Signature"),
                     (900, "1.2x", "Zoom out"), (1200, "1.0x", "Final")]
        for frame, zoom, effect in keyframes:
            table.add_row(str(frame), zoom, effect)
        console.print(table)
    else:
        print(f"Rendering {total_frames} frames...")


def save_outputs(crops: Dict[str, Image.Image]) -> Path:
    print_header("SAVING OUTPUTS")

    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)

    for name, crop in list(crops.items())[:3]:
        crop.save(output_dir / f"crop_{name}.jpg", quality=95)

    if RICH_AVAILABLE:
        console.print(f"[bold green]✓[/bold green] Files saved to [cyan]{output_dir}/[/cyan]")
    else:
        print(f"Saved to {output_dir}/")

    return output_dir


def main() -> None:
    show_banner()

    if RICH_AVAILABLE:
        console.print("[dim]This demo shows Ken Burns video creation concept.[/dim]\n")

    crops = create_sample_artwork()
    visualize_timeline()
    simulate_rendering(crops)
    save_outputs(crops)

    print_header("SUMMARY")
    if RICH_AVAILABLE:
        console.print(Panel("""
[cyan]Input:[/cyan]  8 product crops
[cyan]Output:[/cyan] 45-second Ken Burns video

[bold]Specs:[/bold] 1920x1080 @ 30fps = 1,350 frames

[bold gold1]Next Steps:[/bold gold1]
  1. Install FFmpeg
  2. Run: [cyan]python create_product_videos.py[/cyan]
""", title="🎬 Results", border_style="cyan", box=box.ROUNDED))

    print_header("DEMO COMPLETE")


if __name__ == "__main__":
    main()
