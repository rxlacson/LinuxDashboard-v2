#!/bin/bash
# System Cleanup Script

echo "🧹 SYSTEM CLEANUP"
echo "=================="

# Show initial disk usage
echo "💿 Initial Disk Usage:"
df -h /

echo -e "\n🗂️  Starting cleanup..."

# Clean temporary files
echo "Cleaning temporary files..."
sudo find /tmp -type f -atime +7 -delete 2>/dev/null && echo "✅ Old temp files cleaned"

# Clean log files older than 30 days
echo "Cleaning old log files..."
sudo find /var/log -name "*.log" -type f -mtime +30 -delete 2>/dev/null && echo "✅ Old logs cleaned"

# Clean package cache
echo "Cleaning package cache..."
if command -v apt &> /dev/null; then
    sudo apt autoremove -y &> /dev/null
    sudo apt autoclean &> /dev/null
    echo "✅ APT cache cleaned"
elif command -v yum &> /dev/null; then
    sudo yum clean all &> /dev/null
    echo "✅ YUM cache cleaned"
elif command -v dnf &> /dev/null; then
    sudo dnf clean all &> /dev/null
    echo "✅ DNF cache cleaned"
fi

# Clean thumbnail cache
if [ -d "$HOME/.cache/thumbnails" ]; then
    rm -rf $HOME/.cache/thumbnails/*
    echo "✅ Thumbnail cache cleaned"
fi

# Clean browser cache (if found)
if [ -d "$HOME/.cache/google-chrome" ]; then
    rm -rf $HOME/.cache/google-chrome/Default/Cache/*
    echo "✅ Chrome cache cleaned"
fi

# Clean old kernels (Ubuntu/Debian)
if command -v apt &> /dev/null; then
    old_kernels=$(dpkg -l | grep linux-image | grep -v $(uname -r) | wc -l)
    if [ $old_kernels -gt 0 ]; then
        echo "Found $old_kernels old kernel(s) - manual removal recommended"
    fi
fi

# Show final disk usage
echo -e "\n💿 Final Disk Usage:"
df -h /

echo -e "\n✅ System cleanup complete!"