#!/usr/bin/env python3
"""
Network Monitor Script
Monitors multiple IP addresses and DNS servers for connectivity and response time
"""

import subprocess
import socket
import time
import sys
from datetime import datetime
import json
import os

class NetworkMonitor:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'network_config.json')
        self.load_config()

    def load_config(self):
        """Load network monitoring configuration"""
        default_config = {
            "hosts": [
                {"name": "Google DNS", "address": "8.8.8.8", "type": "ip"},
                {"name": "Cloudflare DNS", "address": "1.1.1.1", "type": "ip"},
                {"name": "Google", "address": "google.com", "type": "domain"},
                {"name": "GitHub", "address": "github.com", "type": "domain"},
                {"name": "Stack Overflow", "address": "stackoverflow.com", "type": "domain"}
            ],
            "dns_servers": [
                {"name": "Google DNS", "server": "8.8.8.8"},
                {"name": "Cloudflare DNS", "server": "1.1.1.1"},
                {"name": "OpenDNS", "server": "208.67.222.222"}
            ],
            "timeout": 3,
            "test_domain": "google.com"
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
                self.save_config()
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

    def ping_host(self, host, timeout=3):
        """Ping a host and return response time"""
        try:
            # Use ping command
            cmd = f"ping -c 1 -W {timeout} {host}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                # Parse response time from ping output
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'time=' in line:
                        time_part = line.split('time=')[1].split()[0]
                        return float(time_part.replace('ms', ''))
                return 0.0  # Success but couldn't parse time
            else:
                return None  # Failed
        except:
            return None

    def check_dns_resolution(self, domain, dns_server):
        """Check DNS resolution using specific DNS server"""
        try:
            cmd = f"nslookup {domain} {dns_server}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)

            if result.returncode == 0 and "NXDOMAIN" not in result.stdout:
                # Extract response time or IP
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Address:' in line and '#' not in line:
                        ip = line.split('Address:')[1].strip()
                        if ip and ip != dns_server:
                            return ip
                return "Resolved"
            else:
                return None
        except:
            return None

    def test_port_connectivity(self, host, port, timeout=3):
        """Test if a specific port is open on a host"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            start_time = time.time()
            result = sock.connect_ex((host, port))
            end_time = time.time()

            sock.close()

            if result == 0:
                return round((end_time - start_time) * 1000, 2)  # Return time in ms
            else:
                return None
        except:
            return None

    def monitor_hosts(self, continuous=False):
        """Monitor configured hosts"""
        print("🌐 NETWORK HOST MONITORING")
        print("=" * 50)

        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n📅 Scan Time: {timestamp}")
            print("-" * 50)

            for host_info in self.config['hosts']:
                name = host_info['name']
                address = host_info['address']
                host_type = host_info['type']

                print(f"📍 {name} ({address})")

                # Ping test
                ping_time = self.ping_host(address, self.config['timeout'])
                if ping_time is not None:
                    if ping_time > 0:
                        status = "🟢" if ping_time < 100 else "🟡" if ping_time < 500 else "🔴"
                        print(f"   Ping: {status} {ping_time:.1f}ms")
                    else:
                        print(f"   Ping: 🟢 Reachable")
                else:
                    print(f"   Ping: 🔴 Unreachable")

                # Additional tests for domains
                if host_type == 'domain':
                    # HTTP connectivity test
                    http_time = self.test_port_connectivity(address, 80, self.config['timeout'])
                    https_time = self.test_port_connectivity(address, 443, self.config['timeout'])

                    if http_time is not None:
                        print(f"   HTTP:  🟢 {http_time}ms")
                    else:
                        print(f"   HTTP:  🔴 No response")

                    if https_time is not None:
                        print(f"   HTTPS: 🟢 {https_time}ms")
                    else:
                        print(f"   HTTPS: 🔴 No response")

            if not continuous:
                break

            time.sleep(10)  # Wait 10 seconds between scans

    def monitor_dns_servers(self):
        """Monitor DNS server performance"""
        print("🔍 DNS SERVER MONITORING")
        print("=" * 50)

        test_domain = self.config['test_domain']
        print(f"Testing resolution of: {test_domain}\n")

        for dns_info in self.config['dns_servers']:
            name = dns_info['name']
            server = dns_info['server']

            print(f"📡 {name} ({server})")

            # Test DNS resolution
            start_time = time.time()
            resolved = self.check_dns_resolution(test_domain, server)
            end_time = time.time()

            if resolved:
                response_time = round((end_time - start_time) * 1000, 1)
                status = "🟢" if response_time < 100 else "🟡" if response_time < 500 else "🔴"
                print(f"   Resolution: {status} {response_time}ms")
                print(f"   Result: {resolved}")
            else:
                print(f"   Resolution: 🔴 Failed")

            # Test DNS server connectivity
            ping_time = self.ping_host(server, self.config['timeout'])
            if ping_time is not None:
                status = "🟢" if ping_time < 50 else "🟡" if ping_time < 200 else "🔴"
                print(f"   Ping: {status} {ping_time:.1f}ms")
            else:
                print(f"   Ping: 🔴 Unreachable")

            print()

    def network_summary(self):
        """Provide a quick network summary"""
        print("📊 NETWORK SUMMARY")
        print("=" * 30)

        total_hosts = len(self.config['hosts'])
        reachable_hosts = 0

        for host_info in self.config['hosts']:
            if self.ping_host(host_info['address'], 2) is not None:
                reachable_hosts += 1

        print(f"Total hosts monitored: {total_hosts}")
        print(f"Reachable hosts: {reachable_hosts}")
        print(f"Unreachable hosts: {total_hosts - reachable_hosts}")

        if reachable_hosts == total_hosts:
            print("Status: 🟢 All hosts reachable")
        elif reachable_hosts > total_hosts * 0.7:
            print("Status: 🟡 Most hosts reachable")
        else:
            print("Status: 🔴 Many hosts unreachable")

    def add_host(self, name, address, host_type='ip'):
        """Add a new host to monitor"""
        new_host = {
            "name": name,
            "address": address,
            "type": host_type
        }
        self.config['hosts'].append(new_host)
        self.save_config()
        print(f"✅ Added {name} ({address}) to monitoring list")

    def remove_host(self, name):
        """Remove a host from monitoring"""
        self.config['hosts'] = [h for h in self.config['hosts'] if h['name'] != name]
        self.save_config()
        print(f"✅ Removed {name} from monitoring list")

    def list_hosts(self):
        """List all configured hosts"""
        print("📋 CONFIGURED HOSTS")
        print("=" * 30)
        for i, host in enumerate(self.config['hosts'], 1):
            print(f"{i}. {host['name']} - {host['address']} ({host['type']})")

def main():
    if len(sys.argv) < 2:
        print("🌐 Network Monitor Tool")
        print("Usage:")
        print("  python3 network_monitor.py hosts          - Monitor all hosts once")
        print("  python3 network_monitor.py hosts-watch    - Monitor hosts continuously")
        print("  python3 network_monitor.py dns            - Test DNS servers")
        print("  python3 network_monitor.py summary        - Quick network summary")
        print("  python3 network_monitor.py list           - List configured hosts")
        print("  python3 network_monitor.py add <name> <address> [type] - Add host")
        print("  python3 network_monitor.py remove <name>  - Remove host")
        return

    monitor = NetworkMonitor()
    command = sys.argv[1].lower()

    try:
        if command == 'hosts':
            monitor.monitor_hosts(continuous=False)
        elif command == 'hosts-watch':
            print("Press Ctrl+C to stop continuous monitoring...")
            monitor.monitor_hosts(continuous=True)
        elif command == 'dns':
            monitor.monitor_dns_servers()
        elif command == 'summary':
            monitor.network_summary()
        elif command == 'list':
            monitor.list_hosts()
        elif command == 'add' and len(sys.argv) >= 4:
            name = sys.argv[2]
            address = sys.argv[3]
            host_type = sys.argv[4] if len(sys.argv) > 4 else 'ip'
            monitor.add_host(name, address, host_type)
        elif command == 'remove' and len(sys.argv) >= 3:
            name = sys.argv[2]
            monitor.remove_host(name)
        else:
            print("❌ Invalid command or missing parameters")

    except KeyboardInterrupt:
        print("\n\n👋 Network monitoring stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()