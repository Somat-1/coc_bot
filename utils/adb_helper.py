# utils/adb_helper.py
import os
import re
import time
import cv2
import subprocess
import shutil
import sys

ADB_PATH = shutil.which("adb") or "adb"
ENV_SERIAL = os.getenv("ANDROID_SERIAL") or os.getenv("ADB_SERIAL")
ADB_DEVICE = None  # set in _select_device()

def _run(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)

def _list_devices():
    out = _run([ADB_PATH, "devices"]).stdout.splitlines()[1:]  # skip header
    return [l.split()[0] for l in out if "\tdevice" in l]

def _is_hostport(s):
    return bool(s and re.match(r"^\d{1,3}(?:\.\d{1,3}){3}:\d{2,5}$", s))

def _select_device():
    global ADB_DEVICE
    sel = ENV_SERIAL
    if sel and _is_hostport(sel):
        # ensure host:port is connected
        if f"{sel}\tdevice" not in _run([ADB_PATH, "devices"]).stdout:
            try:
                _run([ADB_PATH, "connect", sel])
            except subprocess.CalledProcessError as e:
                print(f"[-] adb connect {sel} failed:\n{e.stderr}", file=sys.stderr)
                sys.exit(1)

    devices = _list_devices()
    if sel:
        if sel not in devices:
            print(f"[-] Selected device {sel} not found in adb devices.", file=sys.stderr)
            if not _is_hostport(sel):
                print("    Tip: is the emulator/instance running? Correct serial?", file=sys.stderr)
            sys.exit(1)
        ADB_DEVICE = sel
    else:
        if not devices:
            print("[-] No ADB device found. Connect one or set ANDROID_SERIAL/ADB_SERIAL.", file=sys.stderr)
            sys.exit(1)
        ADB_DEVICE = devices[0]
    print(f"[+] Using ADB device: {ADB_DEVICE}")

def ensure_connection():
    # Re-validate the chosen device is still present
    global ADB_DEVICE
    if ADB_DEVICE is None:
        _select_device()
        return
    if ADB_DEVICE not in _list_devices():
        # Try to reconnect host:port, otherwise reselect
        if _is_hostport(ADB_DEVICE):
            try:
                _run([ADB_PATH, "connect", ADB_DEVICE])
            except subprocess.CalledProcessError:
                pass
        if ADB_DEVICE not in _list_devices():
            _select_device()

# Select device immediately on import so main.py prints it once
_select_device()

def _adb(*args):
    """Always call adb with -s <ADB_DEVICE>."""
    if ADB_DEVICE is None:
        _select_device()
    return subprocess.run([ADB_PATH, "-s", ADB_DEVICE, *map(str, args)],
                          check=True, text=True, capture_output=True)

def take_screenshot(output_path="screen.png", retries=3, delay=0.4):
    """Grab a PNG via exec-out; validate it isn't blank."""
    for attempt in range(retries):
        ensure_connection()
        with open(output_path, "wb") as f:
            p = subprocess.Popen([ADB_PATH, "-s", ADB_DEVICE, "exec-out", "screencap", "-p"],
                                 stdout=f, stderr=subprocess.PIPE)
            _, err = p.communicate()
            if p.returncode != 0:
                msg = err.decode(errors="ignore")
                print(f"[-] screencap failed (try {attempt+1}): {msg.strip()}")
        time.sleep(delay)
        img = cv2.imread(output_path)
        if img is not None and img.size and img.mean() not in (0, 255):
            return
        print(f"[-] Screenshot retry {attempt+1}/{retries} (blank or unreadable)")
        time.sleep(0.2)
    print("[-] Final screenshot attempt failed or was blank.")

def tap(x, y):
    ensure_connection()
    _adb("shell", "input", "tap", int(x), int(y))

def tap_and_hold(x, y, duration_ms=2500):
    ensure_connection()
    _adb("shell", "input", "swipe", int(x), int(y), int(x), int(y), int(duration_ms))

# ---- helpers exposed to main.py ----
def get_selected_device():
    """Return the serial of the currently selected device."""
    return ADB_DEVICE

def set_device(serial):
    """Optional: switch device programmatically before first use."""
    global ADB_DEVICE, ENV_SERIAL
    ENV_SERIAL = serial
    ADB_DEVICE = None
    _select_device()
