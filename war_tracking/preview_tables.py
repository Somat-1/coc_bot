#!/usr/bin/env python3
"""
Preview Tables - Shows what the CSV tables will contain

This script displays the column structure and example data for all three tables.
Useful for understanding what data will be available before tracking actual wars.
"""

def preview_tables():
    print("=" * 100)
    print("📊 WAR TRACKING TABLES PREVIEW")
    print("=" * 100)
    
    print("\n1️⃣  WAR SUMMARY TABLE (war_summary.csv)")
    print("-" * 100)
    print("Columns:")
    columns_war_summary = [
        "War Date",
        "War State", 
        "Result",
        "Our Stars",
        "Opponent Stars",
        "Our Destruction %",
        "Opponent Destruction %",
        "Team Size",
        "Attacks Used",
        "Total Possible Attacks",
        "Participation Rate %"
    ]
    for i, col in enumerate(columns_war_summary, 1):
        print(f"  {i:2d}. {col}")
    
    print("\nExample Data:")
    print("  War Date             | State    | Result | Stars | Destruction % | Participation %")
    print("  2026-01-20 15:46     | warEnded | Win    | 74/68 | 99.50/95.20   | 96.00")
    print("  2026-01-18 10:30     | warEnded | Loss   | 65/70 | 92.10/97.30   | 90.00")
    
    print("\n\n2️⃣  PER-WAR MEMBER PERFORMANCE TABLE (per_war_member_performance.csv)")
    print("-" * 100)
    print("Columns:")
    columns_member_perf = [
        "War Date",
        "Member Name",
        "Member Tag",
        "Attacked?",
        "Attacks Used",
        "Total Stars",
        "Avg Stars per Attack",
        "Avg Destruction %",
        "Best Attack Stars",
        "Best Attack Destruction %"
    ]
    for i, col in enumerate(columns_member_perf, 1):
        print(f"  {i:2d}. {col}")
    
    print("\nExample Data:")
    print("  War Date         | Member    | Tag      | Status  | Attacks | Stars | Avg Stars | Best")
    print("  2026-01-20 15:46 | PlayerOne | #ABC123  | All     | 2       | 6     | 3.00      | 3⭐ 100%")
    print("  2026-01-20 15:46 | PlayerTwo | #DEF456  | Partial | 1       | 2     | 2.00      | 2⭐ 75%")
    print("  2026-01-20 15:46 | PlayerX   | #GHI789  | None    | 0       | 0     | 0.00      | 0⭐ 0%")
    
    print("\n\n3️⃣  OVERALL MEMBER PERFORMANCE TABLE (overall_member_performance.csv)")
    print("-" * 100)
    print("Columns:")
    columns_overall = [
        "Member Name",
        "Member Tag",
        "Total Wars Participated",
        "Wars Attacked (All)",
        "Wars Attacked (Partial)",
        "Wars Missed (No Attacks)",
        "Full Participation Rate %",
        "Total Attacks Made",
        "Total Stars Earned",
        "Avg Stars per Attack",
        "Avg Destruction per Attack %"
    ]
    for i, col in enumerate(columns_overall, 1):
        print(f"  {i:2d}. {col}")
    
    print("\nExample Data:")
    print("  Member    | Tag     | Wars | Full | Partial | Missed | Rate  | Total Atk | Stars | Avg")
    print("  PlayerOne | #ABC123 | 10   | 9    | 1       | 0      | 90.00 | 19        | 54    | 2.84⭐")
    print("  PlayerTwo | #DEF456 | 10   | 8    | 0       | 2      | 80.00 | 16        | 42    | 2.63⭐")
    print("  PlayerX   | #GHI789 | 10   | 6    | 2       | 2      | 60.00 | 14        | 35    | 2.50⭐")
    
    print("\n" + "=" * 100)
    print("📝 NOTES")
    print("=" * 100)
    print("• Tables are automatically generated when you run: python war_info.py")
    print("• CSV files can be opened in Excel, Google Sheets, or any spreadsheet software")
    print("• More wars tracked = more valuable insights")
    print("• Tables update automatically each time you run the script")
    
    print("\n" + "=" * 100)
    print("🎯 WHAT YOU CAN ANALYZE")
    print("=" * 100)
    print("War Summary Table:")
    print("  → Win/loss trends over time")
    print("  → Participation rate patterns")
    print("  → Impact of team size on results")
    
    print("\nPer-War Member Performance:")
    print("  → Individual performance in specific wars")
    print("  → Member improvement over time")
    print("  → Comparison between members")
    
    print("\nOverall Member Performance:")
    print("  → Most reliable members (high participation rate)")
    print("  → Best attackers (high avg stars per attack)")
    print("  → Members needing improvement")
    
    print("\n" + "=" * 100)
    print("✅ Ready to start tracking! Run: python war_info.py")
    print("=" * 100)

if __name__ == "__main__":
    preview_tables()
