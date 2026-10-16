import time
import os
import csv
import yfinance as yf
from datetime import datetime

# Customize your watchlist here
WATCHLIST = ["AMD", "NVDA", "VXUS", "FXAIX", "SCHD", "TSLA", "VFORX"]
REFRESH_INTERVAL = 45  # Time in seconds between updates
CSV_FILE_NAME = "portfolio_history.csv"
DEFAULT_GRAPH_TICKER = "AMD"  # Locked default chart ticker

# ANSI Escape Sequences for Windows 11 Terminal Formatting
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW = "\033[33m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pad_ansi(text, visible_width):
    actual_len = 0
    in_escape = False
    for char in text:
        if char == '\033':
            in_escape = True
        elif in_escape and char == 'm':
            in_escape = False
            continue
        if not in_escape:
            actual_len += 1
    padding_needed = max(0, visible_width - actual_len)
    return text + (" " * padding_needed)

def format_large_number(number):
    if number is None:
        return "N/A"
    try:
        num = float(number)
        if num >= 1e12: return f"${num / 1e12:.2f}T"
        if num >= 1e9:  return f"${num / 1e9:.2f}B"
        if num >= 1e6:  return f"${num / 1e6:.2f}M"
        return f"${num:,.2f}"
    except Exception:
        return "N/A"

def format_price(price):
    return f"${price:.2f}" if price is not None else "N/A"

def generate_range_slider(current, low, high, width=10):
    if None in (current, low, high) or low == high:
        return "[  N/A  ]"
    current = max(low, min(high, current))
    position = int(((current - low) / (high - low)) * (width - 1))
    slider = ["-"] * width
    slider[position] = f"{YELLOW}*{RESET}{CYAN}"
    return f"[{''.join(slider)}]"

def log_portfolio_to_csv(snapshot_data):
    file_exists = os.path.isfile(CSV_FILE_NAME)
    try:
        with open(CSV_FILE_NAME, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Ticker", "Price", "Net Change", "% Change", "Day Low", "Day High", "Net Asset or Cap"])
            for row in snapshot_data:
                writer.writerow(row)
    except Exception:
        pass

def draw_pure_python_chart(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d", interval="15m", timeout=5)
        if hist.empty:
            hist = stock.history(period="1mo", interval="1d", timeout=5)
            
        if hist.empty:
            print(f"\n[ No chart data found for {ticker} ]")
            return

        prices = hist['Close'].dropna().tolist()
        if len(prices) < 2:
            return

        max_points = 50
        if len(prices) > max_points:
            step = len(prices) / max_points
            prices = [prices[int(i * step)] for i in range(max_points)]

        min_p, max_p = min(prices), max(prices)
        price_range = max_p - min_p if max_p != min_p else 1.0
        
        height = 5
        print(f"\n{CYAN}--- {ticker} Modern Price Trend (Historical Window) ---{RESET}".center(125))
        print(f"High: ${max_p:.2f}".rjust(105))
        
        for r in range(height - 1, -1, -1):
            row_str = ""
            for p in prices:
                normalized_val = ((p - min_p) / price_range) * (height - 1)
                if round(normalized_val) == r:
                    row_str += "📈" if r > height//2 else "📊"
                elif round(normalized_val) > r:
                    row_str += "│"
                else:
                    row_str += " "
            print(f"   {row_str}")
            
        print(f"Low:  ${min_p:.2f}".rjust(105))
    except Exception:
        pass

def main():
    prev_prices = {ticker: None for ticker in WATCHLIST}
    last_csv_log_time = None
    
    print("Connecting to live data pipes...")
    time.sleep(1)

    while True:
        try:
            now_dt = datetime.now()
            now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
            
            output_lines = []
            current_loop_snapshot = []

            for ticker in WATCHLIST:
                try:
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period="1d", timeout=5)
                    
                    if hist.empty or len(hist) == 0:
                        hist = stock.history(period="5d", timeout=5)
                        
                    if hist.empty:
                        info_data = stock.info
                        current_price = info_data.get('navPrice') or info_data.get('previousClose')
                        day_low = info_data.get('dayLow') or current_price
                        day_high = info_data.get('dayHigh') or current_price
                        prev_close = info_data.get('previousClose') or current_price
                    else:
                        current_price = hist['Close'].dropna().iloc[-1]
                        day_low = hist['Low'].min()
                        day_high = hist['High'].max()
                        prev_close = hist['Open'].iloc[0] if len(hist) > 0 else current_price

                    if current_price is None:
                        raise ValueError("No price available")

                    net_asset_or_cap = None
                    try:
                        info = stock.info
                        net_asset_or_cap = info.get('totalAssets') or info.get('marketCap')
                    except Exception:
                        pass
                    
                    formatted_value = format_large_number(net_asset_or_cap)
                    
                    if prev_prices[ticker] is None:
                        trend = "⚪ FLAT"
                        ticker_display = f"{BOLD}{ticker}{RESET}"
                    elif current_price > prev_prices[ticker]:
                        trend = "🟢 UP"
                        ticker_display = f"{BOLD}{GREEN}{ticker}{RESET}"
                    elif current_price < prev_prices[ticker]:
                        trend = "🔴 DOWN"
                        ticker_display = f"{BOLD}{RED}{ticker}{RESET}"
                    else:
                        trend = "⚪ FLAT"
                        ticker_display = f"{BOLD}{ticker}{RESET}"
                    
                    session_diff = current_price - prev_close
                    session_pct = (session_diff / prev_close) * 100 if prev_close else 0.0

                    c_price_str = format_price(current_price)
                    d_low_str = format_price(day_low)
                    d_high_str = format_price(day_high)
                    
                    diff_sign = "+" if session_diff >= 0 else ""
                    session_diff_str = f"{diff_sign}{session_diff:.2f}"
                    session_pct_str = f"{diff_sign}{session_pct:.2f}%"
                    
                    current_loop_snapshot.append([
                        now_str, ticker, round(current_price, 2), f"{session_diff:+.2f}", f"{session_pct:+.2f}%",
                        f"{day_low:.2f}" if day_low else "N/A", f"{day_high:.2f}" if day_high else "N/A", formatted_value
                    ])

                    if session_diff > 0:
                        session_pct_str = f"{GREEN}{session_pct_str}{RESET}"
                    elif session_diff < 0:
                        session_pct_str = f"{RED}{session_pct_str}{RESET}"

                    slider_str = f"{CYAN}{generate_range_slider(current_price, day_low, day_high)}{RESET}"
                    
                    ticker_padded = pad_ansi(ticker_display, 8)
                    pct_padded = pad_ansi(session_pct_str, 8)
                    slider_padded = pad_ansi(slider_str, 12)
                    
                    output_lines.append(f"{ticker_padded} | {c_price_str:<9} | {trend:<7} | {session_diff_str:<9} | {pct_padded} | {d_low_str:<9} | {d_high_str:<9} | {slider_padded} | {formatted_value:<13}")
                    prev_prices[ticker] = current_price
                    
                except Exception:
                    error_ticker = pad_ansi(f"{BOLD}{ticker}{RESET}", 8)
                    output_lines.append(f"{error_ticker} | {'Error mapping mutual fund close values':<103}")

            # Draw Screen
            clear_screen()
            print(f"===================== Rex ® Work Week Live Market Watchlist Monitor 🐧 ({now_str}) =====================")
            print(f"{'Ticker':<8} | {'Price':<9} | {'Trend':<7} | {'Net Chg':<9} | {'% Chg':<8} | {'Day Low':<9} | {'Day High':<9} | {'Range Status':<12} | {'Net Asset/Cap':<13}")
            print("-" * 114)
            for line in output_lines:
                print(line)
            print("-" * 114)
            
            # CSV Hourly Logger Check
            current_hour = now_dt.hour
            if last_csv_log_time is None or last_csv_log_time != current_hour:
                log_portfolio_to_csv(current_loop_snapshot)
                last_csv_log_time = current_hour
                print(f"{GREEN}[ SYSTEM ]: CSV Snapshot logged successfully to '{CSV_FILE_NAME}'{RESET}")
            else:
                print(f"{CYAN}[ SYSTEM ]: Logging active. Next CSV snapshot scheduled on top of next hour.{RESET}")
            
            print("-" * 114)
            draw_pure_python_chart(DEFAULT_GRAPH_TICKER)
            print("-" * 114)
            print("Press Ctrl+C to stop monitoring.")
            time.sleep(REFRESH_INTERVAL)

        except KeyboardInterrupt:
            print("\nMonitor stopped.")
            break
        except Exception as e:
            print(f"\nUnexpected core execution error: {str(e)}")
            time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    main()
