import os
import argparse
from utils.adb_helper import take_screenshot, tap, ensure_connection
import easyocr
import cv2
import random
import time
import math

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
DEBUG_OUTPUT = "debug_donate_overlay.png"

# OCR search box for "Donate" button
DONATE_OCR_BOX = (374, 817, 511, 865)
DONATE_BOX_CENTER = ((374 + 511) // 2, (817 + 865) // 2)

# Standby (keep-awake) tap rectangle (x1, y1, x2, y2)
STANDBY_RECT = (700, 300, 1400, 750)

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

    # Standby (keep-awake) rectangle
    sx1, sy1, sx2, sy2 = STANDBY_RECT
    cv2.rectangle(img, (sx1, sy1), (sx2, sy2), (255, 0, 0), 2)
    cv2.putText(img, "Standby Area", (sx1, sy1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

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

# ========== MAIN LOOP ==========
print("[*] Starting donate watcher...")
while True:
    # Check 90-minute timeout
    if time.time() - START_TIME > TIMEOUT_DURATION:
        print("[!] 90-minute timeout reached. Exiting script.")
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
