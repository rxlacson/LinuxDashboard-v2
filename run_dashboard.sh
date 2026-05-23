#!/bin/bash
# Dashboard Launcher Script

# Make scripts executable
chmod +x dashboard_scripts/*.sh

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Launch the dashboard
clear
echo "🚀 Starting Linux Admin Dashboard..."
echo "======================================"
echo ""

python3 admin_dashboard.py