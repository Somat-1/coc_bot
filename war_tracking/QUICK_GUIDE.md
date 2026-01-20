# 📊 Quick Guide: Where to Find Everything

## 🎯 Where to Find Copy-Paste Messages

### When War is Active

Run the script:
```bash
cd war_tracking
source ../env/bin/activate
python war_info.py
```

### Messages Appear in Terminal

Look for this section in the console output:

```
================================================================================
📋 COPY-PASTE MESSAGES FOR DISCORD/CLASH
================================================================================

Message 1 (65 chars):
❌ NO ATTACKS: @PlayerOne, @PlayerTwo

Message 2 (42 chars):
⚠️ PARTIAL ATTACKS: @PlayerThree
```

### How to Use the Messages

1. **Copy the message** (select and Cmd+C on Mac)
2. **Paste in Clash of Clans chat** or **Discord**
3. Messages are already formatted with @mentions
4. Each message is under 240 characters

### When Messages Appear

- **Only when war is ACTIVE** (not preparation phase)
- **Only if someone missed attacks**
- If everyone attacked, no messages will show

---

## 📈 Where to Find CSV Tables

### Location

After running `python war_info.py`, three CSV files are created in the **same directory**:

```
war_tracking/
├── war_info.py
├── war_summary.csv                        ← HERE
├── per_war_member_performance.csv         ← HERE
├── overall_member_performance.csv         ← HERE
└── war_data/
```

### Table Files

1. **`war_summary.csv`** - Overview of all wars
2. **`per_war_member_performance.csv`** - Detailed member stats per war
3. **`overall_member_performance.csv`** - Aggregate member performance

---

## 📊 How to Visualize the Tables

### Option 1: Excel (Easiest)

#### On Mac:
1. Open **Finder**
2. Navigate to: `/Users/tomasvalentinas/Documents/coc_bot/war_tracking/`
3. **Double-click** any CSV file (e.g., `war_summary.csv`)
4. Excel/Numbers will open automatically

#### In Excel:
- ✅ Sort columns (click column header → Sort)
- ✅ Filter data (Data → Filter)
- ✅ Create charts (Insert → Chart)
- ✅ Calculate totals (use SUM, AVERAGE formulas)

**Example Analysis:**
```
1. Open overall_member_performance.csv
2. Sort by "Full Participation Rate %" (descending)
3. See who has best attendance!
```

### Option 2: Google Sheets (Cloud-based)

1. Go to [sheets.google.com](https://sheets.google.com)
2. Click **File → Import**
3. Click **Upload** tab
4. Drag and drop the CSV file (e.g., `war_summary.csv`)
5. Choose "Replace spreadsheet" or "Insert new sheet"
6. Click **Import data**

**Advantages:**
- ✅ Share with clan leadership
- ✅ Collaborative editing
- ✅ Access from any device
- ✅ Auto-save

### Option 3: Visual Studio Code (Quick Preview)

If you're already in VS Code:

1. **Right-click** on any CSV file
2. Select **Open Preview** or **Edit in Excel**
3. Or install "Rainbow CSV" extension for colored columns

### Option 4: Terminal (Quick Check)

```bash
cd war_tracking

# View first 10 lines
head war_summary.csv

# View with column formatting
column -s, -t < war_summary.csv | head

# Count total wars tracked
wc -l war_summary.csv
```

---

## 🎨 Visualizing Data in Excel/Google Sheets

### Create Charts

#### Win/Loss Over Time (from war_summary.csv)

1. Open `war_summary.csv`
2. Select columns: `War Date` and `Result`
3. Insert → Pie Chart or Bar Chart
4. See win/loss distribution!

#### Member Participation Rate (from overall_member_performance.csv)

1. Open `overall_member_performance.csv`
2. Select: `Member Name` and `Full Participation Rate %`
3. Insert → Bar Chart (horizontal)
4. Sort by participation rate
5. See who's most reliable!

#### Stars per Attack Comparison

1. Open `overall_member_performance.csv`
2. Select: `Member Name` and `Avg Stars per Attack`
3. Insert → Column Chart
4. See who's most effective!

### Color-Code Problem Members

In Excel/Google Sheets:

1. Select the "Wars Missed (No Attacks)" column
2. **Conditional Formatting** → Color Scale
   - Red = High (many missed wars)
   - Green = Low (few missed wars)
3. Instantly see who needs attention!

### Filter for Specific Issues

**Example: Find members who miss wars frequently**

1. Open `overall_member_performance.csv`
2. Click "Data → Filter" (or Ctrl+Shift+L)
3. Click filter dropdown on "Wars Missed (No Attacks)"
4. Select "> 2" (more than 2 missed wars)
5. See only problem members!

---

## 📁 Complete File Structure

```
war_tracking/
├── README.md                              📖 Main overview
├── war_info.py                            🔧 Main script
├── generate_tables.py                     🔧 Table generator only
├── preview_tables.py                      👁️  Preview tool
│
├── WAR_TRACKING_README.md                 📖 Basic usage
├── WAR_ANALYSIS_GUIDE.md                  📖 API limitations
├── TABLE_GENERATION_GUIDE.md              📖 Detailed tables guide
├── IMPLEMENTATION_COMPLETE.md             📖 Project summary
│
├── war_summary.csv                        📊 War overview table
├── per_war_member_performance.csv         📊 Per-war member stats
├── overall_member_performance.csv         📊 Overall member stats
│
└── war_data/                              📁 JSON war logs
    ├── war_2P0GPYYJY_20260119_154611.json
    ├── war_2P0GPYYJY_20260120_103045.json
    └── ...
```

---

## 🚀 Complete Workflow Example

### Step 1: Track a War

```bash
cd /Users/tomasvalentinas/Documents/coc_bot/war_tracking
source ../env/bin/activate
python war_info.py
```

**Output in terminal:**
- War information
- Participation summary
- 📋 **COPY-PASTE MESSAGES** ← Copy these!
- CSV tables generated

### Step 2: Copy Messages

From terminal output:
```
📋 COPY-PASTE MESSAGES FOR DISCORD/CLASH
================================================================================

Message 1 (65 chars):
❌ NO ATTACKS: @PlayerOne, @PlayerTwo
```

1. **Select the message text** (not the "Message 1" part)
2. **Cmd+C** to copy
3. **Paste in Clash of Clans** or Discord

### Step 3: Open Tables in Excel

```bash
# From Finder:
open .
```

Or navigate to: `/Users/tomasvalentinas/Documents/coc_bot/war_tracking/`

Double-click:
- `war_summary.csv` → See war results
- `overall_member_performance.csv` → See member stats

### Step 4: Analyze Data

**Find unreliable members:**
1. Open `overall_member_performance.csv`
2. Sort by "Wars Missed (No Attacks)" (descending)
3. Members at top = most missed wars

**Find best performers:**
1. Sort by "Avg Stars per Attack" (descending)
2. Members at top = highest average stars

**Calculate win rate:**
1. Open `war_summary.csv`
2. Count "Win" in Result column
3. Divide by total wars
4. Multiply by 100 for percentage

---

## 💡 Pro Tips

### Combine All Tables in One Excel File

Create an Excel workbook with multiple sheets:

```python
# Create this file: combine_tables.py
import pandas as pd

war_summary = pd.read_csv('war_summary.csv')
member_perf = pd.read_csv('per_war_member_performance.csv')
overall = pd.read_csv('overall_member_performance.csv')

with pd.ExcelWriter('war_analysis.xlsx') as writer:
    war_summary.to_excel(writer, sheet_name='War Summary', index=False)
    member_perf.to_excel(writer, sheet_name='Per-War Performance', index=False)
    overall.to_excel(writer, sheet_name='Overall Performance', index=False)

print("✅ Created war_analysis.xlsx with 3 sheets!")
```

Run with:
```bash
python combine_tables.py
```

Now you have **one Excel file with 3 tabs**!

### Share with Leadership

**Upload to Google Drive:**
1. Drag CSV files to Google Drive
2. Right-click → Open with → Google Sheets
3. Share link with co-leaders

**Export as PDF:**
1. Open in Excel/Google Sheets
2. File → Download → PDF
3. Share PDF via email/Discord

---

## 🆘 Troubleshooting

### "No CSV files found"
- **Cause:** No wars tracked yet
- **Solution:** Wait for war to be active, run `python war_info.py`

### "CSV shows no data"
- **Cause:** War is in preparation phase
- **Solution:** Run script again when war battle day starts

### "Can't find the files"
- **Location:** `/Users/tomasvalentinas/Documents/coc_bot/war_tracking/`
- Use Finder or:
  ```bash
  cd /Users/tomasvalentinas/Documents/coc_bot/war_tracking
  ls -l *.csv
  ```

### "Messages don't appear"
- **Cause:** Everyone attacked or war not started
- **Messages only show if someone missed attacks**

---

## 📱 Quick Reference

### To Track War:
```bash
cd war_tracking && source ../env/bin/activate && python war_info.py
```

### To Regenerate Tables:
```bash
cd war_tracking && source ../env/bin/activate && python generate_tables.py
```

### To Open Files:
```bash
cd war_tracking && open .
```

### Files to Open:
- **war_summary.csv** → War results
- **overall_member_performance.csv** → Member stats
- **per_war_member_performance.csv** → Detailed breakdown

### Messages Location:
- **Terminal output** after running `war_info.py`
- Look for: "📋 COPY-PASTE MESSAGES"
- Copy and paste into Clash/Discord

---

**Created:** January 19, 2026  
**For:** LøpeforbundetFC Clan (#2P0GPYYJY)
