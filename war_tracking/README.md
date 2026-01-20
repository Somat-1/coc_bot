# 🏰 Clash of Clans War Tracking System

A comprehensive war tracking and analysis system for Clash of Clans clans using the official CoC API.

## 📁 Directory Structure

```
war_tracking/
├── README.md                           # This file - main overview
├── war_info.py                         # Main script - tracks wars and generates tables
├── generate_tables.py                  # Standalone table generator
├── preview_tables.py                   # Preview table structure
├── WAR_TRACKING_README.md              # Basic usage guide
├── WAR_ANALYSIS_GUIDE.md               # API limitations explained
├── TABLE_GENERATION_GUIDE.md           # Comprehensive table documentation
├── IMPLEMENTATION_COMPLETE.md          # Project completion summary
└── war_data/                           # Auto-created directory for JSON war logs
    ├── war_2P0GPYYJY_20260119_154611.json
    ├── war_2P0GPYYJY_20260120_103045.json
    └── ...
```

## 🚀 Quick Start

### ⭐ NEW: Unified Menu System (Easiest!)

**ONE script for everything:**

```bash
cd war_tracking
./run.sh
```

Interactive menu with all features:
- Track wars
- Generate tables
- View history
- Open files in Finder
- View statistics

**See [RUN_THIS.md](RUN_THIS.md) for complete guide!**

### Alternative: Direct Commands

#### 1. Basic Usage

Track the current war and generate all reports:

```bash
cd war_tracking
source ../env/bin/activate
python war_info.py
```

This will:
- ✅ Fetch current war data from CoC API
- ✅ Show who attacked and who didn't
- ✅ Generate @mention messages for missed attacks (under 240 chars)
- ✅ Auto-save war data to JSON file
- ✅ Generate 3 CSV tables with comprehensive statistics

#### 2. Generate Tables Only

Regenerate CSV tables from existing war data:

```bash
python generate_tables.py
```

#### 3. Preview Table Structure

See what the CSV tables will contain:

```bash
python preview_tables.py
```

## 📊 Output Files

### CSV Tables (Generated Automatically)

1. **`war_summary.csv`** - Overview of all wars
   - War dates, results (Win/Loss/Tie)
   - Stars and destruction percentages
   - Team size and participation rates

2. **`per_war_member_performance.csv`** - Member stats per war
   - Individual member performance in each war
   - Attack status (All/Partial/None)
   - Detailed attack statistics

3. **`overall_member_performance.csv`** - Aggregate member stats
   - Performance across all tracked wars
   - Participation rates
   - Average stars and destruction

### JSON War Logs

Stored in `war_data/` directory:
- Format: `war_{CLAN_TAG}_{DATE}_{TIME}.json`
- Contains complete war data including member analysis
- Updated if same war is polled multiple times

## 🎯 Features

### ✅ Real-Time War Tracking
- Tracks member attack performance during active wars
- Categorizes members: All attacks (2/2), Partial (1/2), None (0/2)
- Shows detailed stats: stars, destruction %, best attack

### ✅ Missed Attack Notifications
- Automatically identifies who hasn't attacked
- Generates Discord/Clash-ready messages with @mentions
- Respects 240 character limit (splits into multiple messages)
- Separate messages for "NO ATTACKS" and "PARTIAL ATTACKS"

### ✅ Automatic Data Storage
- Auto-saves war data to unique JSON files
- Filename based on war start time (prevents duplicates)
- Creates `war_data/` directory automatically
- Updates existing file if war is polled multiple times

### ✅ Comprehensive Analytics
- War summary across all tracked wars
- Per-war member performance breakdown
- Overall member performance aggregation
- Identify reliable vs unreliable members
- Track improvement over time

## 📖 Documentation

- **[WAR_TRACKING_README.md](WAR_TRACKING_README.md)** - Basic usage and setup
- **[WAR_ANALYSIS_GUIDE.md](WAR_ANALYSIS_GUIDE.md)** - API limitations and data collection
- **[TABLE_GENERATION_GUIDE.md](TABLE_GENERATION_GUIDE.md)** - Complete guide to CSV tables ⭐ Most comprehensive
- **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** - Project completion summary

## ⚙️ Configuration

Edit `war_info.py` to configure:

```python
# API Configuration
API_KEY = "your-api-key-here"           # Get from https://developer.clashofclans.com/
CLAN_TAG = "#2P0GPYYJY"                 # Your clan tag

# Settings
WAR_DATA_DIR = "war_data"               # Directory for JSON war logs
MESSAGE_CHAR_LIMIT = 240                # Character limit for messages
```

## 🔧 Requirements

- Python 3.13+ (installed in `../env/`)
- `requests` library (already installed)
- Valid CoC API key (already configured)

## 💡 Use Cases

### For Leaders/Co-Leaders
- Track who consistently misses attacks
- Identify top performers for promotions
- Monitor clan participation trends
- Make data-driven membership decisions
- Share copy-paste messages in clan chat

### For Members
- View personal war statistics
- Track improvement over time
- Compare performance with others

### For Analysis
- Calculate win/loss ratios
- Correlate participation with outcomes
- Identify behavioral patterns
- Generate leadership reports

## 📝 Example Output

### Console Output (Active War)
```
📊 PARTICIPATION SUMMARY
================================================================================
✅ Used all attacks (2/2): 22 members
⚠️  Partial attacks: 1 members
❌ No attacks: 2 members

📋 COPY-PASTE MESSAGES FOR DISCORD/CLASH
================================================================================

Message 1 (65 chars):
❌ NO ATTACKS: @PlayerOne, @PlayerTwo

Message 2 (42 chars):
⚠️ PARTIAL ATTACKS: @PlayerThree
```

### CSV Tables
Three ready-to-analyze CSV files:
- Open in Excel, Google Sheets, or any spreadsheet software
- Sort, filter, and create charts
- Share with leadership team

## 🔄 Workflow

### During War Season

1. **When war starts:**
   ```bash
   python war_info.py
   ```

2. **During war (check progress):**
   ```bash
   python war_info.py
   ```

3. **When war ends:**
   ```bash
   python war_info.py
   ```

4. **Analyze results:**
   - Open the 3 CSV files in Excel/Google Sheets
   - Review participation and performance

### After Multiple Wars

```bash
python generate_tables.py
```

Regenerates all tables with updated aggregate statistics.

## 🤖 Automation

Set up a cron job to run automatically:

```bash
# Run every 2 hours during war day
0 */2 * * * cd /Users/tomasvalentinas/Documents/coc_bot/war_tracking && source ../env/bin/activate && python war_info.py
```

## 🆘 Troubleshooting

### "No war data directory found"
- **Cause:** No wars tracked yet
- **Solution:** Run script when a war is active

### "Clan is not currently in war"
- **Cause:** No active war
- **Solution:** Wait for war to start

### Empty CSV files
- **Cause:** Tables generated before tracking any wars
- **Solution:** Track at least one war, then run `generate_tables.py`

## 📊 Current Status

**Clan:** LøpeforbundetFC (#2P0GPYYJY)  
**Implementation:** Complete ✅  
**All Features:** Fully functional ✅

## 🔗 Related Files

All war tracking functionality is self-contained in this directory. The main bot scripts in the parent directory are separate.

## 📞 Support

For detailed information, see the documentation files:
- Usage questions → `WAR_TRACKING_README.md`
- API limitations → `WAR_ANALYSIS_GUIDE.md`
- Table analysis → `TABLE_GENERATION_GUIDE.md`

---

**Created:** January 19, 2026  
**Status:** Production Ready  
**Version:** 1.0
