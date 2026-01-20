# 🚀 War Tracker - Unified Script

**ONE script to rule them all!** All war tracking functionality in a single menu-driven interface.

## ⚡ Quick Start

### Super Simple - Just Run:

```bash
cd war_tracking
./run.sh
```

Or:

```bash
cd war_tracking
source ../env/bin/activate
python war_tracker.py
```

## 🎯 What It Does

The unified `war_tracker.py` script provides an interactive menu with ALL functionality:

```
🏰 CLASH OF CLANS WAR TRACKER
================================================================================
Clan: #2P0GPYYJY
Date: 2026-01-19 13:45:00
================================================================================

📋 MAIN MENU
--------------------------------------------------------------------------------
1️⃣  Track Current War (Full Analysis)
2️⃣  View War History
3️⃣  Generate All CSV Tables
4️⃣  Generate War Summary Table Only
5️⃣  Generate Per-War Member Table Only
6️⃣  Generate Overall Member Table Only
7️⃣  View Table Files Location
8️⃣  Open CSV Files in Finder
9️⃣  Show Table Preview
🔟  View Statistics
0️⃣  Exit
--------------------------------------------------------------------------------
```

## 📋 Features

### 1️⃣ Track Current War
- Fetches live war data from CoC API
- Shows who attacked and who didn't
- **Displays copy-paste messages** with @mentions
- Auto-saves war data to JSON
- Option to generate CSV tables immediately

**When to use:** During active wars to track member participation

### 2️⃣ View War History
- Shows past wars from API
- Customizable number of wars to display
- Win/loss/tie results with scores

**When to use:** Review recent war performance

### 3️⃣ Generate All CSV Tables
- Creates all 3 CSV files at once:
  - `war_summary.csv`
  - `per_war_member_performance.csv`
  - `overall_member_performance.csv`

**When to use:** After tracking multiple wars, to analyze data

### 4️⃣-6️⃣ Generate Individual Tables
- Create just one specific table
- Faster if you only need one report

**When to use:** Quick specific analysis

### 7️⃣ View Table Files Location
- Shows where all files are saved
- Lists CSV files and their sizes
- Shows tracked wars in `war_data/`

**When to use:** Find where your data is stored

### 8️⃣ Open CSV Files in Finder
- Opens the directory in macOS Finder
- Quick access to CSV files for Excel/Numbers

**When to use:** Ready to analyze in spreadsheet software

### 9️⃣ Show Table Preview
- Displays what columns each table contains
- Helps understand data structure

**When to use:** Learn what data is available

### 🔟 View Statistics
- Shows how many wars tracked
- Lists CSV files created
- Shows storage info

**When to use:** Quick status check

## 🎬 Complete Workflow Example

### Scenario: Track a War and Get Reports

1. **Run the unified script:**
   ```bash
   ./run.sh
   ```

2. **Select Option 1** (Track Current War)
   - Script fetches war data
   - Shows participation summary
   - **Displays copy-paste messages** ← Copy these to Clash/Discord!
   - Saves war data automatically
   - Asks if you want to generate tables

3. **Press 'y'** to generate tables
   - All 3 CSV files created instantly

4. **Select Option 8** (Open in Finder)
   - Finder opens with CSV files
   - Double-click any CSV to open in Excel/Numbers

5. **Select Option 0** to exit

**Total time: < 30 seconds!**

## 📊 Where to Find Everything

### Copy-Paste Messages

**Location:** In the terminal after selecting Option 1

Look for this section:
```
================================================================================
📋 COPY-PASTE MESSAGES FOR DISCORD/CLASH
================================================================================

Message 1 (65 chars):
❌ NO ATTACKS: @PlayerOne, @PlayerTwo
```

**How to use:**
1. Select the message text (not the "Message 1" line)
2. Cmd+C to copy
3. Paste directly in Clash of Clans chat or Discord

### CSV Tables

**Location:** Same directory as the script

After generating tables (Option 3-6):
```
war_tracking/
├── war_summary.csv                    ← HERE
├── per_war_member_performance.csv     ← HERE
├── overall_member_performance.csv     ← HERE
```

**How to open:**
- **Option 8** in menu → Opens Finder automatically
- Or double-click CSV file
- Or drag to Excel/Google Sheets

### War Data (JSON)

**Location:** `war_data/` subdirectory

```
war_tracking/
└── war_data/
    ├── war_2P0GPYYJY_20260119_154611.json
    ├── war_2P0GPYYJY_20260120_103045.json
    └── ...
```

## 🎨 Visualizing Tables

### In Excel (Easiest)

1. **From the menu:** Select Option 8 (Open in Finder)
2. **Double-click** any CSV file
3. Excel/Numbers opens automatically
4. Sort, filter, create charts!

### In Google Sheets

1. Go to [sheets.google.com](https://sheets.google.com)
2. File → Import → Upload
3. Select the CSV file
4. Click Import

### Quick Terminal View

```bash
# View first 10 lines
head war_summary.csv

# View with formatting
column -s, -t < war_summary.csv | less
```

## 💡 Pro Tips

### Daily War Tracking Routine

**Morning (War Day Start):**
```bash
./run.sh
# Select 1 → Track war
# Copy messages, paste in clan chat
```

**Evening (Before War Ends):**
```bash
./run.sh
# Select 1 → Track war again (updates data)
# See who still hasn't attacked
```

**After War:**
```bash
./run.sh
# Select 3 → Generate all tables
# Select 8 → Open in Finder
# Analyze in Excel
```

### Finding Problem Members

Use **Option 3** to generate tables, then in Excel:

1. Open `overall_member_performance.csv`
2. Sort by "Wars Missed (No Attacks)" (descending)
3. Top rows = frequent offenders

### Tracking Best Performers

1. Open `overall_member_performance.csv`
2. Sort by "Avg Stars per Attack" (descending)
3. Top rows = best attackers

### Calculate Win Rate

1. Open `war_summary.csv`
2. Count "Win" in Result column
3. Divide by total rows
4. Multiply by 100 = Win %

## 🔧 Advanced Features

### Combine Tables into Excel Workbook

After generating tables, run:

```python
import pandas as pd

war_summary = pd.read_csv('war_summary.csv')
member_perf = pd.read_csv('per_war_member_performance.csv')
overall = pd.read_csv('overall_member_performance.csv')

with pd.ExcelWriter('war_analysis.xlsx') as writer:
    war_summary.to_excel(writer, sheet_name='War Summary', index=False)
    member_perf.to_excel(writer, sheet_name='Per-War', index=False)
    overall.to_excel(writer, sheet_name='Overall', index=False)
```

Now you have **one Excel file with 3 tabs**!

## 🆘 Troubleshooting

### "No module named 'war_info'"

**Cause:** Running from wrong directory

**Solution:**
```bash
cd /Users/tomasvalentinas/Documents/coc_bot/war_tracking
./run.sh
```

### "Clan is not currently in war"

**Cause:** No active war

**Solution:** Wait for war to start, then run again

### "No war data directory found"

**Cause:** No wars tracked yet

**Solution:** Use Option 1 to track a war first

### Messages don't appear

**Cause:** Everyone attacked (no missed attacks)

**Solution:** This is good! Messages only show when someone misses attacks

## 📱 Quick Commands

### Run the unified menu:
```bash
cd war_tracking && ./run.sh
```

### Or directly:
```bash
cd war_tracking
source ../env/bin/activate
python war_tracker.py
```

### Open files in Finder:
```bash
cd war_tracking
open .
```

## 🗂️ File Structure

```
war_tracking/
├── war_tracker.py          ⭐ THE UNIFIED SCRIPT (use this!)
├── run.sh                  ⭐ QUICK LAUNCHER
│
├── war_info.py             (underlying functions)
├── generate_tables.py      (legacy - not needed anymore)
├── preview_tables.py       (legacy - not needed anymore)
│
├── README.md               (folder overview)
├── QUICK_GUIDE.md          (how to find messages/tables)
├── RUN_THIS.md             (this file)
│
├── war_summary.csv         📊 Generated by script
├── per_war_member_performance.csv  📊 Generated by script
├── overall_member_performance.csv  📊 Generated by script
│
└── war_data/               📁 Auto-created by script
    └── war_*.json
```

## ✨ Why Use the Unified Script?

**Before:** Multiple scripts to run
- `python war_info.py` → Track war
- `python generate_tables.py` → Make tables
- `python preview_tables.py` → See structure
- `open .` → Find files

**Now:** ONE script with menu
- `./run.sh` → Everything in one place!
- Interactive menu
- No need to remember commands
- Guided workflow

## 🎯 Summary

### To use the unified War Tracker:

1. **Run:** `./run.sh`
2. **Choose option** from menu
3. **Follow prompts**
4. **Done!**

### Most common workflow:

```bash
./run.sh
→ Press 1 (Track war)
→ Copy messages from terminal
→ Press y (Generate tables)
→ Press 8 (Open Finder)
→ Double-click CSV files
→ Analyze in Excel!
```

**That's it!** Everything you need in one unified script.

---

**Created:** January 19, 2026  
**For:** LøpeforbundetFC (#2P0GPYYJY)  
**Author:** War Tracking System v2.0
