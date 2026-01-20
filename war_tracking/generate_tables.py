#!/usr/bin/env python3
"""
Generate CSV tables from war data.

This script generates three CSV files:
1. war_summary.csv - Summary of all wars (results, stars, destruction, participation)
2. per_war_member_performance.csv - Member performance for each individual war
3. overall_member_performance.csv - Aggregate member stats across all wars

Usage:
    python generate_tables.py
"""

from war_info import generate_all_tables

if __name__ == "__main__":
    generate_all_tables()
