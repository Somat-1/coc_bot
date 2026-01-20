# 🧹 Cleanup Plan

## Files to Remove from Root Directory

### Duplicate Documentation (already in war_tracking/)
- IMPLEMENTATION_COMPLETE.md
- TABLE_GENERATION_GUIDE.md
- WAR_ANALYSIS_GUIDE.md
- WAR_INFO_README.md
- WAR_TRACKING_README.md

### Duplicate Scripts (already in war_tracking/)
- generate_tables.py
- preview_tables.py
- war_info.py

### Debug/Test Files
- test_messages.py
- test_pinch_zoom.py
- test_zoom_out.py

### Debug Images (large files)
- debug_full_overlay.png
- debug_full_overlay_emulator-5554.png
- debug_full_overlay_emulator-5564.png
- donation_debug.png
- screen.png
- screen_emulator-5554.png
- screen_emulator-5564.png

## Files to Remove from war_tracking/

### Duplicate/Outdated Documentation
- IMPLEMENTATION_COMPLETE.md (superseded by COMPLETION_CHECKLIST.md)
- EXCEL_COMPLETE.md (merged into FINAL_SUMMARY.md)
- UNIFIED_COMPLETE.md (superseded by FINAL_SUMMARY.md)
- TABLE_GENERATION_GUIDE.md (superseded by EXCEL_GUIDE.md)
- WAR_ANALYSIS_GUIDE.md (superseded by INDIVIDUAL_ATTACKS_GUIDE.md)
- WAR_INFO_README.md (superseded by README.md)
- WAR_TRACKING_README.md (superseded by README.md)

## Files to Keep

### Root Directory
- bb_farm.py (bot farming script)
- continuous_attack.py (bot attack script)
- donate.py (bot donation script)
- event.py (bot event handler)
- main.py (main bot script)
- main2.py (alternative main)
- main_cont.py (continuous main)
- utils/ (helper utilities)
- war_tracking/ (complete war tracking system)
- .gitignore (git configuration)

### war_tracking/ Directory
- README.md (main documentation)
- START_HERE.md (quick start)
- RUN_THIS.md (usage guide)
- QUICK_GUIDE.md (quick reference)
- EXCEL_GUIDE.md (Excel features)
- INDIVIDUAL_ATTACKS_GUIDE.md (attack tracking)
- COMPLETION_CHECKLIST.md (project status)
- FINAL_SUMMARY.md (project summary)
- WHERE_IS_EVERYTHING.md (navigation)
- war_tracker.py (main menu system)
- war_info.py (core engine)
- generate_excel_tables.py (Excel generation)
- generate_tables.py (CSV generation)
- preview_tables.py (preview utility)
- run.sh (launcher)
- war_data/ (data storage)

## Action Plan

1. Remove duplicate documentation from root
2. Remove duplicate scripts from root
3. Remove debug images from root
4. Remove outdated documentation from war_tracking/
5. Keep generated CSV/XLSX (user may want them)
6. Keep war_data/ JSON files (important data)
7. Create .gitignore to exclude large/temporary files
8. Initialize git repository
9. Commit cleaned structure
10. Ready for push to remote
