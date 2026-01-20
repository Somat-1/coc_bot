# 🏰 Clash of Clans Bot & War Tracker

A comprehensive automation and war tracking system for Clash of Clans.

## 📁 Project Structure

```
coc_bot/
├── 🤖 Bot Scripts
│   ├── main.py              # Main bot script
│   ├── main_cont.py         # Continuous attack bot
│   ├── main2.py             # Alternative bot version
│   ├── donate.py            # Donation automation
│   ├── bb_farm.py           # Builder base farming
│   └── event.py             # Event handler
│
├── 🔧 Utilities
│   └── utils/
│       ├── adb_helper.py    # ADB device control
│       └── debug_overlay.py # Debug visualization
│
└── 📊 War Tracking System ⭐
    └── war_tracking/        # Complete war tracking & analysis
        ├── README.md        # Full documentation
        ├── START_HERE.md    # Quick start guide
        └── ...              # See war_tracking/README.md
```

## 🚀 Quick Start

### Bot Scripts
```bash
# Main bot
python3 main.py

# Main continuous bot
python3 main_cont.py

# Donation bot
python3 donate.py
```

### War Tracking System ⭐
```bash
cd war_tracking
./run.sh
```

**For complete war tracking documentation, see: [`war_tracking/START_HERE.md`](war_tracking/START_HERE.md)**

## 📊 War Tracking Features

The war tracking system provides comprehensive clan war analysis:

- ✅ **Real-time war tracking** via Clash of Clans API
- ✅ **Individual attack analysis** (stars + destruction % per attack)
- ✅ **Copy-paste messages** for missed attacks (≤240 chars, max 5 names)
- ✅ **Excel tables** with professional formatting and color-coding
- ✅ **CSV tables** for basic analysis
- ✅ **Automatic data storage** with unique filenames
- ✅ **Performance warnings** (yellow for 2 consecutive misses, red for 3+)
- ✅ **Unified menu system** with 11 options

### Example Output

**Messages:**
```
❌ NO ATTACKS: @Player1, @Player2, @Player3, @Player4, @Player5
⚠️ PARTIAL ATTACKS: @Player6, @Player7
```

**Excel Tables:**
- Per-war performance (separate sheet per war)
- Overall member statistics (with color-coded warnings)
- Individual attack tracking (Attack 1 & 2 separately)

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [`README.md`](README.md) | This file - project overview |
| [`war_tracking/START_HERE.md`](war_tracking/START_HERE.md) | Quick start for war tracking |
| [`war_tracking/README.md`](war_tracking/README.md) | Complete war tracking guide |
| [`war_tracking/EXCEL_GUIDE.md`](war_tracking/EXCEL_GUIDE.md) | Excel features & color-coding |
| [`war_tracking/COMPLETION_CHECKLIST.md`](war_tracking/COMPLETION_CHECKLIST.md) | Project status |

## 🔧 Requirements

### Bot Scripts
- Python 3.x
- ADB (Android Debug Bridge)
- Android emulator or device
- Required packages: (see requirements in each script)

### War Tracking System
```bash
pip3 install requests openpyxl
```

## 🎯 Features by Module

### 🤖 Bot Automation
- **Attack Automation**: Automated attacking with loot detection
- **Donation System**: Auto-donate troops to clan members
- **Builder Base**: Automated builder base farming
- **Event Handling**: Clan games and event automation

### 📊 War Tracking
- **API Integration**: Real-time data from Clash of Clans API
- **Attack Analysis**: Individual attack tracking with stars and destruction %
- **Member Performance**: Participation rates, average stars, destruction %
- **Message Generation**: Auto-formatted messages for clan chat
- **Excel Reports**: Professional tables with color-coded warnings
- **Historical Data**: Track performance across multiple wars

## 🆘 Support

### Bot Issues
- Check ADB connection: `adb devices`
- Verify emulator is running
- Review script logs for errors

### War Tracking Issues
- See [`war_tracking/README.md`](war_tracking/README.md)
- Verify API key in `war_tracking/war_info.py`
- Check clan tag configuration

## 📝 License

Personal project for Clash of Clans automation and analysis.

## 🏆 Credits

**Clan**: LøpeforbundetFC (#2P0GPYYJY)  
**Date**: January 2026  
**Status**: ✅ Production Ready

---

**⚠️ Important**: Use bot features responsibly and in accordance with game terms of service.

**📊 War Tracking**: Fully compliant with Clash of Clans API terms.

---

**For war tracking, start here:** [`war_tracking/START_HERE.md`](war_tracking/START_HERE.md)
