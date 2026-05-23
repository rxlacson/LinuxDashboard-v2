#!/bin/bash
# Network Diagnostics Script

echo "🌐 NETWORK DIAGNOSTICS"
echo "====================="

# Check network interfaces
echo "🔌 Network Interfaces:"
ip addr show | grep -E '^[0-9]+:|inet ' | head -20

# Check default gateway
echo -e "\n🚪 Default Gateway:"
ip route show default

# Check DNS servers
echo -e "\n🔍 DNS Servers:"
cat /etc/resolv.conf | grep nameserver

# Test connectivity to common sites
echo -e "\n🏓 Connectivity Tests:"
for site in google.com cloudflare.com 8.8.8.8; do
    echo -n "Testing $site: "
    if ping -c 1 -W 2 $site &> /dev/null; then
        echo "✅ OK"
    else
        echo "❌ FAILED"
    fi
done

# Check listening ports
echo -e "\n👂 Listening Ports:"
netstat -tuln | head -10

# Check active connections
echo -e "\n🔗 Active Connections:"
netstat -tu | grep ESTABLISHED | wc -l
echo "Active TCP/UDP connections found"

# Check network statistics
echo -e "\n📈 Network Statistics:"
cat /proc/net/dev | head -5

echo -e "\n✅ Network diagnostics complete!"