#!/usr/bin/env python3
"""
Automated War Monitor - Continuously tracks active wars and updates data

Features:
- Checks time until war end
- If < 3 hours: Monitors continuously
- Updates every 30 minutes normally
- Updates every 2 minutes in last 10 minutes
- Auto-saves and generates tables when war ends
"""

import time
from datetime import datetime, timezone
from typing import Optional, Dict
import sys

from war_info import (
    get_current_war,
    log_current_war_attacks,
    save_war_data_unique,
    CLAN_TAG,
    generate_all_tables
)
from generate_excel_tables import generate_all_excel_tables


def get_time_until_war_end(war_data: Dict) -> Optional[float]:
    """
    Calculate seconds until war ends.
    
    Returns:
        Seconds until war end, or None if can't calculate
    """
    if not war_data or 'endTime' not in war_data:
        return None
    
    try:
        # Parse war end time (format: "20260120T154611.000Z")
        end_time_str = war_data['endTime']
        end_time = datetime.strptime(end_time_str, "%Y%m%dT%H%M%S.%fZ")
        end_time = end_time.replace(tzinfo=timezone.utc)
        
        # Current time
        now = datetime.now(timezone.utc)
        
        # Calculate difference
        time_diff = (end_time - now).total_seconds()
        
        return max(0, time_diff)  # Don't return negative values
    except Exception as e:
        print(f"⚠️  Error calculating time until war end: {e}")
        return None


def format_time_remaining(seconds: float) -> str:
    """Format seconds into human-readable time."""
    if seconds <= 0:
        return "War Ended"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def update_war_data() -> Optional[Dict]:
    """
    Fetch and save current war data.
    
    Returns:
        War log data if successful, None otherwise
    """
    print(f"\n{'='*80}")
    print(f"🔄 UPDATING WAR DATA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")
    
    war_log_data = log_current_war_attacks(CLAN_TAG)
    
    if war_log_data:
        filename = save_war_data_unique(war_log_data)
        print(f"✅ Data saved to: {filename}")
        return war_log_data
    else:
        print("❌ Failed to fetch war data")
        return None


def generate_final_tables():
    """Generate both CSV and Excel tables."""
    print(f"\n{'='*80}")
    print("📊 GENERATING FINAL TABLES")
    print(f"{'='*80}")
    
    print("\n📊 Generating CSV tables...")
    generate_all_tables()
    
    print("\n📊 Generating Excel tables...")
    generate_all_excel_tables()
    
    print(f"\n✅ All tables generated successfully!")


def monitor_war():
    """Main monitoring loop."""
    print("=" * 80)
    print("🏰 AUTOMATED WAR MONITOR")
    print("=" * 80)
    print(f"Clan: {CLAN_TAG}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Initial check
    print("\n🔍 Checking current war status...")
    war_data = get_current_war(CLAN_TAG)
    
    if not war_data:
        print("\n❌ Could not fetch war data. Exiting.")
        return
    
    state = war_data.get('state', 'unknown')
    
    if state == 'notInWar':
        print("\n❌ Clan is not currently in war. Nothing to monitor.")
        return
    
    if state == 'preparation':
        print("\n⚠️  War is in preparation phase. Will start monitoring when war begins.")
        print("💡 Tip: Run this script again when the war starts.")
        return
    
    # Calculate time until war end
    time_remaining = get_time_until_war_end(war_data)
    
    if time_remaining is None:
        print("\n❌ Could not calculate time until war end. Exiting.")
        return
    
    print(f"\n⏰ Time until war end: {format_time_remaining(time_remaining)}")
    
    # Check if we should start monitoring
    THREE_HOURS = 3 * 60 * 60  # 3 hours in seconds
    
    if time_remaining > THREE_HOURS:
        hours_until_monitor = (time_remaining - THREE_HOURS) / 3600
        print(f"\n⏳ War end is more than 3 hours away ({hours_until_monitor:.1f}h)")
        print(f"💡 Monitoring will start in {hours_until_monitor:.1f} hours")
        print(f"💡 Run this script again closer to war end, or leave it running to auto-start monitoring.")
        
        # Ask if user wants to wait
        try:
            response = input("\n⏰ Wait until 3 hours before war end? (y/n): ").strip().lower()
            if response != 'y':
                print("\n👋 Exiting. Run this script again later.")
                return
            
            # Wait until 3 hours before war end
            wait_time = time_remaining - THREE_HOURS
            print(f"\n⏳ Waiting {format_time_remaining(wait_time)} until monitoring starts...")
            print("💡 Press Ctrl+C to cancel")
            time.sleep(wait_time)
            
            # Refresh war data after waiting
            war_data = get_current_war(CLAN_TAG)
            if not war_data:
                print("\n❌ Could not fetch updated war data. Exiting.")
                return
            time_remaining = get_time_until_war_end(war_data)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Monitoring cancelled by user.")
            return
    
    # Start monitoring
    print(f"\n{'='*80}")
    print("🚀 STARTING CONTINUOUS MONITORING")
    print(f"{'='*80}")
    print(f"⏰ Monitoring started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️  Time remaining: {format_time_remaining(time_remaining)}")
    print(f"\n📋 Update Schedule:")
    print(f"   • Every 30 minutes (normal)")
    print(f"   • Every 2 minutes (last 10 minutes)")
    print(f"   • Auto-save when war ends")
    print(f"\n💡 Press Ctrl+C to stop monitoring")
    print(f"{'='*80}\n")
    
    last_update_time = time.time()
    update_count = 0
    
    try:
        while True:
            # Fetch current war data
            war_data = get_current_war(CLAN_TAG)
            
            if not war_data:
                print("\n⚠️  Could not fetch war data. Retrying in 1 minute...")
                time.sleep(60)
                continue
            
            state = war_data.get('state', 'unknown')
            time_remaining = get_time_until_war_end(war_data)
            
            if time_remaining is None:
                print("\n⚠️  Could not calculate time remaining. Retrying in 1 minute...")
                time.sleep(60)
                continue
            
            # Check if war has ended
            if state == 'warEnded' or time_remaining <= 0:
                print("\n" + "="*80)
                print("🏁 WAR HAS ENDED!")
                print("="*80)
                
                # Final update
                print("\n📊 Performing final data update...")
                final_data = update_war_data()
                
                if final_data:
                    # Generate all tables
                    generate_final_tables()
                    
                    print("\n" + "="*80)
                    print("✅ MONITORING COMPLETE")
                    print("="*80)
                    print(f"Total updates performed: {update_count + 1}")
                    print(f"Final data saved to: war_data/")
                    print(f"Tables generated:")
                    print(f"  • CSV: war_summary.csv")
                    print(f"  • CSV: per_war_member_performance.csv")
                    print(f"  • CSV: overall_member_performance.csv")
                    print(f"  • Excel: per_war_member_performance.xlsx")
                    print(f"  • Excel: overall_member_performance.xlsx")
                    print("="*80)
                else:
                    print("\n⚠️  Failed to perform final update")
                
                break
            
            # Determine update interval based on time remaining
            TEN_MINUTES = 10 * 60  # 10 minutes in seconds
            THIRTY_MINUTES = 30 * 60  # 30 minutes in seconds
            TWO_MINUTES = 2 * 60  # 2 minutes in seconds
            
            if time_remaining <= TEN_MINUTES:
                # Last 10 minutes: Update every 2 minutes
                update_interval = TWO_MINUTES
                status = "🔴 FINAL PHASE"
            else:
                # More than 10 minutes: Update every 30 minutes
                update_interval = THIRTY_MINUTES
                status = "🟢 MONITORING"
            
            # Check if it's time to update
            time_since_last_update = time.time() - last_update_time
            
            if time_since_last_update >= update_interval:
                # Perform update
                update_count += 1
                print(f"\n[{status}] Update #{update_count} - {format_time_remaining(time_remaining)} remaining")
                
                war_log_data = update_war_data()
                
                if war_log_data:
                    last_update_time = time.time()
                    print(f"✅ Update #{update_count} completed")
                    
                    # Show quick stats
                    member_analysis = war_log_data.get('member_analysis', {})
                    full_attacks = member_analysis.get('used_all_attacks', 0)
                    partial = member_analysis.get('partial_attacks', 0)
                    missed = member_analysis.get('no_attacks', 0)
                    
                    clan_stats = war_log_data.get('clan', {})
                    opponent_stats = war_log_data.get('opponent', {})
                    
                    print(f"📊 Quick Stats:")
                    print(f"   Score: {clan_stats.get('stars', 0)}⭐ vs {opponent_stats.get('stars', 0)}⭐")
                    print(f"   Attacks: {full_attacks} full, {partial} partial, {missed} missed")
                else:
                    print(f"⚠️  Update #{update_count} failed")
                
                # Calculate next update time
                if time_remaining <= TEN_MINUTES:
                    next_update = TWO_MINUTES
                else:
                    next_update = THIRTY_MINUTES
                
                print(f"⏰ Next update in: {format_time_remaining(next_update)}")
            
            # Sleep for 30 seconds before next check
            time.sleep(30)
    
    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print("⚠️  MONITORING STOPPED BY USER")
        print("="*80)
        print(f"Updates performed: {update_count}")
        print("💡 Run this script again to resume monitoring")
        print("="*80)
    
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        print("⚠️  Monitoring stopped due to error")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point."""
    try:
        monitor_war()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
