#!/usr/bin/env python3
"""
Clash of Clans War Tracker - Unified Menu System

All-in-one script for tracking wars, generating tables, and viewing data.
"""

import os
import sys
from datetime import datetime

# Import functions from war_info.py
from war_info import (
    log_current_war_attacks,
    save_war_data_unique,
    generate_all_tables,
    generate_war_summary_table,
    generate_per_war_member_table,
    generate_overall_member_performance_table,
    get_war_log,
    display_war_log,
    display_detailed_war_analysis,
    WAR_DATA_DIR,
    CLAN_TAG
)

# Import Excel generation functions
from generate_excel_tables import (
    generate_all_excel_tables,
    generate_per_war_tables_excel,
    generate_overall_member_performance_excel
)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    """Print the application header."""
    print("=" * 80)
    print("🏰 CLASH OF CLANS WAR TRACKER")
    print("=" * 80)
    print(f"Clan: {CLAN_TAG}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

def print_menu():
    """Print the main menu."""
    print("\n📋 MAIN MENU")
    print("-" * 80)
    print("1️⃣  Track Current War (Full Analysis)")
    print("2️⃣  View War History")
    print("3️⃣  Generate All CSV Tables")
    print("4️⃣  Generate War Summary Table Only")
    print("5️⃣  Generate Per-War Member Table Only")
    print("6️⃣  Generate Overall Member Table Only")
    print("7️⃣  Generate All Excel Tables (XLSX)")
    print("8️⃣  View Table Files Location")
    print("9️⃣  Open Files in Finder")
    print("🔟  Show Table Preview")
    print("1️⃣1️⃣  View Statistics")
    print("0️⃣  Exit")
    print("-" * 80)

def track_current_war():
    """Track the current war."""
    clear_screen()
    print_header()
    print("\n⚙️  TRACKING CURRENT WAR")
    print("=" * 80)
    
    war_log_data = log_current_war_attacks(CLAN_TAG)
    
    if war_log_data:
        filename = save_war_data_unique(war_log_data)
        print(f"\n💾 War data automatically saved to: war_data/{filename}")
        
        # Offer to generate tables
        print("\n" + "=" * 80)
        choice = input("\n📊 Generate CSV tables now? (y/n): ").strip().lower()
        if choice == 'y':
            generate_all_tables()
    
    input("\n\nPress Enter to continue...")

def view_war_history():
    """View war history."""
    clear_screen()
    print_header()
    print("\n📜 WAR HISTORY")
    print("=" * 80)
    
    try:
        count = int(input("\nHow many wars to display? (default: 5): ").strip() or "5")
    except ValueError:
        count = 5
    
    war_log = get_war_log(CLAN_TAG, limit=count)
    if war_log:
        display_war_log(war_log, count=count)
        display_detailed_war_analysis(war_log, count=count)
    
    input("\n\nPress Enter to continue...")

def generate_tables_menu():
    """Generate all tables."""
    clear_screen()
    print_header()
    print("\n📊 GENERATING ALL CSV TABLES")
    print("=" * 80)
    
    generate_all_tables()
    
    print("\n" + "=" * 80)
    print("💡 TIP: You can now open these CSV files in Excel or Google Sheets!")
    print("   Location: war_tracking/")
    
    input("\n\nPress Enter to continue...")

def generate_war_summary_menu():
    """Generate war summary table only."""
    clear_screen()
    print_header()
    print("\n📊 GENERATING WAR SUMMARY TABLE")
    print("=" * 80)
    
    generate_war_summary_table()
    
    input("\n\nPress Enter to continue...")

def generate_per_war_menu():
    """Generate per-war member table only."""
    clear_screen()
    print_header()
    print("\n📊 GENERATING PER-WAR MEMBER PERFORMANCE TABLE")
    print("=" * 80)
    
    generate_per_war_member_table()
    
    input("\n\nPress Enter to continue...")

def generate_overall_menu():
    """Generate overall member performance table only."""
    clear_screen()
    print_header()
    print("\n📊 GENERATING OVERALL MEMBER PERFORMANCE TABLE")
    print("=" * 80)
    
    generate_overall_member_performance_table()
    
    input("\n\nPress Enter to continue...")

def generate_excel_tables_menu():
    """Generate all Excel tables."""
    clear_screen()
    print_header()
    print("\n📊 GENERATING ALL EXCEL TABLES")
    print("=" * 80)
    
    generate_all_excel_tables()
    
    print("\n" + "=" * 80)
    print("💡 TIP: Open these Excel files for formatted tables with color-coding!")
    print("   Location: war_tracking/")
    print("   Files:")
    print("   • per_war_member_performance.xlsx (separate sheet per war)")
    print("   • overall_member_performance.xlsx (with color-coded warnings)")
    
    input("\n\nPress Enter to continue...")

def view_files_location():
    """Show where files are located."""
    clear_screen()
    print_header()
    print("\n📁 FILE LOCATIONS")
    print("=" * 80)
    
    current_dir = os.getcwd()
    
    print(f"\n📂 Current Directory:")
    print(f"   {current_dir}")
    
    print(f"\n📊 CSV Table Files:")
    csv_files = ['war_summary.csv', 'per_war_member_performance.csv', 'overall_member_performance.csv']
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            size = os.path.getsize(csv_file)
            print(f"   ✅ {csv_file} ({size} bytes)")
        else:
            print(f"   ❌ {csv_file} (not created yet)")
    
    print(f"\n📊 Excel Table Files:")
    excel_files = ['per_war_member_performance.xlsx', 'overall_member_performance.xlsx']
    for excel_file in excel_files:
        if os.path.exists(excel_file):
            size = os.path.getsize(excel_file)
            print(f"   ✅ {excel_file} ({size} bytes)")
        else:
            print(f"   ❌ {excel_file} (not created yet)")
    
    print(f"\n📁 War Data Directory:")
    if os.path.exists(WAR_DATA_DIR):
        json_files = [f for f in os.listdir(WAR_DATA_DIR) if f.endswith('.json')]
        print(f"   {WAR_DATA_DIR}/ ({len(json_files)} war(s) tracked)")
        if json_files:
            print(f"\n   Latest wars:")
            for f in sorted(json_files, reverse=True)[:5]:
                print(f"   • {f}")
    else:
        print(f"   ❌ {WAR_DATA_DIR}/ (not created yet)")
    
    print(f"\n💡 To open in Finder:")
    print(f"   Run: open {current_dir}")
    
    input("\n\nPress Enter to continue...")

def open_in_finder():
    """Open the current directory in Finder."""
    clear_screen()
    print_header()
    print("\n📂 OPENING IN FINDER")
    print("=" * 80)
    
    current_dir = os.getcwd()
    os.system(f'open "{current_dir}"')
    
    print(f"\n✅ Opened: {current_dir}")
    print("\n📊 Look for these files:")
    print("\n   CSV Files:")
    print("   • war_summary.csv")
    print("   • per_war_member_performance.csv")
    print("   • overall_member_performance.csv")
    print("\n   Excel Files:")
    print("   • per_war_member_performance.xlsx")
    print("   • overall_member_performance.xlsx")
    
    input("\n\nPress Enter to continue...")

def show_table_preview():
    """Show what the tables contain."""
    clear_screen()
    print_header()
    print("\n👁️  TABLE STRUCTURE PREVIEW")
    print("=" * 80)
    
    print("\n1️⃣  WAR SUMMARY TABLE (war_summary.csv)")
    print("-" * 80)
    print("Columns:")
    columns_war = [
        "War Date", "War State", "Result", "Our Stars", "Opponent Stars",
        "Our Destruction %", "Opponent Destruction %", "Team Size",
        "Attacks Used", "Total Possible Attacks", "Participation Rate %"
    ]
    for i, col in enumerate(columns_war, 1):
        print(f"  {i:2d}. {col}")
    
    print("\n\n2️⃣  PER-WAR MEMBER PERFORMANCE TABLE (per_war_member_performance.csv)")
    print("-" * 80)
    print("Columns:")
    columns_member = [
        "War Date", "Member Name", "Member Tag", "Attacked?", "Attacks Used",
        "Total Stars", "Avg Stars per Attack", "Avg Destruction %",
        "Best Attack Stars", "Best Attack Destruction %"
    ]
    for i, col in enumerate(columns_member, 1):
        print(f"  {i:2d}. {col}")
    
    print("\n\n3️⃣  OVERALL MEMBER PERFORMANCE TABLE (overall_member_performance.csv)")
    print("-" * 80)
    print("Columns:")
    columns_overall = [
        "Member Name", "Member Tag", "Total Wars Participated",
        "Wars Attacked (All)", "Wars Attacked (Partial)", "Wars Missed (No Attacks)",
        "Full Participation Rate %", "Total Attacks Made", "Total Stars Earned",
        "Avg Stars per Attack", "Avg Destruction per Attack %"
    ]
    for i, col in enumerate(columns_overall, 1):
        print(f"  {i:2d}. {col}")
    
    input("\n\nPress Enter to continue...")

def view_statistics():
    """View current statistics."""
    clear_screen()
    print_header()
    print("\n📊 CURRENT STATISTICS")
    print("=" * 80)
    
    # Count wars tracked
    wars_tracked = 0
    if os.path.exists(WAR_DATA_DIR):
        json_files = [f for f in os.listdir(WAR_DATA_DIR) if f.endswith('.json')]
        wars_tracked = len(json_files)
    
    print(f"\n🏆 Wars Tracked: {wars_tracked}")
    
    # Check CSV files
    csv_files = {
        'War Summary (CSV)': 'war_summary.csv',
        'Per-War Performance (CSV)': 'per_war_member_performance.csv',
        'Overall Performance (CSV)': 'overall_member_performance.csv'
    }
    
    print(f"\n📊 CSV Tables:")
    for name, filename in csv_files.items():
        if os.path.exists(filename):
            # Count lines (rows)
            with open(filename, 'r') as f:
                lines = len(f.readlines()) - 1  # Subtract header
            print(f"   ✅ {name}: {lines} rows")
        else:
            print(f"   ❌ {name}: Not generated yet")
    
    # Check Excel files
    excel_files = {
        'Per-War Performance (Excel)': 'per_war_member_performance.xlsx',
        'Overall Performance (Excel)': 'overall_member_performance.xlsx'
    }
    
    print(f"\n📊 Excel Tables:")
    for name, filename in excel_files.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024  # KB
            print(f"   ✅ {name}: {size:.1f} KB")
        else:
            print(f"   ❌ {name}: Not generated yet")
    
    # Show war data directory info
    if os.path.exists(WAR_DATA_DIR):
        print(f"\n📁 War Data Files:")
        json_files = sorted([f for f in os.listdir(WAR_DATA_DIR) if f.endswith('.json')])
        if json_files:
            print(f"   Total: {len(json_files)} war(s)")
            print(f"   Oldest: {json_files[0]}")
            print(f"   Newest: {json_files[-1]}")
        else:
            print(f"   No wars tracked yet")
    
    print(f"\n💾 Storage Location:")
    print(f"   {os.getcwd()}")
    
    input("\n\nPress Enter to continue...")

def main():
    """Main application loop."""
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("\nSelect an option (0-11): ").strip()
        
        if choice == '1':
            track_current_war()
        elif choice == '2':
            view_war_history()
        elif choice == '3':
            generate_tables_menu()
        elif choice == '4':
            generate_war_summary_menu()
        elif choice == '5':
            generate_per_war_menu()
        elif choice == '6':
            generate_overall_menu()
        elif choice == '7':
            generate_excel_tables_menu()
        elif choice == '8':
            view_files_location()
        elif choice == '9':
            open_in_finder()
        elif choice == '10':
            show_table_preview()
        elif choice == '11':
            view_statistics()
        elif choice == '0':
            clear_screen()
            print("\n" + "=" * 80)
            print("👋 Thank you for using Clash of Clans War Tracker!")
            print("=" * 80)
            print("\n📊 Your data is saved in:")
            print(f"   {os.getcwd()}")
            print("\n💡 Run this script anytime to track wars or generate tables!")
            print("=" * 80 + "\n")
            sys.exit(0)
        else:
            print("\n❌ Invalid option. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
