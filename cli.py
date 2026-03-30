
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt,FloatPrompt
from bot.orders import place_order
from bot.validators import (
    validate_symbol,
    validate_quantity,
    validate_price
)

console = Console()

def enhanced_cli():
    """
    Interactive CLI for placing Binance Futures orders.
    Prompts the user for all required order details with validation and displays the result in a table.
    """
    console.print("[bold magenta]\nWelcome to the Binance Futures Testnet Trading Bot![/bold magenta]")

    # Prompt for trading symbol
    while True:
        symbol = Prompt.ask("Enter trading symbol (e.g., BTCUSDT)").upper()
        if validate_symbol(symbol):
            break
        console.print("[red]Invalid symbol. Must be uppercase, alphanumeric, e.g., BTCUSDT[/red]")

    # Prompt for order side
    side = Prompt.ask("Order side", choices=["BUY", "SELL"], default="BUY").upper()

    # Prompt for order type
    order_type = Prompt.ask("Order type", choices=["MARKET", "LIMIT", "STOP_LIMIT"], default="MARKET").upper()

    # Prompt for quantity
    while True:
        try:
            quantity = FloatPrompt.ask("Enter quantity (must be positive)")
            if validate_quantity(quantity):
                break
            else:
                console.print("[red]Quantity must be a positive number.[/red]")
        except Exception:
            console.print("[red]Invalid input. Please enter a number.[/red]")

    # Prompt for price if needed (LIMIT or STOP_LIMIT)
    price = None
    if order_type in ["LIMIT", "STOP_LIMIT"]:
        while True:
            try:
                price = FloatPrompt.ask(f"Enter price for {order_type} order (must be positive)")
                if validate_price(price):
                    break
                else:
                    console.print("[red]Price must be a positive number.[/red]")
            except Exception:
                console.print("[red]Invalid input. Please enter a number.[/red]")

    console.print(f"\n[bold cyan]\u23f3 Initiating {order_type} {side} order for {quantity} {symbol}...[/bold cyan]")
    response = place_order(symbol, side, order_type, quantity, price)

    if response:
        # Display order details in a table
        table = Table(title="Order Successfully Placed", show_header=True, header_style="bold green")
        table.add_column("Order ID", style="dim")
        table.add_column("Symbol", justify="center")
        table.add_column("Side", justify="center")
        table.add_column("Type", justify="center")
        table.add_column("Status", style="bold green", justify="center")
        table.add_column("Executed Qty", justify="right")
        table.add_column("Price", justify="right")

        table.add_row(
            str(response.get('orderId', 'N/A')),
            response.get('symbol', symbol),
            response.get('side', side),
            response.get('type', order_type),
            response.get('status', 'NEW'),
            str(response.get('executedQty', '0')),
            str(price if price else "Market Price")
        )
        console.print(table)
        console.print("[dim]Log saved to trading_bot.log[/dim]\n")
    else:
        # Print error message if order failed
        console.print("[bold red]Order failed. Check `trading_bot.log` file for details.[/bold red]\n")

if __name__ == "__main__":
    enhanced_cli()