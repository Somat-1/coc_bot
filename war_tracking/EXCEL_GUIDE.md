# 📊 Excel Table Generation Guide

## Overview

The war tracking system now generates **beautifully formatted Excel files** with:
- ✅ Separate worksheets for each war
- ✅ Color-coded performance warnings
- ✅ Professional formatting with borders and headers
- ✅ Auto-sized columns for easy reading
- ✅ Individual attack tracking (stars + destruction % for each attack)

---

## 📁 Generated Files

### 1. **per_war_member_performance.xlsx**
- **Format**: One worksheet per war
- **Sheet Name**: "War {#} - {Opponent Name}"
- **Columns**:
  - Member Name
  - Attacks Used
  - Stars Obtained
  - Average %
  - Attack 1 Stars
  - Attack 1 %
  - Attack 2 Stars
  - Attack 2 %

**Features**:
- Sorted by total stars (highest first)
- Blue header row with white text
- All data cells have borders
- Centered alignment for numbers

---

### 2. **overall_member_performance.xlsx**
- **Format**: Single worksheet
- **Sheet Name**: "Overall Performance"
- **Columns**:
  - Member Name
  - Wars Participated
  - Wars Missed (Attacks)
  - Average Stars per War
  - Average % per War

**Features**:
- **🟡 Yellow highlighting**: 2 consecutive missed wars
- **🔴 Red highlighting**: 3+ consecutive missed wars
- Legend at bottom explaining color codes
- Sorted by wars participated (most active first)

---

## 🚀 How to Generate

### Option 1: Use the War Tracker Menu
```bash
cd war_tracking
./run.sh
# Select option 7: Generate All Excel Tables
```

### Option 2: Run Directly
```bash
cd war_tracking
python3 generate_excel_tables.py
```

### Option 3: Import in Python
```python
from generate_excel_tables import generate_all_excel_tables
generate_all_excel_tables()
```

---

## 📋 Requirements

The system uses the **openpyxl** library for Excel generation:
```bash
pip3 install openpyxl
```

*Already installed in your environment!*

---

## 🎨 Color Coding Explained

### Overall Performance Table

| Color | Meaning | Trigger |
|-------|---------|---------|
| 🟡 **Yellow** | Warning | Member missed attacks in **2 consecutive wars** |
| 🔴 **Red** | Critical | Member missed attacks in **3+ consecutive wars** |

**Note**: "Missed attacks" includes:
- Wars where the member used 0/2 attacks
- Wars where the member used 1/2 attacks (partial)

---

## 💡 Tips

### Opening Excel Files
- **macOS**: Double-click the .xlsx file
- **Windows**: Double-click or right-click → Open with Excel
- **Google Sheets**: Upload the file to Google Drive

### Best Practices
1. Generate Excel tables after tracking each war
2. Review color-coded warnings to identify inactive members
3. Use per-war sheets to analyze individual war performance
4. Compare Attack 1 vs Attack 2 stats to see improvement patterns

### File Location
All files are saved in:
```
/Users/tomasvalentinas/Documents/coc_bot/war_tracking/
```

---

## 🔍 Example Output

### Per-War Table (War 1 - Gorkhali)
```
Member Name    | Attacks Used | Stars | Avg % | Attack 1 Stars | Attack 1 % | Attack 2 Stars | Attack 2 %
---------------|--------------|-------|-------|----------------|------------|----------------|----------
TopPlayer      | 2            | 6     | 95.0  | 3              | 94.0       | 3              | 96.0
GoodPlayer     | 2            | 5     | 88.5  | 2              | 85.0       | 3              | 92.0
PartialPlayer  | 1            | 2     | 75.0  | 2              | 75.0       |                |
InactivePlayer | 0            | 0     | 0.0   |                |            |                |
```

### Overall Performance Table
```
Member Name    | Wars Participated | Wars Missed | Avg Stars | Avg %  | Color
---------------|-------------------|-------------|-----------|--------|-------
TopPlayer      | 5                 | 0           | 5.40      | 92.5   | -
PartialPlayer  | 5                 | 2           | 3.20      | 68.0   | 🟡 Yellow
InactivePlayer | 5                 | 3           | 1.00      | 25.0   | 🔴 Red
```

---

## 📊 Data Source

Excel tables are generated from JSON war data stored in:
```
war_data/war_{CLAN_TAG}_{DATE}_{TIME}.json
```

Make sure to **track wars first** before generating Excel tables!

---

## ✅ Verification

After generation, you should see:
```
✅ Per-war member performance Excel saved to: per_war_member_performance.xlsx
   Total wars: X sheets

✅ Overall member performance Excel saved to: overall_member_performance.xlsx
   Total members: X
```

Files will appear in the `war_tracking/` directory.

---

## 🆘 Troubleshooting

### "No war data files found"
- Run option 1 in the menu to track current war first
- Check that `war_data/` directory exists and has .json files

### Import errors
- Make sure you're in the `war_tracking/` directory
- Verify openpyxl is installed: `pip3 install openpyxl`

### Empty worksheets
- Verify JSON files in `war_data/` have valid war data
- Check that wars are not in "preparation" state

---

**🎉 Enjoy your beautifully formatted war statistics!**
