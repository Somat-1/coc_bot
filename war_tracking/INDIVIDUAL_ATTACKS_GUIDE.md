# 🎯 Individual Attack Tracking Guide

## Overview

The system now tracks **each individual attack** separately with full details including:
- ⭐ Stars earned
- 💥 Destruction percentage
- 📊 Attack order

---

## 📡 Data Source

### API Endpoint
```
GET /clans/{clanTag}/currentwar
```

### JSON Structure
```json
{
  "clan": {
    "members": [
      {
        "name": "PlayerName",
        "tag": "#TAG",
        "attacks": [
          {
            "attackerTag": "#TAG",
            "defenderTag": "#DEFENDER_TAG",
            "stars": 3,
            "destructionPercentage": 100,
            "order": 1
          },
          {
            "attackerTag": "#TAG",
            "defenderTag": "#DEFENDER_TAG2",
            "stars": 2,
            "destructionPercentage": 85,
            "order": 5
          }
        ]
      }
    ]
  }
}
```

---

## 💾 How It's Stored

### 1. War Data JSON (`war_data/war_*.json`)

The raw API response is saved with the full `members` array:

```json
{
  "clan": {
    "name": "LøpeforbundetFC",
    "tag": "#2P0GPYYJY",
    "members": [
      {
        "name": "gooner",
        "tag": "#GRVJ9CRJL",
        "attacks": [
          {
            "stars": 3,
            "destructionPercentage": 100,
            "order": 10
          },
          {
            "stars": 3,
            "destructionPercentage": 100,
            "order": 15
          }
        ]
      }
    ]
  }
}
```

**Key Update**: The `save_war_data_unique()` function now includes:
```python
"clan": {
    "members": members  # ⭐ Raw members data with individual attacks
}
```

---

## 📊 Excel Table Display

### Per-War Performance Sheet

Each war gets its own worksheet with columns:

| Column | Description | Example |
|--------|-------------|---------|
| Member Name | Player name | "gooner" |
| Attacks Used | Total attacks made | 2 |
| Stars Obtained | Total stars | 6 |
| Average % | Avg destruction | 100.0 |
| Attack 1 Stars | First attack stars | 3 |
| Attack 1 % | First attack destruction | 100.0 |
| Attack 2 Stars | Second attack stars | 3 |
| Attack 2 % | Second attack destruction | 100.0 |

**Example Output**:
```
┌─────────────┬──────────┬───────┬─────────┬──────────┬──────────┬──────────┬──────────┐
│ Member Name │ Attacks  │ Stars │ Avg %   │ Atk1 ⭐  │ Atk1 %   │ Atk2 ⭐  │ Atk2 %   │
├─────────────┼──────────┼───────┼─────────┼──────────┼──────────┼──────────┼──────────┤
│ gooner      │    2     │   6   │  100.0  │    3     │   100.0  │    3     │   100.0  │
│ Piotreknor  │    2     │   5   │   93.5  │    2     │    87.0  │    3     │   100.0  │
│ Marcus      │    1     │   3   │  100.0  │    3     │   100.0  │          │          │
│ Inactive    │    0     │   0   │    0.0  │          │          │          │          │
└─────────────┴──────────┴───────┴─────────┴──────────┴──────────┴──────────┴──────────┘
```

---

## 🔍 Implementation Details

### Code Flow

1. **API Call** (`get_current_war()`)
   ```python
   response = requests.get(
       f"{API_BASE_URL}/clans/%23{clan_tag}/currentwar",
       headers={"Authorization": f"Bearer {API_KEY}"}
   )
   war_data = response.json()
   ```

2. **Extract Members** (`log_current_war_attacks()`)
   ```python
   members = war_data.get("clan", {}).get("members", [])
   ```

3. **Save Raw Data** (`save_war_data_unique()`)
   ```python
   war_log_data = {
       "clan": {
           "members": members  # ⭐ Full member data with attacks
       }
   }
   ```

4. **Excel Generation** (`generate_per_war_tables_excel()`)
   ```python
   # For each member, extract individual attacks
   member_attacks = None
   for m in clan_members:
       if m.get('name') == name:
           member_attacks = m.get('attacks', [])
           break
   
   if member_attacks:
       if len(member_attacks) >= 1:
           attack1_stars = member_attacks[0].get('stars', 0)
           attack1_percent = member_attacks[0].get('destructionPercentage', 0)
       if len(member_attacks) >= 2:
           attack2_stars = member_attacks[1].get('stars', 0)
           attack2_percent = member_attacks[1].get('destructionPercentage', 0)
   ```

---

## ✅ Verification

### Check War Data Has Attacks
```python
import json

with open("war_data/war_2P0GPYYJY_20260119_154611.json", 'r') as f:
    data = json.load(f)

# Verify members array exists
assert 'members' in data['clan']

# Find a member with attacks
for member in data['clan']['members']:
    attacks = member.get('attacks', [])
    if len(attacks) > 0:
        print(f"{member['name']} has {len(attacks)} attacks")
        print(f"  Attack 1: {attacks[0]['stars']}⭐ {attacks[0]['destructionPercentage']}%")
        if len(attacks) > 1:
            print(f"  Attack 2: {attacks[1]['stars']}⭐ {attacks[1]['destructionPercentage']}%")
        break
```

### Check Excel Has Individual Data
```python
from openpyxl import load_workbook

wb = load_workbook("per_war_member_performance.xlsx")
ws = wb.active

# Check a row with data
row = 4  # First data row
name = ws.cell(row=row, column=1).value
atk1_stars = ws.cell(row=row, column=5).value
atk1_pct = ws.cell(row=row, column=6).value

print(f"{name}: Attack 1 = {atk1_stars}⭐ {atk1_pct}%")
```

---

## 📈 Use Cases

### 1. **Performance Analysis**
Compare Attack 1 vs Attack 2 to see if players improve their strategy

### 2. **Strategy Review**
- Which players consistently 3-star on first attack?
- Who needs practice with their second attack?
- Are partial attackers using their one attack well?

### 3. **Coaching Opportunities**
- Identify members with low first-attack success
- Track improvement over multiple wars
- Share best practices from top performers

### 4. **War Planning**
- Know which members can be relied on for cleanup attacks
- Identify who should attack early vs late in war

---

## 🎯 Real Example

**War vs Gorkhali (2026-01-19)**

```
stor våkter:
  Attack 1: 2⭐ 93% (strong first attempt)
  Attack 2: 2⭐ 61% (struggled on cleanup)
  → Suggestion: Focus on consistency

gooner:
  Attack 1: 3⭐ 100% (perfect execution)
  Attack 2: 3⭐ 100% (perfect execution)
  → Top performer!

Marcus:
  Attack 1: 3⭐ 100% (used 1/2 attacks)
  Attack 2: — (didn't use second attack)
  → Reminder needed
```

---

## 🔧 Troubleshooting

### Empty Attack Columns

**Problem**: Attack 1/2 columns show blank

**Causes**:
1. War data saved before update (missing `members` array)
2. War in preparation phase (no attacks yet)
3. Player hasn't attacked yet

**Solution**:
```bash
# Re-track the current war to update data
cd war_tracking
python3 -c "from war_info import log_current_war_attacks, save_war_data_unique, CLAN_TAG; save_war_data_unique(log_current_war_attacks(CLAN_TAG))"

# Regenerate Excel tables
python3 generate_excel_tables.py
```

### Verify Members Data Saved

```bash
python3 << 'EOF'
import json
with open("war_data/war_2P0GPYYJY_20260119_154611.json", 'r') as f:
    data = json.load(f)

if 'members' in data['clan']:
    print("✅ Members data found")
    print(f"   Total members: {len(data['clan']['members'])}")
else:
    print("❌ Members data missing - need to re-track war")
EOF
```

---

## 📚 Related Files

- **war_info.py**: Line 936 - `war_log_data["clan"]["members"] = members`
- **generate_excel_tables.py**: Lines 116-149 - Individual attack extraction
- **war_data/*.json**: Stored war data with full member attacks

---

## 🎉 Benefits

✅ **Complete Attack History**: Every attack is recorded  
✅ **Performance Trends**: Track improvement over time  
✅ **Strategic Insights**: Understand attack patterns  
✅ **Professional Reports**: Beautiful Excel tables  
✅ **Data-Driven Decisions**: Make informed war plans  

---

**Last Updated**: January 20, 2026  
**Status**: ✅ Fully Operational  
**Data Source**: Clash of Clans Official API  
**Storage**: JSON + Excel (.xlsx)
