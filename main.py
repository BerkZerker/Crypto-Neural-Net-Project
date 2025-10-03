import ccxt
import time
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich import print as rprint
import asyncio
from datetime import datetime

# Initialize Rich console
console = Console()

def get_supported_exchanges():
    """Get list of US-compliant exchanges that support XRP trading"""
    us_exchanges = ['kraken', 'coinbasepro', 'gemini']  # Known US-compliant exchanges
    exchanges = []
    
    for exchange_id in us_exchanges:
        try:
            exchange = getattr(ccxt, exchange_id)()
            exchange.enableRateLimit = True  # Respect rate limits
            
            # Check if exchange supports XRP trading
            if exchange.has['fetchTicker']:
                # Load markets to verify XRP/USDT pair availability
                exchange.load_markets()
                if 'XRP/USDT' in exchange.markets or 'XRP/USD' in exchange.markets:
                    exchanges.append(exchange)
        except Exception as e:
            console.print(f"[red]Error initializing {exchange_id}: {str(e)}[/red]")
            continue
    return exchanges

def fetch_xrp_price(exchange):
    """Fetch XRP/USDT or XRP/USD price from a single exchange"""
    try:
        # Try XRP/USDT first, fall back to XRP/USD if needed
        symbol = 'XRP/USDT' if 'XRP/USDT' in exchange.markets else 'XRP/USD'
        ticker = exchange.fetch_ticker(symbol)
        return {
            'exchange': exchange.id,
            'bid': ticker['bid'],
            'ask': ticker['ask'],
            'symbol': symbol
        }
    except Exception as e:
        console.print(f"[red]Error fetching from {exchange.id}: {str(e)}[/red]")
        return None

def main():
    # Setup exchanges
    console.print("[bold blue]Initializing US-compliant exchanges...[/bold blue]")
    exchanges = get_supported_exchanges()
    
    if not exchanges:
        console.print("[red]No supported US exchanges found with XRP trading pairs. Please check your internet connection or try again later.[/red]")
        return
        
    console.print(f"[green]Found {len(exchanges)} supported US exchanges[/green]")
    for exchange in exchanges:
        console.print(f"[green]✓ {exchange.id.upper()}[/green]")
    console.print()

    # Create progress bar
    with Progress() as progress:
        task = progress.add_task("[cyan]Analyzing spreads...", total=30)

        for i in range(30):
            prices = []
            
            # Fetch prices from all exchanges
            for exchange in exchanges:
                price_data = fetch_xrp_price(exchange)
                if price_data:
                    prices.append(price_data)

            if prices:
                # Find lowest ask and highest bid
                lowest_ask = min(prices, key=lambda x: x['ask'])
                highest_bid = max(prices, key=lambda x: x['bid'])
                spread = lowest_ask['ask'] - highest_bid['bid']
                spread_percentage = (spread / lowest_ask['ask']) * 100

                # Create and display results table
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Timestamp")
                table.add_column("Best Bid Exchange")
                table.add_column("Best Bid")
                table.add_column("Best Ask Exchange")
                table.add_column("Best Ask")
                table.add_column("Spread")
                table.add_column("Spread %")

                table.add_row(
                    datetime.now().strftime("%H:%M:%S"),
                    highest_bid['exchange'],
                    f"${highest_bid['bid']:.4f}",
                    lowest_ask['exchange'],
                    f"${lowest_ask['ask']:.4f}",
                    f"${spread:.4f}",
                    f"{spread_percentage:.2f}%"
                )

                console.print(table)

            # Update progress
            progress.update(task, advance=1)
            time.sleep(2)

if __name__ == "__main__":
    console.print("[bold yellow]XRP Spread Analysis Tool[/bold yellow]")
    console.print("[bold yellow]========================[/bold yellow]\n")
    main()
