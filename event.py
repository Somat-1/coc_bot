import os
import time
import random

# Verified ADB screen coordinates with names
click_sequence = [
    {'name': 'roulette', 'x': 700, 'y': 1126},
    {'name': 'duel_button', 'x': 700, 'y': 1126},
    {'name': 'dialogue', 'x': 700, 'y': 1126},
    {'name': 'mode_selection', 'x': 700, 'y': 900},
    {'name': 'auto_duel', 'x': 750, 'y': 1400},
    {'name': 'post_battle_ok', 'x': 500, 'y': 1520},
    {'name': 'level_up_screen', 'x': 233, 'y': 1000},
    {'name': 'level_up_screen_next', 'x': 500, 'y': 1520},

    {'name': 'event2_log3', 'x': 500, 'y': 1389},
    {'name': 'event2_log2', 'x': 467, 'y': 1380},
    {'name': 'event2_log3', 'x': 500, 'y': 1300},


    
    {'name': 'dialogue1', 'x': 720, 'y': 1126},
    {'name': 'dialogue2', 'x': 720, 'y': 1126},
    {'name': 'progression', 'x': 500, 'y': 1162},
    {'name': 'zone_completion', 'x': 456, 'y': 1244}
]

def adb_click(x, y):
    os.system(f'adb shell input tap {int(x)} {int(y)}')

def main():
    try:
        loops = int(input("Enter number of times to repeat the sequence: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    print(f"\nStarting automation for {loops} loop(s)...\n")

    for loop in range(loops):
        print(f"--- Loop {loop + 1} ---")
        for click in click_sequence:
            rand_x = click['x'] + random.uniform(-15, 15)
            rand_y = click['y'] + random.uniform(-15, 15)
            print(f"Clicking '{click['name']}' at approx ({int(rand_x)}, {int(rand_y)})")
            adb_click(rand_x, rand_y)

            # Add custom wait for auto_duel
            if click['name'] == 'auto_duel':
                base_delay = 50
            else:
                base_delay = 0

            delay = base_delay + random.uniform(10, 12)
            print(f"Waiting {delay:.2f} seconds...\n")
            time.sleep(delay)

    print("\nDone.")

if __name__ == "__main__":
    main()
