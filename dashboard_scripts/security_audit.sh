#!/bin/bash
# Basic Security Audit Script

echo "🛡️  SECURITY AUDIT"
echo "=================="

# Check for users with UID 0 (root privileges)
echo "👑 Users with root privileges:"
awk -F: '($3 == "0") {print $1}' /etc/passwd

# Check for accounts without passwords
echo -e "\n🔓 Accounts without passwords:"
sudo awk -F: '($2 == "" ) {print $1}' /etc/shadow 2>/dev/null || echo "Cannot access shadow file"

# Check for world-writable files
echo -e "\n📝 World-writable files in /etc:"
find /etc -perm -002 -type f 2>/dev/null | head -10

# Check SSH configuration
echo -e "\n🔐 SSH Security Status:"
if [ -f /etc/ssh/sshd_config ]; then
    echo "SSH config exists"
    grep -E "PermitRootLogin|PasswordAuthentication|Port" /etc/ssh/sshd_config | head -5
else
    echo "SSH config not found"
fi

# Check for SUID files
echo -e "\n⚡ SUID files (first 10):"
find / -perm -4000 -type f 2>/dev/null | head -10

# Check listening services
echo -e "\n👂 Services listening on network:"
netstat -tuln | grep LISTEN | head -10

# Check recent logins
echo -e "\n🔄 Recent logins:"
last -10 2>/dev/null

# Check failed login attempts
echo -e "\n❌ Failed login attempts:"
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -5 || echo "No failed login logs accessible"

# Check firewall status
echo -e "\n🔥 Firewall status:"
if command -v ufw &> /dev/null; then
    ufw status
elif command -v firewall-cmd &> /dev/null; then
    firewall-cmd --state
elif command -v iptables &> /dev/null; then
    echo "iptables rules count: $(iptables -L | wc -l)"
else
    echo "No firewall tools detected"
fi

echo -e "\n✅ Security audit complete!"