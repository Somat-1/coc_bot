#!/usr/bin/env python3
"""
click_recorder.py – log screen-click coordinates and let the user label each one.
Requires: pip install pynput
macOS: grant Accessibility permission to your terminal / Python app.
"""

import json
import sys
from pathlib import Path
from pynput import mouse

clicks = []            # will hold dicts: {"name": str, "x": int, "y": int}
outfile = Path("clicks.json")

def on_click(x, y, button, pressed):
    if not pressed:          # ignore the release event
        return

    print(f"Clicked at: ({x}, {y})")
    label = input("Label this click (Enter = skip): ").strip() or f"click_{len(clicks)+1}"
    entry = {"name": label, "x": x, "y": y}
    clicks.append(entry)
    print(f"Recorded → {entry}\n")

    # Persist after every click so nothing is lost if you ^C out
    outfile.write_text(json.dumps(clicks, indent=2))

def main():
    print("Listening for clicks…  (Ctrl-C to exit)\n")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting – saved", len(clicks), "click(s).")
        sys.exit(0)
