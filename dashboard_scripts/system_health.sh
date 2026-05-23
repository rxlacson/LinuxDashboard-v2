#!/bin/bash
# System Health Check Script

echo "🩺 SYSTEM HEALTH CHECK"
echo "===================="

# Check system load
echo "📊 System Load:"
uptime

# Check memory usage
echo -e "\n💾 Memory Usage:"
free -h

# Check disk usage
echo -e "\n💿 Disk Usage:"
df -h | grep -E '(Filesystem|/dev/)'

# Check for high CPU processes
echo -e "\n🔥 Top CPU Processes:"
ps aux --sort=-%cpu | head -6

# Check for high memory processes
echo -e "\n🧠 Top Memory Processes:"
ps aux --sort=-%mem | head -6

# Check system temperature (if available)
echo -e "\n🌡️  System Temperature:"
if command -v sensors &> /dev/null; then
    sensors | grep -E '(Core|temp)' | head -5
else
    echo "Temperature sensors not available"
fi

# Check failed services
echo -e "\n❌ Failed Services:"
if command -v systemctl &> /dev/null; then
    failed_services=$(systemctl --failed --no-legend | wc -l)
    if [ $failed_services -gt 0 ]; then
        systemctl --failed --no-legend
    else
        echo "No failed services"
    fi
else
    echo "systemctl not available"
fi

echo -e "\n✅ Health check complete!"