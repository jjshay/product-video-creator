#!/usr/bin/env python3
"""Marketing Demo - Product Video Creator"""
import time
import sys

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
    console = Console()
except ImportError:
    print("Run: pip install rich")
    sys.exit(1)

def pause(seconds=2):
    time.sleep(seconds)

def clear():
    console.clear()

# SCENE 1: Hook
clear()
console.print("\n" * 5)
console.print("[bold yellow]         VIDEO GETS 10X MORE ENGAGEMENT[/bold yellow]", justify="center")
pause(2)

# SCENE 2: Problem
clear()
console.print("\n" * 3)
console.print(Panel("""
[bold red]BUT VIDEO IS HARD:[/bold red]

   • Filming takes hours
   • Editing software complex
   • Hiring videographers expensive
   • You only have PHOTOS

[dim]What if photos BECAME video?[/dim]
""", title="❌ No Time for Video Production", border_style="red", width=60), justify="center")
pause(3)

# SCENE 3: Solution
clear()
console.print("\n" * 3)
console.print(Panel("""
[bold green]PHOTOS → CINEMATIC VIDEO:[/bold green]

   ✓ Ken Burns pan & zoom effect
   ✓ Smooth transitions
   ✓ Professional 45-second video
   ✓ Perfect for eBay & social

[bold]Drop photos. Get video.[/bold]
""", title="✅ Product Video Creator", border_style="green", width=60), justify="center")
pause(3)

# SCENE 4: Timeline
clear()
console.print("\n\n")
console.print("[bold cyan]              🎬 YOUR VIDEO TIMELINE[/bold cyan]", justify="center")
console.print()
pause(1)

console.print("""
[bold]0s        15s       30s       45s[/bold]
│─────────│─────────│─────────│
[gold1]██████[/gold1][cyan]████[/cyan][cyan]████[/cyan][cyan]████[/cyan][magenta]███[/magenta][cyan]████[/cyan][gold1]█████[/gold1][green]████[/green][gold1]████████[/gold1]

[gold1]█[/gold1] Opening   [cyan]█[/cyan] Details   [magenta]█[/magenta] Quote   [green]█[/green] Badge
""", justify="center")
pause(3)

# SCENE 5: Rendering
clear()
console.print("\n\n")
console.print("[bold magenta]              ⚡ RENDERING VIDEO...[/bold magenta]", justify="center")
console.print()

for pct in [10, 25, 50, 75, 100]:
    bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
    console.clear()
    console.print("\n\n")
    console.print("[bold magenta]              ⚡ RENDERING VIDEO...[/bold magenta]", justify="center")
    console.print()
    console.print(f"[cyan]              [{bar}] {pct}%[/cyan]", justify="center")
    pause(0.5)

pause(1)

# SCENE 6: Result
clear()
console.print("\n" * 2)
console.print(Panel("""
[bold green]
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║            ▶  VIDEO READY!                ║
    ║                                           ║
    ║         product_video.mp4                 ║
    ║                                           ║
    ║    Duration: 45 seconds                   ║
    ║    Quality:  1920x1080 @ 30fps            ║
    ║    Size:     12.4 MB                      ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
[/bold green]
""", title="🎥 EXPORT COMPLETE", border_style="green", width=55), justify="center")
pause(3)

# SCENE 7: CTA
clear()
console.print("\n" * 4)
console.print("[bold yellow]          ⭐ TURN PHOTOS INTO VIDEO ⭐[/bold yellow]", justify="center")
console.print()
console.print("[bold white]         github.com/jjshay/product-video-creator[/bold white]", justify="center")
console.print()
console.print("[dim]                      python demo.py[/dim]", justify="center")
pause(3)
