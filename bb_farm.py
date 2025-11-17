import random
import time
from utils.adb_helper import tap

# === CONFIG ===
ATTACK_BUTTON = (100, 900)
ATTACK_BUTTON2 = (1200, 655)
TROOP_1_ICON = (200, 920)
TROOP_2_ICON = (340, 920)
DEPLOY_BOX_TOP_LEFT = (122, 150)
DEPLOY_BOX_BOTTOM_RIGHT = (1350, 660)
POST_ATTACK_CLICKS = [(100, 750), (950, 600), (800,850)]
EMPTY_LOOK_CLICKS = [(1117, 72), (1213, 844), (1397, 104)]  # coords to “empty the look”

EXCLUDE_LEFT = 650
EXCLUDE_RIGHT = 820
EXCLUDE_TOP = 360
EXCLUDE_BOTTOM = 460

def generate_deploy_points(count=100):
    points = []
    while len(points) < count:
        x = random.randint(DEPLOY_BOX_TOP_LEFT[0], DEPLOY_BOX_BOTTOM_RIGHT[0])
        y = random.randint(DEPLOY_BOX_TOP_LEFT[1], DEPLOY_BOX_BOTTOM_RIGHT[1])
        if not (EXCLUDE_LEFT <= x <= EXCLUDE_RIGHT and EXCLUDE_TOP <= y <= EXCLUDE_BOTTOM):
            points.append((x, y))
    return points

def deploy_troop1(points):
    tap(*TROOP_1_ICON); time.sleep(0.2)
    for _ in range(3):
        tap(*random.choice(points)); time.sleep(0.1)

def deploy_troop2(points):
    tap(*TROOP_2_ICON); time.sleep(0.2)
    end = time.time() + 4
    while time.time() < end:
        tap(*random.choice(points)); time.sleep(0.05)

def bb_farm_loop():
    deploy_points = generate_deploy_points()
    cycle_count = 0
    thresholds = [5, 6]
    th_idx = 0

    while True:
        cycle_count += 1

        # 1) start attack
        tap(*ATTACK_BUTTON); time.sleep(2)
        tap(*ATTACK_BUTTON2); time.sleep(10)

        # 2) deploy troops
        deploy_troop1(deploy_points)
        deploy_troop2(deploy_points)

        # 3) wait for result
        time.sleep(90)

        # 4) post‐attack taps
        for x, y in POST_ATTACK_CLICKS:
            tap(x, y); time.sleep(3)

        # 5) empty look every 5 then 6 cycles
        if cycle_count >= thresholds[th_idx]:
            for x, y in EMPTY_LOOK_CLICKS:
                tap(x, y); time.sleep(2)
            cycle_count = 0
            th_idx = 1 - th_idx  # flip between 0 and 1

if __name__ == "__main__":
    bb_farm_loop()
