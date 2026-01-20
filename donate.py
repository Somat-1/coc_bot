import os
import argparse
import sys
from utils.adb_helper import take_screenshot, tap, tap_and_hold, ensure_connection, get_selected_device
import easyocr
import cv2
import random
import time
import math

# ========== TAP DEBUGGING CLASS ==========
class TapLocation:
    def __init__(self, name, coords, description, tap_type="normal", duration_ms=None):
        self.name = name
        self.coords = coords
        self.description = description
        self.tap_type = tap_type  # "normal", "hold", "random_point"
        self.duration_ms = duration_ms

    def execute(self):
        x, y = self.coords
        print(f"[TAP] {self.name}: ({x}, {y}) - {self.description}")
        
        if self.tap_type == "hold" and self.duration_ms:
            tap_and_hold(x, y, duration_ms=self.duration_ms)
        else:
            tap(x, y)
        
        time.sleep(1)  # Brief pause between taps for visibility

# ========== ALL TAP LOCATIONS FROM MAIN.PY ==========
TAP_LOCATIONS = [
    # POST_ATTACK_TAPS
    TapLocation("Post Attack 1", (800, 850), "First post-attack recovery tap"),
    TapLocation("Post Attack 2", (97, 900), "Second post-attack recovery tap"),
    TapLocation("Post Attack 3", (250, 700), "Third post-attack recovery tap"),
    
    # Recovery taps (when zero loot detected)
    TapLocation("Recovery 1", (800, 850), "Recovery tap 1 (same as post-attack 1)"),
    TapLocation("Recovery 2", (97, 900), "Recovery tap 2 (same as post-attack 2)"),
    TapLocation("Recovery 3", (250, 700), "Recovery tap 3 (same as post-attack 3)"),
    
    # Troop icons (10 troops)
    TapLocation("Troop 1", (220, 930), "First troop icon"),
    TapLocation("Troop 2", (320, 930), "Second troop icon"),
    TapLocation("Troop 3", (420, 930), "Third troop icon"),
    TapLocation("Troop 4", (520, 930), "Fourth troop icon (first hero)"),
    TapLocation("Troop 5", (620, 930), "Fifth troop icon (second hero)"),
    TapLocation("Troop 6", (720, 930), "Sixth troop icon (third hero)"),
    TapLocation("Troop 7", (820, 930), "Seventh troop icon (fourth hero)"),
    TapLocation("Troop 8", (920, 930), "Eighth troop icon (fifth hero)"),
    TapLocation("Troop 9", (1020, 930), "Ninth troop icon (spell start)"),
    TapLocation("Troop 10", (1120, 930), "Tenth troop icon"),
    
    # Deployment locations
    TapLocation("Deploy 1", (1526, 450), "Primary deployment location"),
    TapLocation("Deploy 2", (180, 480), "Secondary deployment location"),
    
    # Spell deployment locations
    TapLocation("Spell 1", (900, 350), "Spell deployment location 1"),
    TapLocation("Spell 2", (700, 480), "Spell deployment location 2"),
    TapLocation("Spell 3", (900, 600), "Spell deployment location 3"),
    TapLocation("Spell 4", (830, 480), "Spell deployment location 4"),
    TapLocation("Spell 5", (900, 480), "Spell deployment location 5"),
    
    # Extra attack taps
    TapLocation("Extra Attack 1", (110, 790), "Extra post-attack tap 1"),
    TapLocation("Extra Attack 2", (960, 623), "Extra post-attack tap 2"),
    
    # Main navigation
    TapLocation("Next Button", (1470, 760), "Next base button"),
    
    # Debug overlay locations (for reference)
    TapLocation("Return 1", (800, 850), "Return tap 1 (debug overlay)"),
    TapLocation("Return 2", (110, 915), "Return tap 2 (debug overlay)"),
    TapLocation("Return 3", (1234, 636), "Return tap 3 (debug overlay)"),
    
    # Hold locations
    TapLocation("Troop 2 Hold", (320, 930), "Second troop with hold (2.5 seconds)", "hold", 2500),
]

# ========== TAP DEBUG FUNCTIONS ==========
def list_all_tap_locations():
    print("\nAll Tap Locations from main.py:")
    print("-" * 50)
    for i, location in enumerate(TAP_LOCATIONS, 1):
        tap_type_str = f" [{location.tap_type.upper()}]" if location.tap_type != "normal" else ""
        duration_str = f" ({location.duration_ms}ms)" if location.duration_ms else ""
        print(f"{i:2d}. {location.name:20s} ({location.coords[0]:4d}, {location.coords[1]:3d}){tap_type_str}{duration_str}")
        print(f"    {location.description}")
    print()

def test_single_tap_location(index):
    if 1 <= index <= len(TAP_LOCATIONS):
        location = TAP_LOCATIONS[index - 1]
        print(f"\nTesting location {index}: {location.name}")
        print(f"Coordinates: ({location.coords[0]}, {location.coords[1]})")
        print(f"Description: {location.description}")
        
        confirm = input("Execute this tap? (y/N): ").strip().lower()
        if confirm == 'y':
            ensure_connection()
            location.execute()
            print("✅ Tap executed!")
        else:
            print("❌ Tap cancelled.")
    else:
        print(f"Invalid location number. Please choose 1-{len(TAP_LOCATIONS)}")

def test_tap_category(category_name):
    categories = {
        'troops': [loc for loc in TAP_LOCATIONS if 'troop' in loc.name.lower()],
        'deploy': [loc for loc in TAP_LOCATIONS if 'deploy' in loc.name.lower()],
        'spells': [loc for loc in TAP_LOCATIONS if 'spell' in loc.name.lower()],
        'recovery': [loc for loc in TAP_LOCATIONS if 'recovery' in loc.name.lower() or 'post attack' in loc.name.lower()],
        'navigation': [loc for loc in TAP_LOCATIONS if 'next' in loc.name.lower() or 'return' in loc.name.lower()],
    }
    
    if category_name not in categories:
        print(f"Unknown category. Available: {', '.join(categories.keys())}")
        return
    
    locations = categories[category_name]
    if not locations:
        print(f"No locations found for category: {category_name}")
        return
    
    print(f"\nTesting {category_name.upper()} category ({len(locations)} locations):")
    for loc in locations:
        print(f"  • {loc.name}: ({loc.coords[0]}, {loc.coords[1]}) - {loc.description}")
    
    confirm = input(f"\nExecute all {len(locations)} {category_name} taps? (y/N): ").strip().lower()
    if confirm == 'y':
        ensure_connection()
        for i, location in enumerate(locations, 1):
            print(f"\n[{i}/{len(locations)}]", end=" ")
            location.execute()
        print(f"\n✅ All {category_name} taps executed!")
    else:
        print("❌ Category execution cancelled.")

def show_tap_coordinates_only():
    print("\nCoordinates Only (for copy/paste):")
    print("-" * 40)
    for location in TAP_LOCATIONS:
        print(f"({location.coords[0]}, {location.coords[1]})  # {location.name}")
    print()

# ========== ADB TARGET / RUNTAG ==========
def resolve_serial():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--serial", dest="serial", default=None,
                        help="ADB device serial (e.g., 127.0.0.1:5555)")
    args, _ = parser.parse_known_args()

    serial = args.serial or os.environ.get("ANDROID_SERIAL") or "127.0.0.1:5555"
    # Ensure child helpers see it
    os.environ["ANDROID_SERIAL"] = serial
    return serial

ADB_SERIAL = resolve_serial()
RUN_TAG = os.environ.get("RUN_TAG", "").strip()

print(f"[+] Using ADB device: {ADB_SERIAL}" + (f"  (RUN_TAG={RUN_TAG})" if RUN_TAG else ""))

# ========== CONFIG ==========
SCREEN_PATH = "screen.png"
DEBUG_OUTPUT = "donation_debug.png"

# OCR search box for "Donate" button
DONATE_OCR_BOX = (374, 817, 511, 865)
DONATE_BOX_CENTER = ((374 + 511) // 2, (817 + 865) // 2)

# Standby (keep-awake) tap rectangle (x1, y1, x2, y2) - shrunk by 10% total
STANDBY_RECT = (734, 322, 1366, 728)

# Troop donation centers: [Troop1, Troop2, Troop3, Troop4]
TROOP_DONATE_CENTERS = [
    (685, 429),        # Troop 1
    (653, 590),        # Troop 2
    (655, 746),        # Troop 3
    (685 + 50, 429)    # Troop 4 (right of Troop 1)
]

TAP_RADIUS = 15
IDLE_TAP_MIN = 120  # seconds
IDLE_TAP_MAX = 180  # seconds

TIMEOUT_DURATION = 360 * 60  # 90 minutes
START_TIME = time.time()

reader = easyocr.Reader(['en'], gpu=True)

# Timer for idle screen taps
next_idle_tap_time = time.time() + random.randint(IDLE_TAP_MIN, IDLE_TAP_MAX)

# ========== FUNCTIONS ==========

def random_point_in_circle(center, radius):
    angle = random.uniform(0, 2 * math.pi)
    r = radius * math.sqrt(random.uniform(0, 1))
    x = int(center[0] + r * math.cos(angle))
    y = int(center[1] + r * math.sin(angle))
    return x, y

def random_point_in_rect(rect):
    x1, y1, x2, y2 = rect
    x = random.randint(min(x1, x2), max(x1, x2))
    y = random.randint(min(y1, y2), max(y1, y2))
    return x, y

def draw_donate_debug_overlay(image_path=SCREEN_PATH, output_path=DEBUG_OUTPUT):
    img = cv2.imread(image_path)
    if img is None:
        print("[-] Could not load screenshot for overlay.")
        return

    # Donate OCR box
    x1, y1, x2, y2 = DONATE_OCR_BOX
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.putText(img, "Donate Scan", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Standby (keep-awake) rectangle - make it more visible
    sx1, sy1, sx2, sy2 = STANDBY_RECT
    cv2.rectangle(img, (sx1, sy1), (sx2, sy2), (255, 0, 0), 3)
    # Add a semi-transparent overlay
    overlay = img.copy()
    cv2.rectangle(overlay, (sx1, sy1), (sx2, sy2), (255, 0, 0), -1)
    img = cv2.addWeighted(img, 0.9, overlay, 0.1, 0)
    cv2.putText(img, "IDLE TAP AREA", (sx1 + 10, sy1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    cv2.putText(img, f"({sx1},{sy1}) to ({sx2},{sy2})", (sx1 + 10, sy1 + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Troop centers
    for i, (x, y) in enumerate(TROOP_DONATE_CENTERS):
        cv2.circle(img, (x, y), TAP_RADIUS, (0, 255, 0), 2)
        cv2.putText(img, f"Troop{i+1}", (x - 30, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imwrite(output_path, img)
    print(f"[+] Debug overlay saved: {output_path}")

def scan_for_donate():
    img = cv2.imread(SCREEN_PATH)
    if img is None:
        print("[-] Could not load screenshot for OCR.")
        return False

    x1, y1, x2, y2 = DONATE_OCR_BOX
    crop = img[y1:y2, x1:x2]
    result = reader.readtext(crop, detail=0)

    print(f"[OCR] Detected texts: {result}")
    for text in result:
        lowered = text.lower()
        if any(keyword in lowered for keyword in ["pomate", "ponate", "dowate", "donate", "domate", "doqate"]):
            print(f"[+] 'Donate' text detected via OCR: '{text}'")
            return True
    return False

def perform_donation_taps():
    sequence = [1, 2, 3, 0]  # Troop 2 → 3 → 4 → 1 (Troop 1 last)
    tap_plan = {
        0: random.randint(8, 10),  # Troop 1
        1: random.randint(4, 5),   # Troop 2
        2: random.randint(3, 4),   # Troop 3
        3: random.randint(1, 2)    # Troop 4
    }

    for troop_index in sequence:
        center = TROOP_DONATE_CENTERS[troop_index]
        for _ in range(tap_plan[troop_index]):
            x, y = random_point_in_circle(center, TAP_RADIUS)
            tap(x, y)
            time.sleep(0.15)

def tap_donate_box():
    # Unchanged: used for *actual donation* taps after OCR detects the Donate button
    x, y = DONATE_BOX_CENTER
    print(f"[*] Tapping Donate box at ({x}, {y})")
    tap(x, y)

def tap_standby_area():
    # New: used for periodic keep-awake taps (random point within STANDBY_RECT)
    x, y = random_point_in_rect(STANDBY_RECT)
    print(f"[*] Standby tap at random point within {STANDBY_RECT}: ({x}, {y})")
    tap(x, y)

# ========== TAP DEBUG MENU ==========
def tap_debug_menu():
    while True:
        print("\n" + "=" * 50)
        print("TAP DEBUGGER - CoC Bot Tap Locations")
        print("=" * 50)
        print(f"Device: {get_selected_device()}")
        print(f"Total tap locations: {len(TAP_LOCATIONS)}")
        print()
        print("1. List all tap locations")
        print("2. Test single location")
        print("3. Test by category")
        print("4. Show coordinates only")
        print("5. Take screenshot")
        print("0. Back to main menu")
        print()
        
        try:
            choice = input("Enter your choice (0-5): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                list_all_tap_locations()
            elif choice == '2':
                list_all_tap_locations()
                try:
                    index = int(input(f"Enter location number (1-{len(TAP_LOCATIONS)}): "))
                    test_single_tap_location(index)
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '3':
                print("\nAvailable categories:")
                print("  • troops    - All troop selection icons")
                print("  • deploy    - Deployment locations on battlefield")
                print("  • spells    - Spell deployment locations")
                print("  • recovery  - Recovery and post-attack taps")
                print("  • navigation - Next button and return taps")
                category = input("Enter category name: ").strip().lower()
                test_tap_category(category)
            elif choice == '4':
                show_tap_coordinates_only()
            elif choice == '5':
                ensure_connection()
                print("Taking screenshot...")
                take_screenshot("debug_screenshot.png")
                print("Screenshot saved as: debug_screenshot.png")
            else:
                print("Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\nReturning to main menu...")
            break
        except Exception as e:
            print(f"Error: {e}")

def main_menu():
    while True:
        print("\n" + "=" * 50)
        print("CoC Bot - Donation & Debug Tool")
        print("=" * 50)
        print(f"Device: {ADB_SERIAL}")
        if RUN_TAG:
            print(f"Run Tag: {RUN_TAG}")
        print()
        print("1. Start donation watcher")
        print("2. Tap debugger (test main.py locations)")
        print("3. Test donation area taps")
        print("4. Generate debug overlay")
        print("0. Exit")
        print()
        
        try:
            choice = input("Enter your choice (0-4): ").strip()
            
            if choice == '0':
                print("Goodbye!")
                sys.exit(0)
            elif choice == '1':
                start_donation_watcher()
            elif choice == '2':
                tap_debug_menu()
            elif choice == '3':
                test_donation_taps_menu()
            elif choice == '4':
                ensure_connection()
                take_screenshot(SCREEN_PATH)
                draw_donate_debug_overlay()
                print(f"Debug overlay saved as: {DEBUG_OUTPUT}")
            else:
                print("Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")

def test_donation_taps_menu():
    print("\n" + "=" * 40)
    print("Donation Area Tap Testing")
    print("=" * 40)
    print("Donation coordinates:")
    for i, (x, y) in enumerate(TROOP_DONATE_CENTERS, 1):
        print(f"  Troop {i}: ({x}, {y})")
    print(f"Donate Box: {DONATE_BOX_CENTER}")
    print(f"Standby Area: {STANDBY_RECT}")
    print()
    
    choice = input("Test (d)onate box, (t)roop centers, (s)tandby area, or (a)ll? ").strip().lower()
    
    if choice in ['d', 'a']:
        print("Testing donate box...")
        tap_donate_box()
        time.sleep(1)
    
    if choice in ['t', 'a']:
        print("Testing troop donation centers...")
        perform_donation_taps()
    
    if choice in ['s', 'a']:
        print("Testing standby area...")
        tap_standby_area()

# ========== MAIN DONATION WATCHER ==========
def start_donation_watcher():
    global next_idle_tap_time
    print("[*] Starting donate watcher...")
    print("Press Ctrl+C to return to main menu")
    
    try:
        while True:
            # Check 90-minute timeout
            if time.time() - START_TIME > TIMEOUT_DURATION:
                print("[!] 90-minute timeout reached. Returning to menu.")
                break

            ensure_connection()  # adb_helper should respect ANDROID_SERIAL env
            take_screenshot(SCREEN_PATH)
            draw_donate_debug_overlay()

            current_time = time.time()

            # Periodic idle tap to prevent screen timeout
            if current_time >= next_idle_tap_time:
                print("[~] Performing periodic tap in standby area to prevent sleep.")
                tap_standby_area()
                next_idle_tap_time = current_time + random.randint(IDLE_TAP_MIN, IDLE_TAP_MAX)

            if scan_for_donate():
                print("[+] 'Donate' detected! Tapping donate box...")
                tap_donate_box()
                time.sleep(2)

                print("[*] Performing troop donation taps...")
                perform_donation_taps()

                print("[*] Done. Sleeping 10s before next scan.")
                time.sleep(10)
            else:
                print("[-] 'Donate' not found. Retrying in 3s...")
                time.sleep(3)
                
    except KeyboardInterrupt:
        print("\n[*] Donation watcher stopped by user.")

# ========== ENTRY POINT ==========
if __name__ == "__main__":
    try:
        # Check for --debug or --tap-debug argument to go straight to tap debugging
        if len(sys.argv) > 1 and sys.argv[1] in ['--debug', '--tap-debug']:
            tap_debug_menu()
        else:
            main_menu()
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
