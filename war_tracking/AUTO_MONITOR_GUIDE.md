# 🤖 Auto-Monitor War Guide

## Overview

The **Auto-Monitor** feature provides continuous, automated war tracking that intelligently adjusts update frequency based on time remaining until war ends.

---

## 🚀 How to Use

### Method 1: From Menu
```bash
cd war_tracking
./run.sh
# Select option 2: Auto-Monitor War
```

### Method 2: Direct Command
```bash
cd war_tracking
python3 auto_war_monitor.py
```

---

## ⚙️ How It Works

### 1. Initial Check
- Fetches current war status
- Calculates time until war ends
- Checks if monitoring should start

### 2. Monitoring Rules
| Time Remaining | Status | Action |
|----------------|--------|--------|
| > 3 hours | 🟡 Waiting | Asks if you want to wait until 3h remaining |
| < 3 hours | 🟢 Monitoring | Starts continuous monitoring |
| < 10 minutes | 🔴 Final Phase | Increases update frequency |
| War Ended | 🏁 Complete | Saves final data & generates tables |

### 3. Update Schedule
- **Normal Phase** (> 10 minutes remaining):
  - Update every **30 minutes**
  - Status: 🟢 MONITORING

- **Final Phase** (< 10 minutes remaining):
  - Update every **2 minutes**
  - Status: 🔴 FINAL PHASE

- **War End**:
  - Final data update
  - Automatic table generation (CSV + Excel)
  - Monitoring stops

---

## 📊 What It Does

### During Monitoring
1. ✅ Fetches current war data
2. ✅ Categorizes members (full/partial/no attacks)
3. ✅ Tracks individual attacks (stars + destruction %)
4. ✅ Saves data with unique filename
5. ✅ Shows quick stats after each update
6. ✅ Displays time remaining

### When War Ends
1. ✅ Performs final data fetch
2. ✅ Saves complete war data
3. ✅ Generates CSV tables
4. ✅ Generates Excel tables
5. ✅ Shows summary of generated files
6. ✅ Stops monitoring

---

## 📋 Example Session

```
================================================================================
🏰 AUTOMATED WAR MONITOR
================================================================================
Clan: #2P0GPYYJY
Started: 2026-01-20 12:00:00
================================================================================

🔍 Checking current war status...

⏰ Time until war end: 2h 45m 30s

================================================================================
🚀 STARTING CONTINUOUS MONITORING
================================================================================
⏰ Monitoring started at: 2026-01-20 12:00:00
⏱️  Time remaining: 2h 45m 30s

📋 Update Schedule:
   • Every 30 minutes (normal)
   • Every 2 minutes (last 10 minutes)
   • Auto-save when war ends

💡 Press Ctrl+C to stop monitoring
================================================================================

[🟢 MONITORING] Update #1 - 2h 45m 0s remaining
================================================================================
🔄 UPDATING WAR DATA - 2026-01-20 12:00:30
================================================================================
...
✅ Data saved to: war_2P0GPYYJY_20260120_120030.json
✅ Update #1 completed
📊 Quick Stats:
   Score: 70⭐ vs 65⭐
   Attacks: 13 full, 2 partial, 10 missed
⏰ Next update in: 30m 0s

[🟢 MONITORING] Update #2 - 2h 15m 0s remaining
...

[🔴 FINAL PHASE] Update #15 - 8m 0s remaining
...

[🔴 FINAL PHASE] Update #18 - 2m 0s remaining
...

================================================================================
🏁 WAR HAS ENDED!
================================================================================

📊 Performing final data update...
✅ Data saved to: war_2P0GPYYJY_20260120_154611.json

================================================================================
📊 GENERATING FINAL TABLES
================================================================================
✅ All tables generated successfully!

================================================================================
✅ MONITORING COMPLETE
================================================================================
Total updates performed: 19
Final data saved to: war_data/
Tables generated:
  • CSV: war_summary.csv
  • CSV: per_war_member_performance.csv
  • CSV: overall_member_performance.csv
  • Excel: per_war_member_performance.xlsx
  • Excel: overall_member_performance.xlsx
================================================================================
```

---

## 💡 Tips & Best Practices

### When to Start Monitoring
- **Recommended**: Start 2-3 hours before war end
- **Latest**: Start in last 10 minutes (updates every 2 min)
- **Earliest**: Can start anytime, will wait until 3h remaining

### Running in Background
```bash
# Run in background (macOS/Linux)
nohup python3 auto_war_monitor.py > monitor.log 2>&1 &

# Check process
ps aux | grep auto_war_monitor

# View logs
tail -f monitor.log

# Stop monitoring
kill <process_id>
```

### Using tmux/screen
```bash
# Start tmux session
tmux new -s war_monitor

# Run monitor
python3 auto_war_monitor.py

# Detach: Ctrl+B then D
# Reattach: tmux attach -t war_monitor
```

---

## 🛑 Stopping Monitoring

### From Terminal
- Press `Ctrl+C` to stop
- Current progress is saved
- Tables won't be auto-generated (war not ended)

### What Happens
```
⚠️  MONITORING STOPPED BY USER
================================================================================
Updates performed: 5
💡 Run this script again to resume monitoring
================================================================================
```

---

## 📊 Data Saved

### During Monitoring
- Each update creates/updates: `war_data/war_{CLANTAG}_{DATE}_{TIME}.json`
- Same war = same filename (overwritten with latest data)

### After War Ends
- Final JSON file in `war_data/`
- CSV files: `war_summary.csv`, `per_war_member_performance.csv`, `overall_member_performance.csv`
- Excel files: `per_war_member_performance.xlsx`, `overall_member_performance.xlsx`

---

## ⚠️ Troubleshooting

### "Could not fetch war data"
- Check internet connection
- Verify API key in `war_info.py`
- Check if clan is in war

### "War is in preparation phase"
- Monitoring only works during active wars
- Wait for war to start
- Run again when war begins

### Script Exits Immediately
- War may have already ended
- Check war state: `python3 -c "from war_info import get_current_war, CLAN_TAG; print(get_current_war(CLAN_TAG).get('state'))"`

### Updates Not Happening
- Check time remaining
- Verify update interval (30min or 2min)
- Look for error messages
- Check API rate limits

---

## 🔍 Monitoring Status

### Status Indicators
- 🟢 **MONITORING**: Normal phase (>10min remaining)
- 🔴 **FINAL PHASE**: Last 10 minutes
- 🏁 **WAR ENDED**: Monitoring complete

### Quick Stats Shown
- Current score (stars)
- Attack participation
  - Full attackers (2/2)
  - Partial attackers (1/2)
  - No attacks (0/2)
- Time until next update

---

## 🎯 Use Cases

### Use Case 1: War Leader
- Start monitoring 3 hours before war end
- Monitor member participation in real-time
- Get instant notifications when war ends
- Share final tables with clan immediately

### Use Case 2: Data Collection
- Start at war beginning
- Let it run continuously
- Collect data throughout entire war
- Analyze attack patterns over time

### Use Case 3: Last-Minute Check
- Start in final 10 minutes
- High-frequency updates (every 2 min)
- Catch last-minute attacks
- Ensure complete data capture

---

## 📈 Performance

### Resource Usage
- **CPU**: Minimal (sleeps between checks)
- **Memory**: < 50MB
- **Network**: API calls only during updates
- **Disk**: ~1-2KB per JSON update

### API Rate Limits
- Clash of Clans API: ~10 requests/second
- This script: 1 request every 2-30 minutes
- Well within limits ✅

---

## 🆚 Comparison

| Feature | Manual Tracking | Auto-Monitor |
|---------|----------------|--------------|
| Updates | Manual | Automatic |
| Frequency | On-demand | 30min / 2min |
| War End Detection | Manual | Automatic |
| Table Generation | Manual | Automatic |
| Monitoring Time | N/A | 2-3 hours typical |
| Hands-free | ❌ | ✅ |

---

## 🎉 Benefits

1. ✅ **Hands-free**: Set it and forget it
2. ✅ **Accurate**: Never miss final war data
3. ✅ **Timely**: Auto-generates tables immediately
4. ✅ **Complete**: Captures all attacks including last-minute
5. ✅ **Intelligent**: Adjusts frequency based on time remaining
6. ✅ **Reliable**: Handles errors gracefully
7. ✅ **Informative**: Shows progress and stats

---

## 🚀 Quick Commands

```bash
# Start monitoring
python3 auto_war_monitor.py

# Check current war timing
python3 -c "from war_info import get_current_war, CLAN_TAG; from datetime import datetime, timezone; war=get_current_war(CLAN_TAG); end=datetime.strptime(war['endTime'], '%Y%m%dT%H%M%S.%fZ').replace(tzinfo=timezone.utc); print(f'Time remaining: {(end-datetime.now(timezone.utc)).total_seconds()/3600:.2f}h')"

# View monitoring log (if running in background)
tail -f monitor.log
```

---

**💡 Tip**: Start auto-monitor 3 hours before war ends for best results!

**⚠️ Note**: Requires active internet connection and valid API key.

**🎯 Best for**: War leaders, data analysts, competitive clans
