# 📍 WHERE IS EVERYTHING? - Visual Guide

## 🎯 Copy-Paste Messages

### Step 1: Run the Script
```bash
cd war_tracking
./run.sh
```

### Step 2: Select Option 1
```
📋 MAIN MENU
1️⃣  Track Current War (Full Analysis)  ← CHOOSE THIS
```

### Step 3: Look for This in Terminal
```
================================================================================
📋 COPY-PASTE MESSAGES FOR DISCORD/CLASH    ← MESSAGES ARE HERE!
================================================================================

Message 1 (65 chars):
❌ NO ATTACKS: @PlayerOne, @PlayerTwo       ← COPY THIS LINE
```

### Step 4: Copy the Message
1. **Click and drag** to select the message text
2. **Cmd+C** to copy
3. **Paste in Clash of Clans** or Discord

**That's it!** The message is ready with @mentions.

---

## 📊 CSV Tables

### Step 1: Generate Tables

Run script and select **Option 3**:
```
3️⃣  Generate All CSV Tables  ← CHOOSE THIS
```

### Step 2: Files Appear Here

```
war_tracking/
├── war_summary.csv                    ← TABLE 1 (War results)
├── per_war_member_performance.csv     ← TABLE 2 (Per-war stats)
└── overall_member_performance.csv     ← TABLE 3 (Overall stats)
```

### Step 3: Open Files

**Option A - From Menu:**
```
8️⃣  Open CSV Files in Finder  ← CHOOSE THIS
```
Finder opens → See all CSV files

**Option B - Double Click:**
1. Open Finder
2. Go to: `/Users/tomasvalentinas/Documents/coc_bot/war_tracking/`
3. Double-click any `.csv` file
4. Opens in Excel/Numbers automatically

---

## 📈 How to View Tables

### Excel (Mac)
```
Double-click war_summary.csv
↓
Opens in Numbers or Excel
↓
Ready to analyze!
```

### Google Sheets
```
Go to sheets.google.com
↓
File → Import → Upload
↓
Choose war_summary.csv
↓
Click Import
↓
Ready to analyze!
```

---

## 🗺️ Complete Visual Map

```
📁 /Users/tomasvalentinas/Documents/coc_bot/
    └── 📁 war_tracking/
        │
        ├── 🚀 war_tracker.py          ⭐ RUN THIS (unified menu)
        ├── 🚀 run.sh                  ⭐ OR THIS (quick launcher)
        │
        ├── 📊 war_summary.csv         ← Tables appear here after generation
        ├── 📊 per_war_member_performance.csv
        ├── 📊 overall_member_performance.csv
        │
        ├── 📁 war_data/               ← War JSON logs stored here
        │   ├── war_2P0GPYYJY_20260119_154611.json
        │   └── war_2P0GPYYJY_20260120_103045.json
        │
        └── 📖 Documentation files
```

---

## 🎬 Step-by-Step Visual Workflow

### Scenario: Track War + Get Messages + View Tables

```
START
  ↓
┌─────────────────────┐
│  cd war_tracking    │
│  ./run.sh           │
└─────────────────────┘
  ↓
┌─────────────────────┐
│  MENU APPEARS       │
│  Press: 1           │
└─────────────────────┘
  ↓
┌─────────────────────┐
│  War data loads...  │
└─────────────────────┘
  ↓
┌────────────────────────────────┐
│  📋 COPY-PASTE MESSAGES        │  ← LOOK HERE IN TERMINAL
│  ❌ NO ATTACKS: @Player1       │  ← COPY THIS
└────────────────────────────────┘
  ↓
┌─────────────────────┐
│  Cmd+C (copy)       │
│  Paste in Clash     │
└─────────────────────┘
  ↓
┌─────────────────────┐
│  Generate tables?   │
│  Press: y           │
└─────────────────────┘
  ↓
┌─────────────────────┐
│  ✅ Tables created  │
└─────────────────────┘
  ↓
┌─────────────────────┐
│  Press Enter        │
│  Back to menu       │
└─────────────────────┘
  ↓
┌─────────────────────┐
│  Press: 8           │
│  (Open Finder)      │
└─────────────────────┘
  ↓
┌─────────────────────┐
│  Finder opens       │
│  See CSV files      │
└─────────────────────┘
  ↓
┌─────────────────────┐
│  Double-click CSV   │
│  Opens in Excel     │
└─────────────────────┘
  ↓
DONE! Analyze data in spreadsheet
```

---

## 🔍 What Each Table Shows

### 1. war_summary.csv
```
Shows: War results, scores, participation rates
Use for: Win/loss tracking, overall clan performance
Example: "We won 15/20 wars with 95% participation"
```

### 2. per_war_member_performance.csv
```
Shows: Individual member stats per war
Use for: See who performed well in specific wars
Example: "PlayerOne got 6 stars in war on Jan 19"
```

### 3. overall_member_performance.csv
```
Shows: Member stats across ALL wars
Use for: Find reliable vs unreliable members
Example: "PlayerTwo has 90% participation rate"
```

---

## 🎯 Quick Reference Card

**Want messages?**
→ `./run.sh` → Press `1` → Look in terminal

**Want tables?**
→ `./run.sh` → Press `3` → Files in same folder

**Want to open tables?**
→ `./run.sh` → Press `8` → Finder opens

**Where are CSV files?**
→ Same directory as `war_tracker.py`

**Where are messages?**
→ In the terminal output after tracking a war

---

## 💡 Remember

### Messages Location:
- ✅ **Terminal output** (after Option 1)
- ✅ Look for "📋 COPY-PASTE MESSAGES"
- ✅ Only appear if someone missed attacks

### Tables Location:
- ✅ **Same folder** as war_tracker.py
- ✅ Named: `war_summary.csv`, etc.
- ✅ Created after Option 3

### How to Open Tables:
- ✅ **Double-click** CSV file
- ✅ Or use **Option 8** in menu
- ✅ Opens in Excel/Numbers automatically

---

**That's all you need to know!**

For more details, see:
- [RUN_THIS.md](RUN_THIS.md) - Complete unified script guide
- [QUICK_GUIDE.md](QUICK_GUIDE.md) - Detailed examples
- [README.md](README.md) - Full documentation
