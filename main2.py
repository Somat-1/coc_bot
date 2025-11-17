from utils.adb_helper import take_screenshot, tap, tap_and_hold, ensure_connection
from time import sleep
from pathlib import Path
from datetime import datetime
import cv2
import easyocr
import re
import random
import math
import time

def random_point(center, radius):
    θ = random.random() * 2 * math.pi
    r = radius * math.sqrt(random.random())
    x = int(center[0] + r * math.cos(θ))
    y = int(center[1] + r * math.sin(θ))
    return x, y

def human_delay(min_s=0.15, max_s=0.4):
    """Small random delay to mimic human actions."""
    sleep(random.uniform(min_s, max_s))

# ========== CONFIG ==========
SCREEN_PATH = "screen.png"
DATASET_DIR = "loot_dataset"
POST_ATTACK_WAIT = 60
# Updated return-to-base tap sequence
POST_ATTACK_TAPS = [
    (800, 850),
    (60, 777),
    (1300, 750),
    (975, 655),
    (1350, 820),
    (1200, 625),
]

GOLD_THRESHOLD = 800000
ELIXIR_THRESHOLD = 800000
DARK_THRESHOLD = 0

reader = easyocr.Reader(['en'], gpu=False)

# Prompt hero count once at the start
try:
    HERO_COUNT = int(input("Enter number of heroes available (0-5): ").strip())
    if HERO_COUNT < 0 or HERO_COUNT > 5:
        HERO_COUNT = 0
except ValueError:
    HERO_COUNT = 0

# ========== DEBUG OVERLAY ==========
def draw_full_debug_overlay(image_path="screen.png", output_path="debug_full_overlay.png"):
    img = cv2.imread(image_path)
    if img is None:
        print("[-] Failed to load screenshot for overlay.")
        return

    boxes = {
        "Gold":   (65, 113, 205, 142),
        "Elixir": (65, 158, 205, 185),
        "Dark":   (65, 198, 180, 228)
    }
    for label, (x1, y1, x2, y2) in boxes.items():
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    troop_coords = [(220 + i * 100, 930) for i in range(10)]
    for i, (x, y) in enumerate(troop_coords):
        cv2.circle(img, (x, y), 12, (255, 0, 0), 2)
        cv2.putText(img, f"T{i+1}", (x - 20, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    deploy_1 = (1526, 450)
    deploy_2 = (180, 480)
    cv2.circle(img, deploy_1, 12, (0, 255, 255), 2)
    cv2.putText(img, "D1", (deploy_1[0] - 20, deploy_1[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    cv2.circle(img, deploy_2, 12, (0, 255, 255), 2)
    cv2.putText(img, "D2", (deploy_2[0] - 20, deploy_2[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Overlay markers to match return-to-base taps
    return_taps = [
        (800, 850),
        (60, 777),
        (1300, 750),
        (975, 655),
        (1350, 820),
        (1200, 625),
    ]
    for i, (x, y) in enumerate(return_taps):
        cv2.circle(img, (x, y), 10, (0, 0, 255), 2)
        cv2.putText(img, f"R{i+1}", (x - 20, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    next_btn = (1470, 760)
    cv2.circle(img, next_btn, 12, (128, 0, 255), 2)
    cv2.putText(img, "Next", (next_btn[0] - 30, next_btn[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 0, 255), 1)

    cv2.imwrite(output_path, img)
    print(f"[+] Debug overlay saved: {output_path}")

# ========== LOOT IMAGE SAVE ==========
def save_loot_crop():
    Path(DATASET_DIR).mkdir(parents=True, exist_ok=True)
    img = cv2.imread(SCREEN_PATH)
    if img is None or img.shape[0] == 0:
        print("[-] Screenshot invalid.")
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"{DATASET_DIR}/loot_{timestamp}.png"
    cv2.imwrite(out_path, img)
    print(f"[+] Saved loot panel to: {out_path}")

# ========== OCR LOOT ==========
def extract_loot_values(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("[-] Could not load screenshot.")
        return None
    crops = {
        "gold": image[113:142, 65:205],
        "elixir": image[158:185, 65:205],
        "dark": image[198:228, 65:180],
    }
    loot = {}
    for key, crop in crops.items():
        result = reader.readtext(crop, detail=0)
        text = ''.join(result)
        digits = re.sub(r'[^\d]', '', text)
        loot[key] = int(digits) if digits.isdigit() else 0
    print(f"[OCR] Parsed Loot: Gold={loot['gold']}, Elixir={loot['elixir']}, Dark={loot['dark']}")
    return loot['gold'], loot['elixir'], loot['dark']

# ========== TROOP DEPLOYMENT ==========
def deploy_troops():
    print("[*] Deploying troops...")
    troop_icons = [(220 + i * 100, 930) for i in range(10)]
    deploy_1 = (1526, 450)
    deploy_2 = (180, 480)
    # NEW: siege machine drop target
    siege_drop = (455, 900)

    # Troop 1: Event troop
    tap(*troop_icons[0])
    human_delay()
    tap(*random_point(random.choice([deploy_1, deploy_2]), 5))
    human_delay(0.3, 0.6)

    # Troop 2: Dragons
    tap(*troop_icons[1])
    human_delay()
    tap_and_hold(*random_point(deploy_1, 5), duration_ms=2500)
    human_delay(0.5, 1)

    # Troop 3: Siege machine  (updated drop location)
    tap(*troop_icons[2])           # select siege machine
    human_delay()
    tap(*random_point(siege_drop, 5))  # deploy near (455, 900)
    human_delay(0.5, 1)

    # Heroes
    if HERO_COUNT > 0:
        first_hero_index = 3
        # First hero at deploy_1
        tap(*troop_icons[first_hero_index])
        human_delay()
        tap(*random_point(deploy_1, 5))
        sleep(4)
        tap(*troop_icons[first_hero_index])  # Activate ability
        human_delay(0.5, 0.8)

        # Remaining heroes at deploy_2
        for i in range(1, HERO_COUNT):
            hero_index = first_hero_index + i
            if hero_index < len(troop_icons):
                tap(*troop_icons[hero_index])
                human_delay()
                tap(*random_point(deploy_2, 5))
                human_delay()
                tap(*random_point(deploy_2, 5))
                human_delay(0.3, 0.5)

    # Spells — always after last hero
    print("[*] Deploying spells...")
    first_hero_index = 3
    last_hero_index = first_hero_index + HERO_COUNT - 1
    spell_start_index = last_hero_index + 1

    if spell_start_index < len(troop_icons):
        tap(*troop_icons[spell_start_index])
        human_delay()
        spell_drops = [
            (900, 350), (700, 480),
            (900, 600), (830, 480),
            (900, 480)
        ]
        for loc in spell_drops:
            tap(*random_point(loc, 15))
            human_delay(0.2, 0.4)

    print("[+] Troops deployed.")

# ========== MAIN LOOP ==========
start_time = time.time()
TIMEOUT_SECONDS = 35 * 60
zero_loot_count = 0

while True:
    if time.time() - start_time > TIMEOUT_SECONDS:
        print("[!] Timeout reached. Exiting script.")
        break

    ensure_connection()

    print("[*] =========================================================")
    print("[*] Taking screenshot...")
    take_screenshot(SCREEN_PATH)
    draw_full_debug_overlay(SCREEN_PATH)

    sleep(1.5)
    save_loot_crop()

    loot = extract_loot_values(SCREEN_PATH)

    if loot == (0, 0, 0):
        for attempt in range(2):
            print(f"[!] Loot 0,0,0 detected. Retrying OCR attempt {attempt+1}...")
            sleep(2)
            take_screenshot(SCREEN_PATH)
            draw_full_debug_overlay(SCREEN_PATH)
            sleep(1.5)
            save_loot_crop()
            loot = extract_loot_values(SCREEN_PATH)
            if loot != (0, 0, 0):
                break

    if loot == (0, 0, 0):
        zero_loot_count += 1
        print(f"[!] Consecutive zero loot count: {zero_loot_count}")
    else:
        zero_loot_count = 0

    if zero_loot_count >= 7:
        print("[!] 15 consecutive zero loot results. Performing recovery taps...")
        for coords in [(800, 850), (97, 900), (1200, 625)]:
            tap(*coords)
            sleep(2)
        continue

    if loot:
        gold, elixir, dark = loot
        print(f"[+] Loot parsed: Gold={gold}, Elixir={elixir}, Dark={dark}")
        if (
            (gold >= GOLD_THRESHOLD and elixir >= ELIXIR_THRESHOLD and dark >= DARK_THRESHOLD)
            or gold >= 1_200_000
            or elixir >= 1_200_000
        ):
            print("[+] Loot is sufficient. Attacking base...")
            deploy_troops()

            print(f"[*] Waiting {POST_ATTACK_WAIT} seconds...")
            sleep(POST_ATTACK_WAIT)

            EXTRA_ATTACK_TAPS = [(110, 790), (960, 623)]
            print("[*] Performing extra post-attack taps...")
            for coords in EXTRA_ATTACK_TAPS:
                tap(*coords)
                sleep(2)

            print("[*] Returning to base...")
            for coords in POST_ATTACK_TAPS:
                tap(*coords)
                sleep(2)

            continue
        else:
            print("[-] Loot too low. Skipping base.")
    else:
        print("[-] Loot parsing failed.")

    print("[*] Tapping 'Next'...")
    tap(1470, 760)
    sleep(5)
