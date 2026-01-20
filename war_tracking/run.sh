#!/bin/bash
# Quick launcher for War Tracker

cd "$(dirname "$0")"
source ../env/bin/activate
python war_tracker.py
