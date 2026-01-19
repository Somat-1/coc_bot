# main.py
from utils.adb_helper import (
    take_screenshot, tap, tap_and_hold, ensure_connection, get_selected_device
)
from time import sleep
from pathlib import Path
from datetime import datetime
import cv2
import easyocr
import re
import random
import math
import time
import os

# ========= PER-INSTANCE NAMESPACING (CRITICAL) =========
RUN_TAG = os.getenv("RUN_TAG") or get_selected_device().replace(":", "_")
SCREEN_PATH        = f"screen_{RUN_TAG}.png"
DATASET_DIR        = f"loot_dataset/{RUN_TAG}"
DEBUG_OVERLAY_PATH = f"debug_full_overlay_{RUN_TAG}.png"

print(f"[BOOT] RUN_TAG={RUN_TAG} | SCREEN_PATH={SCREEN_PATH} | DATASET_DIR={DATASET_DIR}")

# ========= HELPERS =========
def random_point(center, radius):
    θ = random.random() * 2 * math.pi
    r = radius * math.sqrt(random.random())
    x = int(center[0] + r * math.cos(θ))
    y = int(center[1] + r * math.sin(θ))
    return x, y

def human_delay(min_s=0.15, max_s=0.4):
    sleep(random.uniform(min_s, max_s))

# ========= CONFIG =========
POST_ATTACK_WAIT = 60
POST_ATTACK_TAPS = [(800, 850), (97, 900), (250, 700), (1363, 821)]

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

# ========= DEBUG OVERLAY =========
def draw_full_debug_overlay(image_path=SCREEN_PATH, output_path=DEBUG_OVERLAY_PATH):
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
        cv2.putText(img, label, (x1, y1 - 5),                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Updated troop coordinates - 8 troops after removing event troops
    troop_coords = [(220 + i * 118, 910) for i in range(8)]
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

    return_taps = [(800, 850), (110, 915), (1234, 636)]
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

# ========= LOOT IMAGE SAVE =========
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

# ========= OCR LOOT =========
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
    print(f"[OCR-{RUN_TAG}] Gold={loot['gold']} Elixir={loot['elixir']} Dark={loot['dark']}")
    return loot['gold'], loot['elixir'], loot['dark']

# ========= TROOP DEPLOYMENT =========
def deploy_troops():
    print(f"[*-{RUN_TAG}] Deploying troops...")
    # Troop positions after removing event troops (Troops 3 & 4)
    # Now only 8 troops: Balloon, Dragons, Siege, 4 Heroes, Spells
    # Using 118px spacing and y=910
    troop_icons = [(220 + i * 118, 910) for i in range(8)]
    deploy_1 = (1526, 450)  # Dragon/primary deployment location
    deploy_2 = (180, 480)   # Secondary deployment location
    
    # DEBUG: Show all troop icon positions
    print(f"[DEBUG-{RUN_TAG}] === TROOP ICON POSITIONS ===")
    for i, coords in enumerate(troop_icons):
        troop_type = "REGULAR"
        if i == 2:
            troop_type = "SIEGE"
        elif i >= 3 and i <= 6:
            troop_type = f"HERO {i-2}"
        elif i == 7:
            troop_type = "SPELLS"
        print(f"[DEBUG-{RUN_TAG}] Troop {i+1} (index {i}): {coords} - {troop_type}")
    print(f"[DEBUG-{RUN_TAG}] Deploy point 1 (dragon): {deploy_1}")
    print(f"[DEBUG-{RUN_TAG}] Deploy point 2 (secondary): {deploy_2}")
    print(f"[DEBUG-{RUN_TAG}] ===========================")
    
    # STEP 1: Deploy Troop 1 - Balloon (1 time at dragon location)
    print(f"[*-{RUN_TAG}] Step 1: Deploying Troop 1 (Balloon) once...")
    tap(*troop_icons[0]); human_delay()  # Select Troop 1 (index 0)
    tap(*random_point(deploy_1, 5)); human_delay(0.3, 0.6)
    
    # STEP 2: Deploy Troop 2 - Dragons (with hold at dragon location)
    print(f"[*-{RUN_TAG}] Step 2: Deploying Troop 2 (Dragons with hold)...")
    tap(*troop_icons[1]); human_delay()  # Select Troop 2 (index 1)
    tap_and_hold(*random_point(deploy_1, 5), duration_ms=2500); human_delay(0.5, 1)
    
    # STEP 3: Deploy Siege Machine (Troop 3) - ONCE at dragon location (NOT a hero)
    print(f"[*-{RUN_TAG}] Step 3: Deploying Siege Machine (Troop 3) once...")
    siege_coords = troop_icons[2]
    print(f"[DEBUG-{RUN_TAG}] Tapping Siege Machine icon at {siege_coords}")
    tap(*siege_coords); human_delay()  # Select Troop 3 - Siege Machine (index 2)
    deploy_point = random_point(deploy_1, 5)
    print(f"[DEBUG-{RUN_TAG}] Deploying Siege Machine at {deploy_point}")
    tap(*deploy_point)  # Deploy once
    print(f"[DEBUG-{RUN_TAG}] Siege Machine deployed. Waiting brief delay...")
    human_delay(0.5, 0.8)  # Brief delay after siege
    print(f"[DEBUG-{RUN_TAG}] Siege Machine step complete. Moving to heroes...")
    
    # STEP 4: Deploy ALL 4 HEROES (Troops 4-7, indices 3-6)
    # Hero 1 (index 3): Deploy at dragon location (deploy_1), wait 4s, activate ability
    print(f"[*-{RUN_TAG}] Step 4: Deploying Hero 1 (Troop 4 at index 3) at dragon location...")
    hero1_coords = troop_icons[3]
    print(f"[DEBUG-{RUN_TAG}] Hero 1 icon position: {hero1_coords}")
    tap(*hero1_coords); human_delay()  # Select Hero 1 (index 3)
    deploy_point = random_point(deploy_1, 5)
    print(f"[DEBUG-{RUN_TAG}] Deploying Hero 1 at {deploy_point}")
    tap(*deploy_point)  # Deploy at dragon location
    print(f"[*-{RUN_TAG}] Waiting 4s before activating Hero 1 ability...")
    sleep(4)  # Wait 4 seconds
    print(f"[DEBUG-{RUN_TAG}] Tapping Hero 1 icon again at {hero1_coords} to activate ability...")
    tap(*hero1_coords); human_delay(0.9, 1.4)  # Activate ability
    print(f"[*-{RUN_TAG}] Hero 1 deployed and ability activated!")
    
    # STEP 5: Deploy Heroes 2-4 (Troops 5-7, indices 4-6) at secondary location
    # Each hero: deploy at deploy_2, wait 1s, activate ability
    print(f"[*-{RUN_TAG}] Step 5: Deploying Heroes 2-4 at secondary location...")
    for hero_offset in range(3):  # Loop 3 times for Heroes 2, 3, 4
        hero_index = 4 + hero_offset  # indices: 4, 5, 6
        hero_num = hero_offset + 2  # Hero numbers: 2, 3, 4
        hero_coords = troop_icons[hero_index]
        expected_x = 220 + hero_index * 118
        print(f"[*-{RUN_TAG}] Deploying Hero {hero_num} (Troop {hero_index + 1} at index {hero_index})...")
        print(f"[DEBUG-{RUN_TAG}] Hero {hero_num} icon at {hero_coords} (expected x={expected_x})")
        
        tap(*hero_coords); human_delay()  # Select hero
        deploy_point = random_point(deploy_2, 5)
        print(f"[DEBUG-{RUN_TAG}] Deploying Hero {hero_num} at {deploy_point}")
        tap(*deploy_point)  # Deploy at secondary location
        print(f"[*-{RUN_TAG}] Waiting 1s before activating Hero {hero_num} ability...")
        sleep(1)  # Wait 1 second
        print(f"[DEBUG-{RUN_TAG}] Tapping Hero {hero_num} icon at {hero_coords} to activate ability...")
        tap(*hero_coords); human_delay(0.3, 0.5)  # Activate ability
        print(f"[*-{RUN_TAG}] Hero {hero_num} deployed and ability activated!")
    
    # STEP 6: Deploy Spells (Troop 8)
    print(f"[*-{RUN_TAG}] Step 6: Deploying Spells (Troop 8)...")
    tap(*troop_icons[7]); human_delay()  # Select Troop 8 (index 7)
    spell_locations = [(900, 350), (700, 480), (900, 600), (830, 480), (900, 480)]
    for i, loc in enumerate(spell_locations, 1):
        print(f"[*-{RUN_TAG}] Deploying spell {i}/5 at {loc}...")
        tap(*random_point(loc, 15))
        human_delay(0.2, 0.4)
    print(f"[*-{RUN_TAG}] All spells deployed!")

    print(f"[+{RUN_TAG}] All troops deployed successfully!")

# ========= MAIN LOOP =========
start_time = time.time()
TIMEOUT_SECONDS = 35 * 60
zero_loot_count = 0

while True:
    if time.time() - start_time > TIMEOUT_SECONDS:
        print(f"[!{RUN_TAG}] Timeout reached. Exiting script.")
        break

    ensure_connection()

    print(f"[*{RUN_TAG}] =========================================================")
    print(f"[*{RUN_TAG}] Taking screenshot...")
    take_screenshot(SCREEN_PATH)
    draw_full_debug_overlay()  # uses per-instance default path

    sleep(1.5)
    save_loot_crop()

    loot = extract_loot_values(SCREEN_PATH)

    if loot == (0, 0, 0):
        for attempt in range(2):
            print(f"[!{RUN_TAG}] Loot 0,0,0 detected. Retrying OCR attempt {attempt+1}...")
            sleep(2)
            take_screenshot(SCREEN_PATH)
            draw_full_debug_overlay()
            sleep(1.5)
            save_loot_crop()
            loot = extract_loot_values(SCREEN_PATH)
            if loot != (0, 0, 0):
                break

    if loot == (0, 0, 0):
        zero_loot_count += 1
        print(f"[!{RUN_TAG}] Consecutive zero loot count: {zero_loot_count}")
    else:
        zero_loot_count = 0

    if zero_loot_count >= 7:
        print(f"[!{RUN_TAG}] 15 consecutive zero loot results. Performing recovery taps...")
        for coords in [(800, 850), (97, 900), (250, 700), (1363, 821)]:
            tap(*coords); sleep(2)
        continue

    if loot:
        gold, elixir, dark = loot
        print(f"[+{RUN_TAG}] Loot parsed: Gold={gold}, Elixir={elixir}, Dark={dark}")
        if ((gold >= GOLD_THRESHOLD and elixir >= ELIXIR_THRESHOLD and dark >= DARK_THRESHOLD)
            or gold >= 1_200_000 or elixir >= 1_200_000):
            print(f"[+{RUN_TAG}] Loot is sufficient. Attacking base...")
            deploy_troops()

            print(f"[*{RUN_TAG}] Waiting {POST_ATTACK_WAIT} seconds...")
            sleep(POST_ATTACK_WAIT)

            EXTRA_ATTACK_TAPS = [(110, 790), (960, 623)]
            print(f"[*{RUN_TAG}] Performing extra post-attack taps...")
            for coords in EXTRA_ATTACK_TAPS:
                tap(*coords); sleep(2)

            print(f"[*{RUN_TAG}] Returning to base...")
            for coords in POST_ATTACK_TAPS:
                tap(*coords); sleep(2)
            continue
        else:
            print(f"[-{RUN_TAG}] Loot too low. Skipping base.")
    else:
        print(f"[-{RUN_TAG}] Loot parsing failed.")

    print(f"[*{RUN_TAG}] Tapping 'Next'...")
    tap(1470, 760)
    sleep(5)
