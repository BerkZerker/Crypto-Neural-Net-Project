import ccxt
import time
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.layout import Layout
from datetime import datetime
from pprint import pprint

def get_xrp_data(exchange):
    """Fetch XRP market data from the exchange"""
    try:
        ticker = exchange.fetch_ticker('XRP/USDT')
        orderbook = exchange.fetch_order_book('XRP/USDT')
        
        # Calculate spread
        bid = orderbook['bids'][0][0] if orderbook['bids'] else None
        ask = orderbook['asks'][0][0] if orderbook['asks'] else None
        spread = ask - bid if (bid and ask) else None
        spread_percent = (spread / bid * 100) if spread else None
        
        return {
            'last': ticker['last'],
            'high': ticker['high'],
            'low': ticker['low'],
            'volume': ticker['baseVolume'],
            'change_24h': ticker['percentage'],
            'bid': bid,
            'ask': ask,
            'spread': spread,
            'spread_percent': spread_percent
        }
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def create_price_history_chart(price_history, width=50, height=10):
    """Create ASCII chart from price history"""
    if not price_history:
        return "Insufficient data for chart"
    
    prices = [p['price'] for p in price_history]
    min_price = min(prices)
    max_price = max(prices)
    price_range = max_price - min_price
    
    if price_range == 0:
        price_range = 1  # Prevent division by zero
    
    chart = []
    for i in range(height):
        row = []
        level = max_price - (i * price_range / (height - 1))
        
        for price in prices:
            if price >= level:
                row.append('█')
            else:
                row.append(' ')
        chart.append(''.join(row))
    
    return '\n'.join(chart)

def format_number(number, decimals=8):
    """Format number with appropriate decimals"""
    if number is None:
        return "N/A"
    return f"{number:.{decimals}f}"

# def main():
#     # Initialize exchange
#     exchange = ccxt.binance()#{
#     #     'enableRateLimit': True,
#     # })
    
#     console = Console()
#     price_history = []
#     update_interval = 1 # seconds
    
#     with Live(console=console, refresh_per_second=1/5) as live:  # Update every 5 seconds
#         while True:
#             try:
#                 # Fetch new data
#                 data = get_xrp_data(exchange)
#                 if not data:
#                     continue
                
#                 # Update price history
#                 price_history.append({
#                     'timestamp': datetime.now(),
#                     'price': data['last']
#                 })
#                 # Keep last 50 price points
#                 price_history = price_history[-50:]
                
#                 # Create layout
#                 layout = Layout()
#                 layout.split_column(
#                     Layout(name="market_data"),
#                     Layout(name="chart", size=12)
#                 )
                
#                 # Create market data table
#                 table = Table(show_header=True, header_style="bold magenta")
#                 table.add_column("Metric", style="cyan")
#                 table.add_column("Value", justify="right")
                
#                 # Add rows to table
#                 table.add_row("Last Price", format_number(data['last'], 4))
#                 table.add_row("24h High", format_number(data['high'], 4))
#                 table.add_row("24h Low", format_number(data['low'], 4))
#                 table.add_row("24h Change", f"{format_number(data['change_24h'], 2)}%")
#                 table.add_row("Volume (XRP)", format_number(data['volume'], 2))
#                 table.add_row("Bid", format_number(data['bid'], 4))
#                 table.add_row("Ask", format_number(data['ask'], 4))
#                 table.add_row("Spread", format_number(data['spread'], 4))
#                 table.add_row("Spread %", f"{format_number(data['spread_percent'], 4)}%")
                
#                 # Create price chart
#                 chart = create_price_history_chart(price_history)
#                 chart_panel = Panel(
#                     chart,
#                     title="[bold cyan]XRP/USDT Price Chart[/bold cyan]",
#                     border_style="cyan"
#                 )
                
#                 # Update layout
#                 layout["market_data"].update(Panel(table, title="[bold cyan]XRP/USDT Market Data[/bold cyan]", border_style="cyan"))
#                 layout["chart"].update(chart_panel)
                
#                 # Update display
#                 live.update(layout)

#                 time.sleep(update_interval)  # Wait 5 seconds before next update

#             except KeyboardInterrupt:
#                 break
#             except Exception as e:
#                 console.print(f"[red]Error: {str(e)}[/red]")
#                 time.sleep(update_interval)

if __name__ == "__main__":
    exchange = ccxt.binance()
    data = get_xrp_data(exchange)
    pprint(data)

    ticker = exchange.fetch_ticker('XRP/USDT')
    orderbook = exchange.fetch_order_book('XRP/USDT')
    
    # Calculate spread
    bid = orderbook['bids'][0][0] if orderbook['bids'] else None
    ask = orderbook['asks'][0][0] if orderbook['asks'] else None
    spread = ask - bid if (bid and ask) else None
    spread_percent = (spread / bid * 100) if spread else None

    print(orderbook)
    
        # 'last': ticker['last'],
        # 'high': ticker['high'],
        # 'low': ticker['low'],
        # 'volume': ticker['baseVolume'],
        # 'change_24h': ticker['percentage'],
        # 'bid': bid,
        # 'ask': ask,
        # 'spread': spread,
        # 'spread_percent': spread_percent
    