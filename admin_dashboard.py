#!/usr/bin/env python3
"""
Linux Admin Dashboard
A terminal-based dashboard for common administrative tasks
"""

import os
import sys
import subprocess
import platform
import json
from datetime import datetime
import shutil

class AdminDashboard:
    def __init__(self):
        self.scripts_dir = os.path.join(os.path.dirname(__file__), 'dashboard_scripts')
        self.config_file = os.path.join(os.path.dirname(__file__), 'dashboard_config.json')
        self.ensure_scripts_directory()
        self.load_config()

    def ensure_scripts_directory(self):
        """Create scripts directory if it doesn't exist"""
        if not os.path.exists(self.scripts_dir):
            os.makedirs(self.scripts_dir)

    def load_config(self):
        """Load or create dashboard configuration"""
        default_config = {
            "last_run": "",
            "favorite_commands": [],
            "custom_commands": {}
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()

    def save_config(self):
        """Save current configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_header(self):
        """Print dashboard header"""
        self.clear_screen()
        print("=" * 70)
        print("🖥️  LINUX ADMIN DASHBOARD")
        print("=" * 70)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Host: {platform.node()}")
        print(f"User: {os.getenv('USER', 'unknown')}")
        print("=" * 70)

    def run_command(self, command, description=""):
        """Execute a command and display results"""
        print(f"\n📋 {description}")
        print(f"💻 Running: {command}")
        print("-" * 50)

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            if result.stdout:
                print("✅ Output:")
                print(result.stdout)

            if result.stderr:
                print("⚠️  Errors/Warnings:")
                print(result.stderr)

            if result.returncode != 0:
                print(f"❌ Command failed with exit code: {result.returncode}")
            else:
                print("✅ Command completed successfully")

        except Exception as e:
            print(f"❌ Error executing command: {e}")

        input("\n🔄 Press Enter to continue...")

    def system_monitoring_menu(self):
        """System monitoring submenu"""
        while True:
            self.print_header()
            print("🔍 SYSTEM MONITORING")
            print("-" * 30)
            print("1. System Overview")
            print("2. CPU & Memory Usage")
            print("3. Disk Usage")
            print("4. Network Status")
            print("5. Running Processes")
            print("6. System Logs (last 20 lines)")
            print("7. Uptime & Load Average")
            print("8. Temperature Sensors")
            print("0. Back to Main Menu")

            choice = input("\n👉 Select option: ").strip()

            if choice == '1':
                self.run_command("uname -a && lsb_release -a 2>/dev/null || cat /etc/os-release", "System Information")
            elif choice == '2':
                self.run_command("top -bn1 | head -20 && free -h", "CPU & Memory Usage")
            elif choice == '3':
                self.run_command("df -h && echo '' && du -sh /var/log /tmp /home 2>/dev/null", "Disk Usage")
            elif choice == '4':
                self.run_command("ip addr show && echo '' && netstat -tuln | head -20", "Network Status")
            elif choice == '5':
                self.run_command("ps aux | head -20", "Top Running Processes")
            elif choice == '6':
                self.run_command("tail -n 20 /var/log/syslog 2>/dev/null || tail -n 20 /var/log/messages 2>/dev/null || echo 'No accessible system logs'", "Recent System Logs")
            elif choice == '7':
                self.run_command("uptime && w", "System Uptime & Load")
            elif choice == '8':
                self.run_command("sensors 2>/dev/null || echo 'sensors command not available'", "Temperature Sensors")
            elif choice == '0':
                break

    def service_management_menu(self):
        """Service management submenu"""
        while True:
            self.print_header()
            print("⚙️  SERVICE MANAGEMENT")
            print("-" * 30)
            print("1. List All Services")
            print("2. Active Services Only")
            print("3. Failed Services")
            print("4. Start a Service")
            print("5. Stop a Service")
            print("6. Restart a Service")
            print("7. Check Service Status")
            print("8. Enable Service at Boot")
            print("9. Disable Service at Boot")
            print("0. Back to Main Menu")

            choice = input("\n👉 Select option: ").strip()

            if choice == '1':
                self.run_command("systemctl list-units --type=service", "All Services")
            elif choice == '2':
                self.run_command("systemctl list-units --type=service --state=active", "Active Services")
            elif choice == '3':
                self.run_command("systemctl list-units --type=service --state=failed", "Failed Services")
            elif choice in ['4', '5', '6', '7', '8', '9']:
                service_name = input("Enter service name: ").strip()
                if service_name:
                    if choice == '4':
                        self.run_command(f"sudo systemctl start {service_name}", f"Starting {service_name}")
                    elif choice == '5':
                        self.run_command(f"sudo systemctl stop {service_name}", f"Stopping {service_name}")
                    elif choice == '6':
                        self.run_command(f"sudo systemctl restart {service_name}", f"Restarting {service_name}")
                    elif choice == '7':
                        self.run_command(f"systemctl status {service_name}", f"Status of {service_name}")
                    elif choice == '8':
                        self.run_command(f"sudo systemctl enable {service_name}", f"Enabling {service_name}")
                    elif choice == '9':
                        self.run_command(f"sudo systemctl disable {service_name}", f"Disabling {service_name}")
            elif choice == '0':
                break

    def file_operations_menu(self):
        """File operations submenu"""
        while True:
            self.print_header()
            print("📁 FILE OPERATIONS")
            print("-" * 30)
            print("1. Find Large Files (>100MB)")
            print("2. Clean Temporary Files")
            print("3. Find Recently Modified Files")
            print("4. Disk Usage by Directory")
            print("5. Count Files by Type")
            print("6. Find Empty Directories")
            print("7. Search Files by Name")
            print("8. Show Hidden Files")
            print("0. Back to Main Menu")

            choice = input("\n👉 Select option: ").strip()

            if choice == '1':
                path = input("Enter path to search (default: /): ").strip() or "/"
                self.run_command(f"find {path} -type f -size +100M -exec ls -lh {{}} \\; 2>/dev/null", f"Large Files in {path}")
            elif choice == '2':
                self.run_command("sudo rm -rf /tmp/* /var/tmp/* 2>/dev/null && echo 'Temporary files cleaned'", "Cleaning Temporary Files")
            elif choice == '3':
                path = input("Enter path to search (default: .): ").strip() or "."
                self.run_command(f"find {path} -type f -mtime -1 -ls 2>/dev/null", f"Recently Modified Files in {path}")
            elif choice == '4':
                path = input("Enter path to analyze (default: .): ").strip() or "."
                self.run_command(f"du -sh {path}/* 2>/dev/null | sort -hr", f"Directory Usage in {path}")
            elif choice == '5':
                path = input("Enter path to analyze (default: .): ").strip() or "."
                self.run_command(f"find {path} -type f -name '*.*' 2>/dev/null | sed 's/.*\\.//' | sort | uniq -c | sort -nr", f"File Types in {path}")
            elif choice == '6':
                path = input("Enter path to search (default: .): ").strip() or "."
                self.run_command(f"find {path} -type d -empty 2>/dev/null", f"Empty Directories in {path}")
            elif choice == '7':
                pattern = input("Enter filename pattern: ").strip()
                path = input("Enter path to search (default: .): ").strip() or "."
                if pattern:
                    self.run_command(f"find {path} -name '*{pattern}*' -type f 2>/dev/null", f"Files matching '{pattern}' in {path}")
            elif choice == '8':
                path = input("Enter path to list (default: .): ").strip() or "."
                self.run_command(f"ls -la {path}", f"All Files (including hidden) in {path}")
            elif choice == '0':
                break

    def network_tools_menu(self):
        """Network tools submenu"""
        while True:
            self.print_header()
            print("🌐 NETWORK TOOLS")
            print("-" * 30)
            print("1. Network Interfaces")
            print("2. Active Connections")
            print("3. Listening Ports")
            print("4. Ping Test")
            print("5. Traceroute")
            print("6. DNS Lookup")
            print("7. Port Scan")
            print("8. Network Statistics")
            print("0. Back to Main Menu")

            choice = input("\n👉 Select option: ").strip()

            if choice == '1':
                self.run_command("ip addr show && echo '' && route -n", "Network Interfaces")
            elif choice == '2':
                self.run_command("netstat -tuln", "Active Network Connections")
            elif choice == '3':
                self.run_command("netstat -tlnp", "Listening Ports")
            elif choice == '4':
                host = input("Enter hostname/IP to ping: ").strip()
                if host:
                    self.run_command(f"ping -c 4 {host}", f"Ping Test to {host}")
            elif choice == '5':
                host = input("Enter hostname/IP to trace: ").strip()
                if host:
                    self.run_command(f"traceroute {host} 2>/dev/null || tracert {host}", f"Traceroute to {host}")
            elif choice == '6':
                domain = input("Enter domain to lookup: ").strip()
                if domain:
                    self.run_command(f"nslookup {domain}", f"DNS Lookup for {domain}")
            elif choice == '7':
                host = input("Enter hostname/IP to scan: ").strip()
                if host:
                    self.run_command(f"nmap -F {host} 2>/dev/null || echo 'nmap not available'", f"Port Scan of {host}")
            elif choice == '8':
                self.run_command("netstat -s", "Network Statistics")
            elif choice == '0':
                break

    def user_management_menu(self):
        """User management submenu"""
        while True:
            self.print_header()
            print("👥 USER MANAGEMENT")
            print("-" * 30)
            print("1. List All Users")
            print("2. Currently Logged Users")
            print("3. User Groups")
            print("4. Check User Info")
            print("5. Last Logins")
            print("6. Failed Login Attempts")
            print("7. Password Policies")
            print("0. Back to Main Menu")

            choice = input("\n👉 Select option: ").strip()

            if choice == '1':
                self.run_command("cat /etc/passwd | awk -F: '{print $1, $3, $5}' | column -t", "All System Users")
            elif choice == '2':
                self.run_command("who && echo '' && w", "Currently Logged Users")
            elif choice == '3':
                self.run_command("cat /etc/group", "User Groups")
            elif choice == '4':
                username = input("Enter username: ").strip()
                if username:
                    self.run_command(f"id {username} && finger {username} 2>/dev/null", f"User Info for {username}")
            elif choice == '5':
                self.run_command("last -n 20", "Recent Login History")
            elif choice == '6':
                self.run_command("grep 'Failed password' /var/log/auth.log 2>/dev/null | tail -20 || echo 'No auth logs accessible'", "Failed Login Attempts")
            elif choice == '7':
                self.run_command("chage -l $(whoami) 2>/dev/null || echo 'Password policy info not accessible'", "Password Policy Info")
            elif choice == '0':
                break

    def package_management_menu(self):
        """Package management submenu"""
        while True:
            self.print_header()
            print("📦 PACKAGE MANAGEMENT")
            print("-" * 30)
            print("1. Update Package Lists")
            print("2. Upgrade System")
            print("3. Installed Packages")
            print("4. Search Package")
            print("5. Install Package")
            print("6. Remove Package")
            print("7. Package Info")
            print("8. Clean Package Cache")
            print("0. Back to Main Menu")

            choice = input("\n👉 Select option: ").strip()

            if choice == '1':
                self.run_command("sudo apt update || sudo yum check-update || sudo pacman -Sy", "Updating Package Lists")
            elif choice == '2':
                print("⚠️  This will upgrade all packages. Continue? (y/N)")
                confirm = input().strip().lower()
                if confirm == 'y':
                    self.run_command("sudo apt upgrade || sudo yum update || sudo pacman -Su", "System Upgrade")
            elif choice == '3':
                self.run_command("dpkg -l | head -50 || rpm -qa | head -50 || pacman -Q | head -50", "Installed Packages (first 50)")
            elif choice == '4':
                package = input("Enter package name to search: ").strip()
                if package:
                    self.run_command(f"apt search {package} || yum search {package} || pacman -Ss {package}", f"Searching for {package}")
            elif choice == '5':
                package = input("Enter package name to install: ").strip()
                if package:
                    self.run_command(f"sudo apt install {package} || sudo yum install {package} || sudo pacman -S {package}", f"Installing {package}")
            elif choice == '6':
                package = input("Enter package name to remove: ").strip()
                if package:
                    self.run_command(f"sudo apt remove {package} || sudo yum remove {package} || sudo pacman -R {package}", f"Removing {package}")
            elif choice == '7':
                package = input("Enter package name for info: ").strip()
                if package:
                    self.run_command(f"apt show {package} || yum info {package} || pacman -Qi {package}", f"Package Info for {package}")
            elif choice == '8':
                self.run_command("sudo apt autoremove && sudo apt autoclean || sudo yum clean all || sudo pacman -Sc", "Cleaning Package Cache")
            elif choice == '0':
                break

    def custom_commands_menu(self):
        """Custom commands submenu"""
        while True:
            self.print_header()
            print("🔧 CUSTOM COMMANDS")
            print("-" * 30)

            # Display existing custom commands
            if self.config['custom_commands']:
                print("Saved Commands:")
                for i, (name, cmd) in enumerate(self.config['custom_commands'].items(), 1):
                    print(f"{i}. {name}")
                print()

            print("a. Add Custom Command")
            print("r. Remove Custom Command")
            print("e. Execute Custom Command")
            print("0. Back to Main Menu")

            choice = input("\n👉 Select option: ").strip().lower()

            if choice == 'a':
                name = input("Enter command name: ").strip()
                cmd = input("Enter command: ").strip()
                if name and cmd:
                    self.config['custom_commands'][name] = cmd
                    self.save_config()
                    print(f"✅ Added command '{name}'")
                    input("Press Enter to continue...")

            elif choice == 'r':
                if self.config['custom_commands']:
                    name = input("Enter command name to remove: ").strip()
                    if name in self.config['custom_commands']:
                        del self.config['custom_commands'][name]
                        self.save_config()
                        print(f"✅ Removed command '{name}'")
                    else:
                        print(f"❌ Command '{name}' not found")
                    input("Press Enter to continue...")
                else:
                    print("No custom commands to remove")
                    input("Press Enter to continue...")

            elif choice == 'e':
                if self.config['custom_commands']:
                    name = input("Enter command name to execute: ").strip()
                    if name in self.config['custom_commands']:
                        self.run_command(self.config['custom_commands'][name], f"Executing: {name}")
                    else:
                        print(f"❌ Command '{name}' not found")
                        input("Press Enter to continue...")
                else:
                    print("No custom commands available")
                    input("Press Enter to continue...")

            elif choice == '0':
                break

    def monitoring_tools_menu(self):
        """Advanced monitoring tools submenu"""
        while True:
            self.print_header()
            print("📊 MONITORING TOOLS")
            print("-" * 30)
            print("1. 🌐 Network Monitor - Check IPs & DNS")
            print("2. 🌤️  Weather Checker")
            print("3. 📈 Stock Market Monitor")
            print("4. 🛡️  Security Audit")
            print("5. 🩺 System Health Check")
            print("6. 🧹 System Cleanup")
            print("7. 🔍 Advanced Network Diagnostics")
            print("0. Back to Main Menu")

            choice = input("\n👉 Select option: ").strip()

            if choice == '1':
                self.network_monitor_menu()
            elif choice == '2':
                self.weather_checker_menu()
            elif choice == '3':
                self.stock_monitor_menu()
            elif choice == '4':
                self.run_command(f"bash {os.path.join(self.scripts_dir, 'security_audit.sh')}", "Security Audit")
            elif choice == '5':
                self.run_command(f"bash {os.path.join(self.scripts_dir, 'system_health.sh')}", "System Health Check")
            elif choice == '6':
                confirm = input("⚠️  Run system cleanup? This will clean temp files and cache (y/N): ").strip().lower()
                if confirm == 'y':
                    self.run_command(f"bash {os.path.join(self.scripts_dir, 'cleanup_system.sh')}", "System Cleanup")
            elif choice == '7':
                self.run_command(f"bash {os.path.join(self.scripts_dir, 'network_diagnostics.sh')}", "Network Diagnostics")
            elif choice == '0':
                break

    def network_monitor_menu(self):
        """Network monitoring submenu"""
        while True:
            self.print_header()
            print("🌐 NETWORK MONITOR")
            print("-" * 25)
            print("1. Monitor All Hosts")
            print("2. Monitor Hosts (Live)")
            print("3. Test DNS Servers")
            print("4. Network Summary")
            print("5. List Configured Hosts")
            print("6. Add Host")
            print("7. Remove Host")
            print("0. Back to Monitoring Menu")

            choice = input("\n👉 Select option: ").strip()

            if choice == '1':
                self.run_command(f"python3 {os.path.join(self.scripts_dir, 'network_monitor.py')} hosts", "Network Host Monitoring")
            elif choice == '2':
                print("Starting live monitoring... Press Ctrl+C to stop")
                self.run_command(f"python3 {os.path.join(self.scripts_dir, 'network_monitor.py')} hosts-watch", "Live Network Monitoring")
            elif choice == '3':
                self.run_command(f"python3 {os.path.join(self.scripts_dir, 'network_monitor.py')} dns", "DNS Server Testing")
            elif choice == '4':
                self.run_command(f"python3 {os.path.join(self.scripts_dir, 'network_monitor.py')} summary", "Network Summary")
            elif choice == '5':
                self.run_command(f"python3 {os.path.join(self.scripts_dir, 'network_monitor.py')} list", "Configured Hosts")
            elif choice == '6':
                name = input("Enter host name: ").strip()
                address = input("Enter IP/domain: ").strip()
                host_type = input("Enter type (ip/domain) [ip]: ").strip() or "ip"
                if name and address:
                    self.run_command(f"python3 {os.path.join(self.scripts_dir, 'network_monitor.py')} add '{name}' {address} {host_type}", f"Adding {name}")
            elif choice == '7':
                name = input("Enter host name to remove: ").strip()
                if name:
                    self.run_command(f"python3 {os.path.join(self.scripts_dir, 'network_monitor.py')} remove '{name}'", f"Removing {name}")
            elif choice == '0':
                break

    def weather_checker_menu(self):
        """Weather checker submenu"""
        while True:
            self.print_header()
            print("🌤️  WEATHER CHECKER")
            print("-" * 25)
            print("1. Check All Locations")
            print("2. Check Specific Location")
            print("3. Quick Weather")
            print("4. List Configured Locations")
            print("5. Add Location")
            print("6. Remove Location")
            print("0. Back to Monitoring Menu")

            choice = input("\n👉 Select option: ").strip()

            if choice == '1':
                self.run_command(f"python3 {os.path.join(self.scripts_dir, 'weather_check.py')} all", "Weather Check - All Locations")
            elif choice == '2':
                location = input("Enter location name: ").strip()
                if location:
                    self.run_command(f"python3 {os.path.join(self.scripts_dir, 'weather_check.py')} '{location}'", f"Weather for {location}")
            elif choice == '3':
                location = input("Enter location name: ").strip()
                if location:
                    self.run_command(f"python3 {os.path.join(self.scripts_dir, 'weather_check.py')} quick '{location}'", f"Quick Weather for {location}")
            elif choice == '4':
                self.run_command(f"python3 {os.path.join(self.scripts_dir, 'weather_check.py')} list", "Configured Locations")
            elif choice == '5':
                name = input("Enter location name: ").strip()
                country = input("Enter country code (optional): ").strip()
                if name:
                    cmd = f"python3 {os.path.join(self.scripts_dir, 'weather_check.py')} add '{name}'"
                    if country:
                        cmd += f" {country}"
                    self.run_command(cmd, f"Adding {name}")
            elif choice == '6':
                name = input("Enter location name to remove: ").strip()
                if name:
                    self.run_command(f"python3 {os.path.join(self.scripts_dir, 'weather_check.py')} remove '{name}'", f"Removing {name}")
            elif choice == '0':
                break

    def stock_monitor_menu(self):
        """Stock monitoring submenu"""
        while True:
            self.print_header()
            print("📈 STOCK MONITOR")
            print("-" * 20)
            print("1. Monitor Watchlist")
            print("2. Live Monitoring")
            print("3. Check Single Stock")
            print("4. Market Summary")
            print("5. List Watchlist")
            print("6. Add to Watchlist")
            print("7. Remove from Watchlist")
            print("8. Set Price Alert")
            print("0. Back to Monitoring Menu")

            choice = input("\n👉 Select option: ").strip()

            if choice == '1':
                self.run_command(f"python3 {os.path.join(self.scripts_dir, 'stock_monitor.py')} watch", "Stock Watchlist Monitor")
            elif choice == '2':
                print("Starting live monitoring... Press Ctrl+C to stop")
                self.run_command(f"python3 {os.path.join(self.scripts_dir, 'stock_monitor.py')} watch-live", "Live Stock Monitoring")
            elif choice == '3':
                symbol = input("Enter stock symbol (e.g., AAPL): ").strip().upper()
                if symbol:
                    self.run_command(f"python3 {os.path.join(self.scripts_dir, 'stock_monitor.py')} {symbol}", f"Stock Data for {symbol}")
            elif choice == '4':
                self.run_command(f"python3 {os.path.join(self.scripts_dir, 'stock_monitor.py')} market", "Market Summary")
            elif choice == '5':
                self.run_command(f"python3 {os.path.join(self.scripts_dir, 'stock_monitor.py')} list", "Stock Watchlist")
            elif choice == '6':
                symbol = input("Enter stock symbol: ").strip().upper()
                name = input("Enter company name (optional): ").strip()
                if symbol:
                    cmd = f"python3 {os.path.join(self.scripts_dir, 'stock_monitor.py')} add {symbol}"
                    if name:
                        cmd += f" '{name}'"
                    self.run_command(cmd, f"Adding {symbol} to Watchlist")
            elif choice == '7':
                symbol = input("Enter stock symbol to remove: ").strip().upper()
                if symbol:
                    self.run_command(f"python3 {os.path.join(self.scripts_dir, 'stock_monitor.py')} remove {symbol}", f"Removing {symbol}")
            elif choice == '8':
                symbol = input("Enter stock symbol: ").strip().upper()
                alert_type = input("Enter alert type (high/low): ").strip().lower()
                price = input("Enter alert price: ").strip()
                if symbol and alert_type in ['high', 'low'] and price:
                    self.run_command(f"python3 {os.path.join(self.scripts_dir, 'stock_monitor.py')} alert {symbol} {alert_type} {price}", f"Setting {alert_type} alert for {symbol}")
            elif choice == '0':
                break

    def main_menu(self):
        """Main dashboard menu"""
        while True:
            self.print_header()
            print("🎯 MAIN MENU")
            print("-" * 30)
            print("1. 🔍 System Monitoring")
            print("2. ⚙️  Service Management")
            print("3. 📁 File Operations")
            print("4. 🌐 Network Tools")
            print("5. 👥 User Management")
            print("6. 📦 Package Management")
            print("7. 🔧 Custom Commands")
            print("8. 📊 Monitoring Tools")
            print("9. ⚡ Emergency Commands")
            print("q. 📈 Quick System Overview")
            print("0. Exit Dashboard")

            choice = input("\n👉 Select option: ").strip().lower()

            if choice == '1':
                self.system_monitoring_menu()
            elif choice == '2':
                self.service_management_menu()
            elif choice == '3':
                self.file_operations_menu()
            elif choice == '4':
                self.network_tools_menu()
            elif choice == '5':
                self.user_management_menu()
            elif choice == '6':
                self.package_management_menu()
            elif choice == '7':
                self.custom_commands_menu()
            elif choice == '8':
                self.monitoring_tools_menu()
            elif choice == '9':
                self.emergency_menu()
            elif choice == 'q':
                self.run_command("uptime && free -h && df -h / && who", "Quick System Overview")
            elif choice == '0':
                self.config['last_run'] = datetime.now().isoformat()
                self.save_config()
                print("\n👋 Goodbye! Dashboard session saved.")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def emergency_menu(self):
        """Emergency commands submenu"""
        while True:
            self.print_header()
            print("⚡ EMERGENCY COMMANDS")
            print("-" * 30)
            print("⚠️  WARNING: These commands can affect system stability!")
            print()
            print("1. Kill Process by PID")
            print("2. Kill Process by Name")
            print("3. Force Unmount Directory")
            print("4. Clear System Cache")
            print("5. Emergency Disk Space")
            print("6. Reset Network Interface")
            print("7. Check System Integrity")
            print("0. Back to Main Menu")

            choice = input("\n👉 Select option (proceed with caution): ").strip()

            if choice == '1':
                pid = input("Enter Process ID to kill: ").strip()
                if pid.isdigit():
                    confirm = input(f"⚠️  Really kill process {pid}? (y/N): ").strip().lower()
                    if confirm == 'y':
                        self.run_command(f"sudo kill -9 {pid}", f"Force killing process {pid}")
            elif choice == '2':
                name = input("Enter process name to kill: ").strip()
                if name:
                    confirm = input(f"⚠️  Really kill all '{name}' processes? (y/N): ").strip().lower()
                    if confirm == 'y':
                        self.run_command(f"sudo pkill -f {name}", f"Killing processes matching '{name}'")
            elif choice == '3':
                mount_point = input("Enter mount point to force unmount: ").strip()
                if mount_point:
                    confirm = input(f"⚠️  Force unmount {mount_point}? (y/N): ").strip().lower()
                    if confirm == 'y':
                        self.run_command(f"sudo umount -f {mount_point}", f"Force unmounting {mount_point}")
            elif choice == '4':
                confirm = input("⚠️  Clear system cache? (y/N): ").strip().lower()
                if confirm == 'y':
                    self.run_command("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'", "Clearing System Cache")
            elif choice == '5':
                self.run_command("df -h && echo '' && sudo du -sh /var/log /tmp /var/cache 2>/dev/null", "Emergency Disk Space Check")
            elif choice == '6':
                interface = input("Enter network interface (e.g., eth0): ").strip()
                if interface:
                    confirm = input(f"⚠️  Reset network interface {interface}? (y/N): ").strip().lower()
                    if confirm == 'y':
                        self.run_command(f"sudo ifdown {interface} && sudo ifup {interface}", f"Resetting interface {interface}")
            elif choice == '7':
                self.run_command("dmesg | tail -50", "Recent Kernel Messages")
            elif choice == '0':
                break

def main():
    """Main function"""
    try:
        dashboard = AdminDashboard()
        dashboard.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()