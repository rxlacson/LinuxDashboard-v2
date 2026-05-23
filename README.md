# Linux Admin Dashboard

A comprehensive terminal-based dashboard for daily Linux administration tasks.

## Features

### 🔍 System Monitoring
- System overview and information
- CPU and memory usage monitoring
- Disk usage analysis
- Network status checking
- Process monitoring
- System logs viewing
- Uptime and load averages
- Temperature sensors

### ⚙️ Service Management
- List all services
- View active/failed services
- Start, stop, restart services
- Check service status
- Enable/disable services at boot

### 📁 File Operations
- Find large files
- Clean temporary files
- Find recently modified files
- Analyze disk usage by directory
- Count files by type
- Find empty directories
- Search files by name
- Show hidden files

### 🌐 Network Tools
- View network interfaces
- Monitor active connections
- Check listening ports
- Ping tests
- Traceroute
- DNS lookups
- Port scanning
- Network statistics

### 👥 User Management
- List all users
- View currently logged users
- Manage user groups
- Check user information
- View login history
- Monitor failed login attempts
- Check password policies

### 📦 Package Management
- Update package lists
- Upgrade system packages
- List installed packages
- Search for packages
- Install/remove packages
- View package information
- Clean package cache

### 🔧 Custom Commands
- Save frequently used commands
- Execute saved commands
- Manage custom command library

### 📊 Monitoring Tools
- **Network Monitor**: Monitor multiple IP addresses and DNS servers with real-time connectivity testing
- **Weather Checker**: Get current weather information for multiple locations
- **Stock Market Monitor**: Real-time stock monitoring with price alerts and watchlists
- **Security Audit**: Comprehensive security assessment scripts
- **System Health**: Complete system health diagnostics
- **System Cleanup**: Automated cleanup of temporary files and caches

### ⚡ Emergency Commands
- Kill processes by PID or name
- Force unmount directories
- Clear system cache
- Emergency disk space check
- Reset network interfaces
- Check system integrity

## Quick Start

1. **Run the dashboard:**
   ```bash
   ./run_dashboard.sh
   ```

2. **Or run directly:**
   ```bash
   python3 admin_dashboard.py
   ```

## File Structure

```
.
├── admin_dashboard.py      # Main dashboard application
├── run_dashboard.sh       # Launcher script
├── README.md             # This file
├── dashboard_config.json # Configuration (auto-created)
└── dashboard_scripts/    # Helper scripts
    ├── system_health.sh
    ├── network_diagnostics.sh
    ├── cleanup_system.sh
    ├── security_audit.sh
    ├── network_monitor.py    # Network monitoring tool
    ├── weather_check.py      # Weather checker tool  
    ├── stock_monitor.py      # Stock market monitor
    ├── network_config.json   # Network monitoring config
    ├── weather_config.json   # Weather checker config
    └── stock_config.json     # Stock monitor config
```

## Requirements

- Python 3.x
- Bash shell
- Standard Linux utilities (ps, netstat, df, etc.)
- sudo access for administrative commands

## Usage Tips

1. **Navigation:** Use number keys to select menu options
2. **Safety:** Emergency commands require confirmation
3. **Persistence:** Custom commands are saved between sessions
4. **Configuration:** Settings are automatically saved in `dashboard_config.json`

## Supported Systems

- Ubuntu/Debian (APT package manager)
- RHEL/CentOS/Fedora (YUM/DNF package manager)
- Arch Linux (Pacman package manager)
- Most Linux distributions with standard utilities

## Security Notes

- Always review commands before execution
- Emergency commands can affect system stability
- Use sudo responsibly
- Monitor failed login attempts regularly
- Keep the system updated

## Customization

You can add your own commands to the "Custom Commands" section or modify the scripts in the `dashboard_scripts/` directory to suit your needs.

## Troubleshooting

If you encounter permission issues:
```bash
# Make scripts executable
chmod +x *.sh dashboard_scripts/*.sh

# Check Python availability
python3 --version
```

## Contributing

Feel free to enhance the dashboard by:
- Adding new menu sections
- Creating additional helper scripts
- Improving error handling
- Adding new administrative tasks

---

**Warning:** This dashboard provides access to powerful system commands. Always understand what a command does before executing it, especially in the Emergency Commands section.