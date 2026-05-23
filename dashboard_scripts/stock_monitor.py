#!/usr/bin/env python3
"""
Stock Market Monitor Script
Real-time stock market data monitoring and alerts
"""

import requests
import json
import sys
import os
import time
from datetime import datetime, timedelta

class StockMonitor:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'stock_config.json')
        self.load_config()

    def load_config(self):
        """Load stock monitoring configuration"""
        default_config = {
            "api_key": "",
            "watchlist": [
                {"symbol": "AAPL", "name": "Apple Inc.", "alert_high": 0, "alert_low": 0},
                {"symbol": "GOOGL", "name": "Alphabet Inc.", "alert_high": 0, "alert_low": 0},
                {"symbol": "MSFT", "name": "Microsoft Corp.", "alert_high": 0, "alert_low": 0},
                {"symbol": "TSLA", "name": "Tesla Inc.", "alert_high": 0, "alert_low": 0},
                {"symbol": "AMZN", "name": "Amazon.com Inc.", "alert_high": 0, "alert_low": 0}
            ],
            "refresh_interval": 60,
            "currency": "USD"
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

    def get_stock_data_free(self, symbol):
        """Get stock data using free Yahoo Finance API"""
        try:
            # Using Yahoo Finance API (free)
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return self.parse_yahoo_data(data, symbol)
            else:
                return None

        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def parse_yahoo_data(self, data, symbol):
        """Parse Yahoo Finance data"""
        try:
            chart = data['chart']['result'][0]
            meta = chart['meta']
            quote = chart['indicators']['quote'][0]

            # Current price
            current_price = meta.get('regularMarketPrice', 0)

            # Previous close
            previous_close = meta.get('previousClose', 0)

            # Calculate change
            change = current_price - previous_close
            change_percent = (change / previous_close * 100) if previous_close > 0 else 0

            # Get additional data
            day_high = meta.get('regularMarketDayHigh', 0)
            day_low = meta.get('regularMarketDayLow', 0)
            volume = meta.get('regularMarketVolume', 0)

            # Market state
            market_state = meta.get('marketState', 'UNKNOWN')

            return {
                'symbol': symbol,
                'name': meta.get('longName', symbol),
                'price': round(current_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'previous_close': round(previous_close, 2),
                'day_high': round(day_high, 2),
                'day_low': round(day_low, 2),
                'volume': volume,
                'market_state': market_state,
                'currency': meta.get('currency', 'USD'),
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }

        except Exception as e:
            print(f"Error parsing data for {symbol}: {e}")
            return None

    def display_stock_info(self, stock_data):
        """Display stock information"""
        if not stock_data:
            return

        # Choose emoji based on performance
        if stock_data['change'] > 0:
            emoji = "📈"
            change_color = "+"
        elif stock_data['change'] < 0:
            emoji = "📉"
            change_color = ""
        else:
            emoji = "➡️"
            change_color = ""

        print(f"{emoji} {stock_data['symbol']} - {stock_data['name']}")
        print(f"   💰 Price: ${stock_data['price']} {stock_data['currency']}")
        print(f"   📊 Change: {change_color}{stock_data['change']} ({change_color}{stock_data['change_percent']:.2f}%)")
        print(f"   📅 Previous: ${stock_data['previous_close']}")
        print(f"   🔺 Day High: ${stock_data['day_high']}")
        print(f"   🔻 Day Low: ${stock_data['day_low']}")
        print(f"   📦 Volume: {stock_data['volume']:,}")
        print(f"   🕐 Updated: {stock_data['timestamp']}")
        print(f"   🏢 Market: {stock_data['market_state']}")

    def monitor_watchlist(self, continuous=False):
        """Monitor all stocks in watchlist"""
        print("📊 STOCK MARKET MONITOR")
        print("=" * 40)

        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n📅 Update Time: {timestamp}")
            print("-" * 40)

            total_value = 0
            gainers = 0
            losers = 0

            for stock_info in self.config['watchlist']:
                symbol = stock_info['symbol']
                stock_data = self.get_stock_data_free(symbol)

                if stock_data:
                    self.display_stock_info(stock_data)

                    # Check alerts
                    self.check_alerts(stock_info, stock_data)

                    # Update counters
                    if stock_data['change'] > 0:
                        gainers += 1
                    elif stock_data['change'] < 0:
                        losers += 1

                    print()
                    time.sleep(1)  # Rate limiting

            # Display summary
            print("=" * 40)
            print(f"📈 Gainers: {gainers} | 📉 Losers: {losers} | ➡️ Flat: {len(self.config['watchlist']) - gainers - losers}")

            if not continuous:
                break

            print(f"\n⏰ Next update in {self.config['refresh_interval']} seconds...")
            time.sleep(self.config['refresh_interval'])

    def check_alerts(self, stock_info, stock_data):
        """Check price alerts"""
        symbol = stock_info['symbol']
        price = stock_data['price']
        alert_high = stock_info.get('alert_high', 0)
        alert_low = stock_info.get('alert_low', 0)

        if alert_high > 0 and price >= alert_high:
            print(f"   🚨 HIGH ALERT: {symbol} reached ${price} (target: ${alert_high})")

        if alert_low > 0 and price <= alert_low:
            print(f"   ⚠️  LOW ALERT: {symbol} dropped to ${price} (target: ${alert_low})")

    def get_single_stock(self, symbol):
        """Get data for a single stock"""
        stock_data = self.get_stock_data_free(symbol.upper())
        if stock_data:
            self.display_stock_info(stock_data)
        else:
            print(f"❌ Could not retrieve data for {symbol}")

    def add_to_watchlist(self, symbol, name="", alert_high=0, alert_low=0):
        """Add stock to watchlist"""
        symbol = symbol.upper()

        # Check if already exists
        for stock in self.config['watchlist']:
            if stock['symbol'] == symbol:
                print(f"📊 {symbol} is already in watchlist")
                return

        new_stock = {
            "symbol": symbol,
            "name": name or symbol,
            "alert_high": float(alert_high) if alert_high else 0,
            "alert_low": float(alert_low) if alert_low else 0
        }

        self.config['watchlist'].append(new_stock)
        self.save_config()
        print(f"✅ Added {symbol} to watchlist")

    def remove_from_watchlist(self, symbol):
        """Remove stock from watchlist"""
        symbol = symbol.upper()
        original_length = len(self.config['watchlist'])

        self.config['watchlist'] = [
            stock for stock in self.config['watchlist']
            if stock['symbol'] != symbol
        ]

        if len(self.config['watchlist']) < original_length:
            self.save_config()
            print(f"✅ Removed {symbol} from watchlist")
        else:
            print(f"❌ {symbol} not found in watchlist")

    def list_watchlist(self):
        """List all stocks in watchlist"""
        print("📋 STOCK WATCHLIST")
        print("=" * 30)

        if not self.config['watchlist']:
            print("No stocks in watchlist")
            return

        for i, stock in enumerate(self.config['watchlist'], 1):
            alerts = []
            if stock.get('alert_high', 0) > 0:
                alerts.append(f"H:${stock['alert_high']}")
            if stock.get('alert_low', 0) > 0:
                alerts.append(f"L:${stock['alert_low']}")

            alert_str = f" [{', '.join(alerts)}]" if alerts else ""
            print(f"{i}. {stock['symbol']} - {stock['name']}{alert_str}")

    def market_summary(self):
        """Get quick market summary"""
        print("🏛️  MARKET SUMMARY")
        print("=" * 25)

        # Major indices symbols
        indices = [
            {"symbol": "^GSPC", "name": "S&P 500"},
            {"symbol": "^DJI", "name": "Dow Jones"},
            {"symbol": "^IXIC", "name": "NASDAQ"},
            {"symbol": "^VIX", "name": "VIX (Fear Index)"}
        ]

        for index in indices:
            data = self.get_stock_data_free(index['symbol'])
            if data:
                change_emoji = "📈" if data['change'] > 0 else "📉" if data['change'] < 0 else "➡️"
                print(f"{change_emoji} {index['name']}: {data['price']} ({data['change']:+.2f})")
            else:
                print(f"❌ {index['name']}: Data unavailable")

    def set_alert(self, symbol, alert_type, price):
        """Set price alert for a stock"""
        symbol = symbol.upper()
        price = float(price)

        for stock in self.config['watchlist']:
            if stock['symbol'] == symbol:
                if alert_type.lower() == 'high':
                    stock['alert_high'] = price
                    print(f"✅ Set high alert for {symbol} at ${price}")
                elif alert_type.lower() == 'low':
                    stock['alert_low'] = price
                    print(f"✅ Set low alert for {symbol} at ${price}")
                else:
                    print("❌ Alert type must be 'high' or 'low'")
                    return

                self.save_config()
                return

        print(f"❌ {symbol} not found in watchlist. Add it first.")

def main():
    if len(sys.argv) < 2:
        print("📊 Stock Monitor Tool")
        print("Usage:")
        print("  python3 stock_monitor.py watch                     - Monitor watchlist once")
        print("  python3 stock_monitor.py watch-live               - Monitor continuously")
        print("  python3 stock_monitor.py <symbol>                 - Get single stock data")
        print("  python3 stock_monitor.py list                     - List watchlist")
        print("  python3 stock_monitor.py add <symbol> [name]      - Add to watchlist")
        print("  python3 stock_monitor.py remove <symbol>          - Remove from watchlist")
        print("  python3 stock_monitor.py alert <symbol> <high|low> <price> - Set alert")
        print("  python3 stock_monitor.py market                   - Market summary")
        print("\nExamples:")
        print("  python3 stock_monitor.py AAPL")
        print("  python3 stock_monitor.py add NVDA 'NVIDIA Corp'")
        print("  python3 stock_monitor.py alert TSLA high 250.00")
        return

    monitor = StockMonitor()
    command = sys.argv[1].lower()

    try:
        if command == 'watch':
            monitor.monitor_watchlist(continuous=False)
        elif command == 'watch-live':
            print("📊 Starting live stock monitoring...")
            print("Press Ctrl+C to stop")
            monitor.monitor_watchlist(continuous=True)
        elif command == 'list':
            monitor.list_watchlist()
        elif command == 'add' and len(sys.argv) >= 3:
            symbol = sys.argv[2]
            name = sys.argv[3] if len(sys.argv) > 3 else ""
            monitor.add_to_watchlist(symbol, name)
        elif command == 'remove' and len(sys.argv) >= 3:
            symbol = sys.argv[2]
            monitor.remove_from_watchlist(symbol)
        elif command == 'alert' and len(sys.argv) >= 5:
            symbol = sys.argv[2]
            alert_type = sys.argv[3]
            price = sys.argv[4]
            monitor.set_alert(symbol, alert_type, price)
        elif command == 'market':
            monitor.market_summary()
        else:
            # Treat as stock symbol
            monitor.get_single_stock(sys.argv[1])

    except KeyboardInterrupt:
        print("\n\n👋 Stock monitoring stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()