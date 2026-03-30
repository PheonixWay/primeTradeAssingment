
import requests

# Cache for valid futures symbols to avoid repeated API calls
_cached_futures_symbols = None

def get_valid_futures_symbols():
    """
    Fetches and caches the set of valid USDT-M perpetual futures symbols from Binance Testnet.
    Returns:
        set: Set of valid symbol strings.
    """
    global _cached_futures_symbols
    if _cached_futures_symbols is not None:
        return _cached_futures_symbols
    try:
        url = "https://testnet.binancefuture.com/fapi/v1/exchangeInfo"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        symbols = [s['symbol'] for s in data['symbols'] if s['contractType'] == 'PERPETUAL']
        _cached_futures_symbols = set(symbols)
        return _cached_futures_symbols
    except Exception:
        return set()

def validate_symbol(symbol: str) -> bool:
    """
    Validates that the symbol is uppercase, alphanumeric, and exists on Binance Testnet.
    Falls back to basic validation if API is unreachable.
    """
    if not (symbol.isalnum() and symbol.isupper() and len(symbol) >= 6):
        return False
    valid_symbols = get_valid_futures_symbols()
    if not valid_symbols:
        # If unable to fetch, fallback to basic validation
        return True
    return symbol in valid_symbols

def validate_side(side: str) -> bool:
    """
    Validates that the order side is either 'BUY' or 'SELL'.
    """
    return side.upper() in ["BUY", "SELL"]

def validate_order_type(order_type: str) -> bool:
    """
    Validates that the order type is one of 'MARKET', 'LIMIT', or 'STOP_LIMIT'.
    """
    return order_type.upper() in ["MARKET", "LIMIT", "STOP_LIMIT"]

def validate_quantity(quantity: float) -> bool:
    """
    Validates that the quantity is a positive number.
    """
    try:
        return float(quantity) > 0
    except Exception:
        return False

def validate_price(price) -> bool:
    """
    Validates that the price is a positive number (required for LIMIT and STOP_LIMIT orders).
    """
    if price is None:
        return False
    try:
        return float(price) > 0
    except Exception:
        return False
