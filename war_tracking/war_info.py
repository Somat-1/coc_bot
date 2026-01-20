#!/usr/bin/env python3
"""
Clash of Clans War Information Fetcher

This script fetches current and previous war information for a clan using the Clash of Clans API.
You'll need an API key from https://developer.clashofclans.com/
"""

import requests
import json
import os
import csv
from datetime import datetime
from typing import Dict, Optional, List

# ========= CONFIGURATION =========
# Get API key from environment variable or set it here (NOT RECOMMENDED to hardcode)
API_KEY = os.getenv("COC_API_KEY", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImM0YTkwNGMzLWYwNDQtNDU2Ni1hMGI1LTNiNzM2YTlkZjdhNiIsImlhdCI6MTc2ODgxODUxNywic3ViIjoiZGV2ZWxvcGVyLzIyNDcyMzQ1LWQ2OWEtYTg1OC1lOGM1LWY1MGMzODAzZTIxYSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjgzLjg1LjE1Ny4xOSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.YVJs55qHPQGGvsjoTNrgdxaHz-jrvIP4gcrOUKyGiNqsWDfTfN66xUGbkI9NNawNTHItEp1m3ThVIj755ZxV9Q")  # Set your API key here or use environment variable

# API Base URL
API_BASE_URL = "https://api.clashofclans.com/v1"

# Example clan tag (replace with your clan tag, must start with #)
CLAN_TAG = "#2P0GPYYJY"  # LøpeforbundetFC

# War data storage directory
WAR_DATA_DIR = "war_data"

# Message character limit for CoC/Discord
MESSAGE_CHAR_LIMIT = 240

# ========= HELPER FUNCTIONS =========
def get_headers() -> Dict[str, str]:
    """Returns headers with API key for authentication."""
    if not API_KEY:
        raise ValueError("API_KEY is not set! Set COC_API_KEY environment variable or update the script.")
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }

def format_clan_tag(tag: str) -> str:
    """Formats clan tag for API URL (removes # and encodes)."""
    # Remove # if present
    if tag.startswith("#"):
        tag = tag[1:]
    # URL encode the tag (replace # with %23 if it somehow remained)
    return tag.replace("#", "%23")

def format_timestamp(timestamp: str) -> str:
    """Converts API timestamp to readable format."""
    try:
        # API timestamp format: 20240115T123045.000Z
        dt = datetime.strptime(timestamp, "%Y%m%dT%H%M%S.%fZ")
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except:
        return timestamp

def format_war_state(state: str) -> str:
    """Formats war state for display."""
    states = {
        "notInWar": "❌ Not in War",
        "preparation": "⏳ Preparation",
        "inWar": "⚔️  In War",
        "warEnded": "✅ War Ended"
    }
    return states.get(state, state)

# ========= API FUNCTIONS =========
def get_current_war(clan_tag: str) -> Optional[Dict]:
    """
    Fetches current war information for a clan.
    
    Args:
        clan_tag: Clan tag (with or without #)
        
    Returns:
        Dict with war information or None if error
    """
    formatted_tag = format_clan_tag(clan_tag)
    url = f"{API_BASE_URL}/clans/%23{formatted_tag}/currentwar"
    
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching current war: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        return None

def get_war_log(clan_tag: str, limit: int = 10) -> Optional[Dict]:
    """
    Fetches war log (previous wars) for a clan.
    
    Args:
        clan_tag: Clan tag (with or without #)
        limit: Number of wars to fetch (API returns up to the limit available)
        
    Returns:
        Dict with war log or None if error
    """
    formatted_tag = format_clan_tag(clan_tag)
    url = f"{API_BASE_URL}/clans/%23{formatted_tag}/warlog"
    
    params = {"limit": limit}
    
    try:
        response = requests.get(url, headers=get_headers(), params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching war log: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        return None

def get_clan_info(clan_tag: str) -> Optional[Dict]:
    """
    Fetches basic clan information.
    
    Args:
        clan_tag: Clan tag (with or without #)
        
    Returns:
        Dict with clan info or None if error
    """
    formatted_tag = format_clan_tag(clan_tag)
    url = f"{API_BASE_URL}/clans/%23{formatted_tag}"
    
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching clan info: {e}")
        return None

# ========= DISPLAY FUNCTIONS =========
def analyze_member_performance(member: Dict) -> Dict:
    """
    Analyzes a member's performance in a war.
    
    Returns:
        Dict with performance stats
    """
    attacks = member.get("attacks", [])
    num_attacks = len(attacks)
    
    if num_attacks == 0:
        return {
            "name": member.get("name", "Unknown"),
            "tag": member.get("tag", "Unknown"),
            "attacked": False,
            "attacks_used": 0,
            "total_stars": 0,
            "avg_stars": 0.0,
            "total_destruction": 0.0,
            "avg_destruction": 0.0,
            "best_attack_stars": 0,
            "best_attack_destruction": 0.0
        }
    
    total_stars = sum(attack.get("stars", 0) for attack in attacks)
    total_destruction = sum(attack.get("destructionPercentage", 0) for attack in attacks)
    best_attack = max(attacks, key=lambda a: (a.get("stars", 0), a.get("destructionPercentage", 0)))
    
    return {
        "name": member.get("name", "Unknown"),
        "tag": member.get("tag", "Unknown"),
        "attacked": True,
        "attacks_used": num_attacks,
        "total_stars": total_stars,
        "avg_stars": total_stars / num_attacks,
        "total_destruction": total_destruction,
        "avg_destruction": total_destruction / num_attacks,
        "best_attack_stars": best_attack.get("stars", 0),
        "best_attack_destruction": best_attack.get("destructionPercentage", 0)
    }

def display_current_war(war_data: Dict) -> None:
    """Displays current war information in a formatted way."""
    print("\n" + "="*80)
    print("🏆 CURRENT WAR INFORMATION")
    print("="*80)
    
    state = war_data.get("state", "unknown")
    
    if state == "notInWar":
        print("\n❌ Clan is not currently in war.")
        return
    
    # Basic war info
    print(f"\n📊 War State: {format_war_state(state)}")
    print(f"🗓️  War Size: {war_data.get('teamSize', 'Unknown')}v{war_data.get('teamSize', 'Unknown')}")
    
    # Timing information
    if "startTime" in war_data:
        print(f"🕐 Start Time: {format_timestamp(war_data['startTime'])}")
    if "endTime" in war_data:
        print(f"🕐 End Time: {format_timestamp(war_data['endTime'])}")
    
    # Clan information
    clan = war_data.get("clan", {})
    opponent = war_data.get("opponent", {})
    
    print(f"\n⚔️  {clan.get('name', 'Unknown')} vs {opponent.get('name', 'Unknown')}")
    print(f"   Tag: {clan.get('tag', 'Unknown')} vs {opponent.get('tag', 'Unknown')}")
    
    # Scores
    print(f"\n🎯 Stars: {clan.get('stars', 0)} ⭐ vs {opponent.get('stars', 0)} ⭐")
    print(f"💥 Destruction: {clan.get('destructionPercentage', 0):.2f}% vs {opponent.get('destructionPercentage', 0):.2f}%")
    print(f"⚔️  Attacks: {clan.get('attacks', 0)} vs {opponent.get('attacks', 0)}")
    
    # Member stats
    print(f"\n👥 Members:")
    print(f"   Your Clan: {len(clan.get('members', []))} members")
    print(f"   Opponent: {len(opponent.get('members', []))} members")
    
    # Display member performance if war has started
    if state in ["inWar", "warEnded"]:
        display_current_war_member_analysis(war_data)

def display_current_war_member_analysis(war_data: Dict) -> None:
    """Displays detailed member analysis for the current war."""
    clan = war_data.get("clan", {})
    members = clan.get("members", [])
    
    if not members:
        return
    
    print(f"\n{'='*80}")
    print("🔍 CURRENT WAR MEMBER ANALYSIS")
    print("="*80)
    
    attackers = []
    non_attackers = []
    
    for member in members:
        perf = analyze_member_performance(member)
        if perf["attacked"]:
            attackers.append(perf)
        else:
            non_attackers.append(perf)
    
    # Display attackers
    if attackers:
        print(f"\n✅ ATTACKED ({len(attackers)}/{len(members)} members):")
        attackers.sort(key=lambda x: (x["total_stars"], x["total_destruction"]), reverse=True)
        for perf in attackers:
            print(f"   • {perf['name']}: {perf['attacks_used']} attacks | "
                  f"Avg: {perf['avg_stars']:.1f}⭐ {perf['avg_destruction']:.1f}% | "
                  f"Best: {perf['best_attack_stars']}⭐ {perf['best_attack_destruction']:.1f}%")
    
    # Display non-attackers
    if non_attackers:
        print(f"\n❌ NOT YET ATTACKED ({len(non_attackers)}/{len(members)} members):")
        for perf in non_attackers:
            print(f"   • {perf['name']}")

def display_war_log(war_log: Dict, count: int = 3) -> None:
    """Displays war log (previous wars) in a formatted way."""
    print("\n" + "="*80)
    print(f"📜 WAR LOG (Last {count} Wars)")
    print("="*80)
    
    items = war_log.get("items", [])
    
    if not items:
        print("\n❌ No war history available or war log is private.")
        return
    
    # Display only the requested number of wars
    for idx, war in enumerate(items[:count], 1):
        result = war.get("result", "unknown")
        
        # Determine result emoji
        result_emoji = {
            "win": "🏆",
            "lose": "❌",
            "tie": "🤝"
        }.get(result, "❓")
        
        print(f"\n{idx}. War on {format_timestamp(war.get('endTime', 'Unknown'))}")
        result_text = result.upper() if result else "UNKNOWN"
        print(f"   Result: {result_emoji} {result_text}")
        print(f"   Size: {war.get('teamSize', '?')}v{war.get('teamSize', '?')}")
        
        # Opponent info
        opponent = war.get("opponent", {})
        print(f"   Opponent: {opponent.get('name', 'Unknown')} ({opponent.get('tag', 'Unknown')})")
        
        # Scores
        clan = war.get("clan", {})
        print(f"   Stars: {clan.get('stars', 0)} ⭐ vs {opponent.get('stars', 0)} ⭐")
        print(f"   Destruction: {clan.get('destructionPercentage', 0):.2f}% vs {opponent.get('destructionPercentage', 0):.2f}%")
        print(f"   Attacks: {clan.get('attacks', 0)} vs {opponent.get('attacks', 0)}")

def display_detailed_war_analysis(war_log: Dict, count: int = 3) -> None:
    """Displays war history summary."""
    print("\n" + "="*80)
    print(f"📜 WAR HISTORY SUMMARY")
    print("="*80)
    
    print("\nℹ️  Note: War log only shows final scores. For detailed member tracking,")
    print("   check the CURRENT WAR section above (when war is active).")
    
    items = war_log.get("items", [])
    
    if not items:
        print("\n❌ No war history available or war log is private.")
        return
    
    print(f"\n📊 Last {count} Wars:")
    print("="*80)
    
    for idx, war in enumerate(items[:count], 1):
        result = war.get("result", "unknown")
        result_emoji = {
            "win": "🏆",
            "lose": "❌",
            "tie": "🤝"
        }.get(result, "❓")
        
        clan = war.get("clan", {})
        opponent = war.get("opponent", {})
        
        print(f"\n{idx}. {format_timestamp(war.get('endTime', 'Unknown'))}")
        print(f"   Result: {result_emoji} {result.upper() if result else 'UNKNOWN'}")
        print(f"   Size: {war.get('teamSize', '?')}v{war.get('teamSize', '?')}")
        print(f"   Opponent: {opponent.get('name', 'Unknown')}")
        print(f"   Score: {clan.get('stars', 0)}⭐ ({clan.get('destructionPercentage', 0):.1f}%) vs "
              f"{opponent.get('stars', 0)}⭐ ({opponent.get('destructionPercentage', 0):.1f}%)")

# ========= TABLE GENERATION FUNCTIONS =========

def generate_war_summary_table(output_file: str = "war_summary.csv") -> None:
    """
    Generate a CSV table summarizing all wars from the war_data directory.
    
    Columns:
    - War Date
    - Opponent Clan
    - War State (Ended/In Progress/Preparation)
    - Result (Win/Loss/Tie/TBD)
    - Our Stars
    - Opponent Stars
    - Our Destruction %
    - Opponent Destruction %
    - Team Size
    - Attacks Used
    - Total Possible Attacks
    - Participation Rate %
    """
    if not os.path.exists(WAR_DATA_DIR):
        print(f"\n❌ No war data directory found ({WAR_DATA_DIR})")
        return
    
    war_files = sorted([f for f in os.listdir(WAR_DATA_DIR) if f.endswith('.json')])
    
    if not war_files:
        print(f"\n❌ No war data files found in {WAR_DATA_DIR}")
        return
    
    print(f"\n📊 Generating war summary table from {len(war_files)} wars...")
    
    rows = []
    
    for filename in war_files:
        filepath = os.path.join(WAR_DATA_DIR, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract war date from start time
            war_start = data.get('war_start', '')
            try:
                war_date = datetime.fromisoformat(war_start.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
            except:
                war_date = war_start
            
            war_state = data.get('war_state', 'Unknown')
            team_size = data.get('team_size', 0)
            attacks_per_member = data.get('attacks_per_member', 2)
            total_possible_attacks = team_size * attacks_per_member
            
            # Clan and opponent data
            clan = data.get('clan', {})
            opponent = data.get('opponent', {})
            
            opponent_name = opponent.get('name', 'Unknown')
            clan_stars = clan.get('stars', 0)
            opponent_stars = opponent.get('stars', 0)
            clan_destruction = clan.get('destruction', 0.0)
            opponent_destruction = opponent.get('destruction', 0.0)
            attacks_used = clan.get('attacks', 0)
            
            # Determine result
            if war_state == 'preparation':
                result = 'TBD (Prep)'
            elif war_state == 'inWar':
                result = 'TBD (In Progress)'
            else:  # warEnded
                if clan_stars > opponent_stars:
                    result = 'Win'
                elif clan_stars < opponent_stars:
                    result = 'Loss'
                else:
                    # Same stars, check destruction
                    if clan_destruction > opponent_destruction:
                        result = 'Win'
                    elif clan_destruction < opponent_destruction:
                        result = 'Loss'
                    else:
                        result = 'Tie'
            
            # Calculate participation rate
            participation_rate = (attacks_used / total_possible_attacks * 100) if total_possible_attacks > 0 else 0
            
            row = {
                'War Date': war_date,
                'Opponent Clan': opponent_name,
                'War State': war_state,
                'Result': result,
                'Our Stars': clan_stars,
                'Opponent Stars': opponent_stars,
                'Our Destruction %': f"{clan_destruction:.2f}",
                'Opponent Destruction %': f"{opponent_destruction:.2f}",
                'Team Size': team_size,
                'Attacks Used': attacks_used,
                'Total Possible Attacks': total_possible_attacks,
                'Participation Rate %': f"{participation_rate:.2f}"
            }
            
            rows.append(row)
            
        except Exception as e:
            print(f"⚠️ Error processing {filename}: {e}")
            continue
    
    # Write to CSV
    if rows:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'War Date', 'Opponent Clan', 'War State', 'Result', 'Our Stars', 'Opponent Stars',
                'Our Destruction %', 'Opponent Destruction %', 'Team Size',
                'Attacks Used', 'Total Possible Attacks', 'Participation Rate %'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✅ War summary table saved to: {output_file}")
        print(f"   Total wars: {len(rows)}")
    else:
        print("❌ No valid war data to export")


def generate_per_war_member_table(output_file: str = "per_war_member_performance.csv") -> None:
    """
    Generate a CSV table showing member performance for each war.
    Each war adds new columns with opponent name.
    Tracks both attacks separately with stars and destruction %.
    
    Columns per war:
    - War vs Opponent - Attack 1 Stars
    - War vs Opponent - Attack 1 Destruction %
    - War vs Opponent - Attack 2 Stars
    - War vs Opponent - Attack 2 Destruction %
    - War vs Opponent - Total Stars
    - War vs Opponent - Participated
    """
    if not os.path.exists(WAR_DATA_DIR):
        print(f"\n❌ No war data directory found ({WAR_DATA_DIR})")
        return
    
    war_files = sorted([f for f in os.listdir(WAR_DATA_DIR) if f.endswith('.json')])
    
    if not war_files:
        print(f"\n❌ No war data files found in {WAR_DATA_DIR}")
        return
    
    print(f"\n📊 Generating per-war member performance table from {len(war_files)} wars...")
    
    # Collect all unique members and war data
    all_members = set()
    wars_data = []  # List of {date, opponent, members_data}
    
    for filename in war_files:
        filepath = os.path.join(WAR_DATA_DIR, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract war info
            war_start = data.get('war_start', '')
            try:
                war_date = datetime.fromisoformat(war_start.replace('Z', '+00:00')).strftime('%Y-%m-%d')
            except:
                war_date = war_start[:10] if war_start else 'Unknown'
            
            opponent_name = data.get('opponent', {}).get('name', 'Unknown')
            war_label = f"{war_date} vs {opponent_name}"
            
            # Get member data from all three categories
            member_analysis = data.get('member_analysis', {})
            attackers = member_analysis.get('attackers', [])
            partial = member_analysis.get('partial', [])
            missed = member_analysis.get('missed', [])
            
            # Build member performance dict for this war
            members_performance = {}
            
            # Process attackers (used all attacks)
            for member in attackers:
                name = member['name']
                all_members.add(name)
                
                # Get individual attack data from raw war data
                clan_members = data.get('clan', {}).get('members', [])
                member_attacks = None
                for m in clan_members:
                    if m.get('name') == name:
                        member_attacks = m.get('attacks', [])
                        break
                
                attack1_stars = ''
                attack1_dest = ''
                attack2_stars = ''
                attack2_dest = ''
                
                if member_attacks:
                    if len(member_attacks) >= 1:
                        attack1_stars = member_attacks[0].get('stars', 0)
                        attack1_dest = f"{member_attacks[0].get('destructionPercentage', 0):.1f}"
                    if len(member_attacks) >= 2:
                        attack2_stars = member_attacks[1].get('stars', 0)
                        attack2_dest = f"{member_attacks[1].get('destructionPercentage', 0):.1f}"
                
                members_performance[name] = {
                    'attack1_stars': attack1_stars,
                    'attack1_dest': attack1_dest,
                    'attack2_stars': attack2_stars,
                    'attack2_dest': attack2_dest,
                    'total_stars': member['total_stars'],
                    'participated': 'Yes (All)'
                }
            
            # Process partial attackers
            for member in partial:
                name = member['name']
                all_members.add(name)
                
                # Get individual attack data
                clan_members = data.get('clan', {}).get('members', [])
                member_attacks = None
                for m in clan_members:
                    if m.get('name') == name:
                        member_attacks = m.get('attacks', [])
                        break
                
                attack1_stars = ''
                attack1_dest = ''
                attack2_stars = ''
                attack2_dest = ''
                
                if member_attacks:
                    if len(member_attacks) >= 1:
                        attack1_stars = member_attacks[0].get('stars', 0)
                        attack1_dest = f"{member_attacks[0].get('destructionPercentage', 0):.1f}"
                    if len(member_attacks) >= 2:
                        attack2_stars = member_attacks[1].get('stars', 0)
                        attack2_dest = f"{member_attacks[1].get('destructionPercentage', 0):.1f}"
                
                members_performance[name] = {
                    'attack1_stars': attack1_stars,
                    'attack1_dest': attack1_dest,
                    'attack2_stars': attack2_stars,
                    'attack2_dest': attack2_dest,
                    'total_stars': member['total_stars'],
                    'participated': f"Partial ({member['attacks_used']}/2)"
                }
            
            # Process members who didn't attack
            for member in missed:
                name = member['name']
                all_members.add(name)
                members_performance[name] = {
                    'attack1_stars': '',
                    'attack1_dest': '',
                    'attack2_stars': '',
                    'attack2_dest': '',
                    'total_stars': 0,
                    'participated': 'No'
                }
            
            wars_data.append({
                'label': war_label,
                'members': members_performance
            })
            
        except Exception as e:
            print(f"⚠️ Error processing {filename}: {e}")
            continue
    
    # Write to CSV
    if wars_data and all_members:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            # Build header
            header = ['Member Name']
            for war in wars_data:
                war_label = war['label']
                header.extend([
                    f"{war_label} - Attack 1 Stars",
                    f"{war_label} - Attack 1 Dest %",
                    f"{war_label} - Attack 2 Stars",
                    f"{war_label} - Attack 2 Dest %",
                    f"{war_label} - Total Stars",
                    f"{war_label} - Participated"
                ])
            
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            
            # Write data for each member
            for member_name in sorted(all_members):
                row = {'Member Name': member_name}
                
                for war in wars_data:
                    war_label = war['label']
                    member_data = war['members'].get(member_name, {})
                    
                    row[f"{war_label} - Attack 1 Stars"] = member_data.get('attack1_stars', '')
                    row[f"{war_label} - Attack 1 Dest %"] = member_data.get('attack1_dest', '')
                    row[f"{war_label} - Attack 2 Stars"] = member_data.get('attack2_stars', '')
                    row[f"{war_label} - Attack 2 Dest %"] = member_data.get('attack2_dest', '')
                    row[f"{war_label} - Total Stars"] = member_data.get('total_stars', '')
                    row[f"{war_label} - Participated"] = member_data.get('participated', 'Not in war')
                
                writer.writerow(row)
        
        print(f"✅ Per-war member performance table saved to: {output_file}")
        print(f"   Total members: {len(all_members)}")
        print(f"   Total wars: {len(wars_data)}")
    else:
        print("❌ No valid member data to export")


def generate_overall_member_performance_table(output_file: str = "overall_member_performance.csv") -> None:
    """
    Generate a CSV table showing aggregate member performance across all wars.
    
    Columns:
    - Member Name
    - Member Tag
    - Total Wars Participated
    - Wars Attacked (All)
    - Wars Attacked (Partial)
    - Wars Missed (No Attacks)
    - Full Participation Rate %
    - Total Attacks Made
    - Total Stars Earned
    - Avg Stars per Attack
    - Avg Destruction per Attack %
    """
    if not os.path.exists(WAR_DATA_DIR):
        print(f"\n❌ No war data directory found ({WAR_DATA_DIR})")
        return
    
    war_files = sorted([f for f in os.listdir(WAR_DATA_DIR) if f.endswith('.json')])
    
    if not war_files:
        print(f"\n❌ No war data files found in {WAR_DATA_DIR}")
        return
    
    print(f"\n📊 Generating overall member performance table from {len(war_files)} wars...")
    
    # Dictionary to aggregate member stats: {member_tag: {...}}
    member_stats = {}
    
    for filename in war_files:
        filepath = os.path.join(WAR_DATA_DIR, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            member_analysis = data.get('member_analysis', {})
            
            # Process all three categories
            attackers = member_analysis.get('attackers', [])
            partial = member_analysis.get('partial', [])
            missed = member_analysis.get('missed', [])
            
            # Process attackers (used all attacks)
            for member in attackers:
                tag = member['tag']
                if tag not in member_stats:
                    member_stats[tag] = {
                        'name': member['name'],
                        'wars_participated': 0,
                        'wars_full_attack': 0,
                        'wars_partial_attack': 0,
                        'wars_no_attack': 0,
                        'total_attacks': 0,
                        'total_stars': 0,
                        'total_destruction': 0.0
                    }
                
                member_stats[tag]['wars_participated'] += 1
                member_stats[tag]['wars_full_attack'] += 1
                member_stats[tag]['total_attacks'] += member['attacks_used']
                member_stats[tag]['total_stars'] += member['total_stars']
                member_stats[tag]['total_destruction'] += member['avg_destruction_percent'] * member['attacks_used']
            
            # Process partial attackers
            for member in partial:
                tag = member['tag']
                if tag not in member_stats:
                    member_stats[tag] = {
                        'name': member['name'],
                        'wars_participated': 0,
                        'wars_full_attack': 0,
                        'wars_partial_attack': 0,
                        'wars_no_attack': 0,
                        'total_attacks': 0,
                        'total_stars': 0,
                        'total_destruction': 0.0
                    }
                
                member_stats[tag]['wars_participated'] += 1
                member_stats[tag]['wars_partial_attack'] += 1
                member_stats[tag]['total_attacks'] += member['attacks_used']
                member_stats[tag]['total_stars'] += member['total_stars']
                member_stats[tag]['total_destruction'] += member['avg_destruction_percent'] * member['attacks_used']
            
            # Process members who didn't attack
            for member in missed:
                tag = member['tag']
                if tag not in member_stats:
                    member_stats[tag] = {
                        'name': member['name'],
                        'wars_participated': 0,
                        'wars_full_attack': 0,
                        'wars_partial_attack': 0,
                        'wars_no_attack': 0,
                        'total_attacks': 0,
                        'total_stars': 0,
                        'total_destruction': 0.0
                    }
                
                member_stats[tag]['wars_participated'] += 1
                member_stats[tag]['wars_no_attack'] += 1
            
        except Exception as e:
            print(f"⚠️ Error processing {filename}: {e}")
            continue
    
    # Convert to rows and calculate averages
    rows = []
    for tag, stats in member_stats.items():
        wars_participated = stats['wars_participated']
        wars_full_attack = stats['wars_full_attack']
        total_attacks = stats['total_attacks']
        total_stars = stats['total_stars']
        total_destruction = stats['total_destruction']
        
        # Calculate participation rate (full attacks only)
        full_participation_rate = (wars_full_attack / wars_participated * 100) if wars_participated > 0 else 0
        
        # Calculate averages
        avg_stars_per_attack = (total_stars / total_attacks) if total_attacks > 0 else 0
        avg_destruction_per_attack = (total_destruction / total_attacks) if total_attacks > 0 else 0
        
        row = {
            'Member Name': stats['name'],
            'Member Tag': tag,
            'Total Wars Participated': wars_participated,
            'Wars Attacked (All)': wars_full_attack,
            'Wars Attacked (Partial)': stats['wars_partial_attack'],
            'Wars Missed (No Attacks)': stats['wars_no_attack'],
            'Full Participation Rate %': f"{full_participation_rate:.2f}",
            'Total Attacks Made': total_attacks,
            'Total Stars Earned': total_stars,
            'Avg Stars per Attack': f"{avg_stars_per_attack:.2f}",
            'Avg Destruction per Attack %': f"{avg_destruction_per_attack:.2f}"
        }
        rows.append(row)
    
    # Sort by total wars participated (descending), then by name
    rows.sort(key=lambda x: (-x['Total Wars Participated'], x['Member Name']))
    
    # Write to CSV
    if rows:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'Member Name', 'Member Tag', 'Total Wars Participated',
                'Wars Attacked (All)', 'Wars Attacked (Partial)', 'Wars Missed (No Attacks)',
                'Full Participation Rate %', 'Total Attacks Made', 'Total Stars Earned',
                'Avg Stars per Attack', 'Avg Destruction per Attack %'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✅ Overall member performance table saved to: {output_file}")
        print(f"   Total members: {len(rows)}")
    else:
        print("❌ No valid member data to export")


def generate_all_tables() -> None:
    """
    Generate all three CSV tables:
    1. War summary
    2. Per-war member performance
    3. Overall member performance
    """
    print("\n" + "=" * 80)
    print("📊 GENERATING ALL WAR ANALYSIS TABLES")
    print("=" * 80)
    
    generate_war_summary_table()
    generate_per_war_member_table()
    generate_overall_member_performance_table()
    
    print("\n✅ All tables generated successfully!")
    print("\nGenerated files:")
    print("  1. war_summary.csv")
    print("  2. per_war_member_performance.csv")
    print("  3. overall_member_performance.csv")

def log_current_war_attacks(clan_tag: str) -> Optional[Dict]:
    """
    Fetches current war and logs member attack performance.
    
    Returns:
        Dict with war log data including member analysis, or None if no war
    """
    war_data = get_current_war(clan_tag)
    
    if not war_data:
        print("❌ Could not fetch current war data")
        return None
    
    state = war_data.get("state", "unknown")
    
    if state == "notInWar":
        print("\n❌ Clan is not currently in war. No attacks to log.")
        return None
    
    # Display basic war info first
    display_current_war(war_data)
    
    # Only analyze attacks if war has started
    if state not in ["inWar", "warEnded"]:
        print(f"\n⚠️ War is in {format_war_state(state)} phase. No attacks yet to log.")
        return None
    
    # Get war details
    clan = war_data.get("clan", {})
    opponent = war_data.get("opponent", {})
    members = clan.get("members", [])
    team_size = war_data.get("teamSize", len(members))
    attacks_per_member = war_data.get("attacksPerMember", 2)
    
    # Categorize members
    used_all_attacks = []
    partial_attacks = []
    no_attacks = []
    
    for member in members:
        attacks = member.get("attacks", [])
        num_attacks = len(attacks)
        
        if num_attacks == 0:
            no_attacks.append({
                "name": member.get("name", "Unknown"),
                "tag": member.get("tag", "Unknown")
            })
        elif num_attacks < attacks_per_member:
            perf = analyze_member_performance(member)
            partial_attacks.append({
                "name": perf["name"],
                "tag": perf["tag"],
                "attacks_used": perf["attacks_used"],
                "total_stars": perf["total_stars"],
                "avg_stars_per_attack": perf["avg_stars"],
                "avg_destruction_percent": perf["avg_destruction"],
                "best_attack": {
                    "stars": perf["best_attack_stars"],
                    "destruction_percent": perf["best_attack_destruction"]
                }
            })
        else:
            perf = analyze_member_performance(member)
            used_all_attacks.append({
                "name": perf["name"],
                "tag": perf["tag"],
                "attacks_used": perf["attacks_used"],
                "total_stars": perf["total_stars"],
                "avg_stars_per_attack": perf["avg_stars"],
                "avg_destruction_percent": perf["avg_destruction"],
                "best_attack": {
                    "stars": perf["best_attack_stars"],
                    "destruction_percent": perf["best_attack_destruction"]
                }
            })
    
    # Display participation summary
    print(f"\n{'='*80}")
    print("📊 PARTICIPATION SUMMARY")
    print("="*80)
    print(f"✅ Used all attacks ({attacks_per_member}/{attacks_per_member}): {len(used_all_attacks)} members")
    print(f"⚠️  Partial attacks: {len(partial_attacks)} members")
    print(f"❌ No attacks: {len(no_attacks)} members")
    
    # Generate and display copy-paste messages
    messages = generate_missed_attack_messages(no_attacks, partial_attacks)
    if messages:
        print(f"\n{'='*80}")
        print("📋 COPY-PASTE MESSAGES FOR DISCORD/CLASH")
        print("="*80)
        for i, msg in enumerate(messages, 1):
            print(f"\nMessage {i} ({len(msg)} chars):")
            print(msg)
    
    # Create war log data structure
    war_log_data = {
        "timestamp": datetime.now().isoformat(),
        "war_state": state,
        "war_start": war_data.get("startTime", ""),
        "war_end": war_data.get("endTime", ""),
        "team_size": team_size,
        "attacks_per_member": attacks_per_member,
        "clan": {
            "name": clan.get("name", "Unknown"),
            "tag": clan.get("tag", "Unknown"),
            "stars": clan.get("stars", 0),
            "destruction": clan.get("destructionPercentage", 0.0),
            "attacks": clan.get("attacks", 0),
            "members": members  # ⭐ ADD RAW MEMBERS DATA WITH INDIVIDUAL ATTACKS
        },
        "opponent": {
            "name": opponent.get("name", "Unknown"),
            "tag": opponent.get("tag", "Unknown"),
            "stars": opponent.get("stars", 0),
            "destruction": opponent.get("destructionPercentage", 0.0),
            "attacks": opponent.get("attacks", 0),
            "members": opponent.get("members", [])  # ⭐ ADD OPPONENT MEMBERS TOO
        },
        "member_analysis": {
            "total_members": len(members),
            "used_all_attacks": len(used_all_attacks),
            "partial_attacks": len(partial_attacks),
            "no_attacks": len(no_attacks),
            "attackers": used_all_attacks,
            "partial": partial_attacks,
            "missed": no_attacks
        }
    }
    
    return war_log_data


def generate_missed_attack_messages(missed_attacks: List[Dict], partial_attacks: List[Dict]) -> List[str]:
    """
    Generates copy-paste messages for members who missed attacks.
    Max 5 names per message, under MESSAGE_CHAR_LIMIT characters.
    
    Args:
        missed_attacks: List of members with no attacks
        partial_attacks: List of members with partial attacks
    
    Returns:
        List of formatted messages ready to copy-paste
    """
    messages = []
    MAX_NAMES_PER_MESSAGE = 5
    
    # Generate messages for members with NO attacks
    if missed_attacks:
        # Split into chunks of max 5 names
        for i in range(0, len(missed_attacks), MAX_NAMES_PER_MESSAGE):
            chunk = missed_attacks[i:i + MAX_NAMES_PER_MESSAGE]
            mentions = ', '.join([f"@{member['name']}" for member in chunk])
            message = f"❌ NO ATTACKS: {mentions}"
            
            # Ensure message is under limit
            if len(message) <= MESSAGE_CHAR_LIMIT:
                messages.append(message)
            else:
                # If still too long, split into individual messages
                for member in chunk:
                    msg = f"❌ NO ATTACKS: @{member['name']}"
                    messages.append(msg)
    
    # Generate messages for members with PARTIAL attacks
    if partial_attacks:
        # Split into chunks of max 5 names
        for i in range(0, len(partial_attacks), MAX_NAMES_PER_MESSAGE):
            chunk = partial_attacks[i:i + MAX_NAMES_PER_MESSAGE]
            mentions = ', '.join([f"@{member['name']}" for member in chunk])
            message = f"⚠️ PARTIAL ATTACKS: {mentions}"
            
            # Ensure message is under limit
            if len(message) <= MESSAGE_CHAR_LIMIT:
                messages.append(message)
            else:
                # If still too long, split into individual messages
                for member in chunk:
                    msg = f"⚠️ PARTIAL ATTACKS: @{member['name']}"
                    messages.append(msg)
    
    return messages


def save_war_data_unique(war_log_data: Dict) -> str:
    """
    Saves war data to a unique JSON file based on war start time.
    Updates the file if the same war is polled multiple times.
    
    Args:
        war_log_data: War log data dictionary
    
    Returns:
        Filename where data was saved
    """
    # Create directory if it doesn't exist
    if not os.path.exists(WAR_DATA_DIR):
        os.makedirs(WAR_DATA_DIR)
        print(f"✅ Created directory: {WAR_DATA_DIR}")
    
    # Extract war start time to create unique filename
    war_start = war_log_data.get("war_start", "")
    
    # Parse timestamp to create filename
    try:
        # Format: 20260119T154611.000Z -> war_2P0GPYYJY_20260119_154611.json
        dt = datetime.strptime(war_start, "%Y%m%dT%H%M%S.%fZ")
        date_str = dt.strftime("%Y%m%d_%H%M%S")
        clan_tag = war_log_data.get("clan", {}).get("tag", "").replace("#", "")
        filename = f"war_{clan_tag}_{date_str}.json"
    except:
        # Fallback to timestamp-based filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"war_data_{timestamp}.json"
    
    filepath = os.path.join(WAR_DATA_DIR, filename)
    
    # Save to file (will overwrite if same war is polled again)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(war_log_data, f, indent=2, ensure_ascii=False)
    
    return filename


def display_clan_war_stats(clan_tag: str) -> None:
    """
    Displays basic clan war statistics.
    """
    print(f"\n📊 Fetching clan information...")
    
    # You could add more clan stats here if needed
    # For now, this is a placeholder that the main function calls
    pass

# ========= MAIN =========
def main():
    """Main function to fetch and display war information."""
    print("🏰 Clash of Clans War Information Fetcher")
    print("=" * 80)
    
    # Check if API key is set
    if not API_KEY:
        print("\n❌ ERROR: API key not set!")
        print("\nTo use this script:")
        print("1. Get an API key from https://developer.clashofclans.com/")
        print("2. Set it as an environment variable: export COC_API_KEY='your-api-key'")
        print("3. Or edit this script and set API_KEY variable directly")
        return
    
    # Use the configured clan tag
    clan_tag = CLAN_TAG
    print(f"\n📋 Analyzing clan: {clan_tag}")
    
    # Display clan stats
    display_clan_war_stats(clan_tag)
    
    # Get and display current war with attack tracking
    print("\n⏳ Fetching current war information...")
    war_log_data = log_current_war_attacks(clan_tag)
    
    # Auto-save war data if available
    if war_log_data:
        filename = save_war_data_unique(war_log_data)
        print(f"\n💾 War data automatically saved to: {filename}")
    
    # Get and display war history
    print("\n⏳ Fetching war history...")
    war_log = get_war_log(clan_tag, limit=10)
    if war_log:
        display_war_log(war_log, count=3)
        display_detailed_war_analysis(war_log, count=3)
    
    # Generate all tables
    generate_all_tables()
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
