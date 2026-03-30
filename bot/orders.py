from binance.exceptions import BinanceAPIException
from bot.logging_config import logger
from bot.client import get_binance_client

# Initialize the Binance client for API requests
client = get_binance_client()

def place_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """
    Places an order on the Binance Futures Testnet.
    Supports MARKET, LIMIT, and STOP_LIMIT order types.
    Logs all requests and responses for auditing and debugging.
    Args:
        symbol (str): Trading symbol, e.g., 'BTCUSDT'.
        side (str): 'BUY' or 'SELL'.
        order_type (str): 'MARKET', 'LIMIT', or 'STOP_LIMIT'.
        quantity (float): Order quantity.
        price (float, optional): Price for LIMIT/STOP_LIMIT orders.
    Returns:
        dict or None: API response if successful, None otherwise.
    """
    try:
        # Log the order request details (for assignment requirement and debugging)
        logger.info(f"Order Request: Symbol={symbol.upper()}, Side={side.upper()}, Type={order_type.upper()}, Qty={quantity}, Price={price}")

        # Prepare base parameters for all order types
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': order_type.upper(),
            'quantity': quantity
        }

        # Add price and timeInForce for LIMIT orders
        if order_type.upper() == 'LIMIT':
            if not price:
                raise ValueError("'price' is required for LIMIT orders.")
            params['price'] = price
            params['timeInForce'] = 'GTC'  # Good Till Cancelled

        # Add price and stopPrice for STOP_LIMIT orders
        if order_type.upper() == 'STOP_LIMIT':
            if not price:
                raise ValueError("'price' is required for STOP_LIMIT orders.")
            params['price'] = price
            params['stopPrice'] = price  # For demonstration, use the same value for stop and limit
            params['timeInForce'] = 'GTC'

        # Make the actual API call to Binance
        response = client.futures_create_order(**params)

        # Log order response details (for assignment requirement and debugging)
        order_id = response.get('orderId')
        status = response.get('status')
        executed_qty = response.get('executedQty')
        avg_price = response.get('avgPrice', '0.0')

        # Log a success message (emoji removed for Windows compatibility)
        success_msg = f"Order Successful! ID: {order_id} | Status: {status} | Executed Qty: {executed_qty} | Avg Price: {avg_price}"
        logger.info(success_msg)

        return response

    except BinanceAPIException as e:
        # Handle API-level errors (e.g., insufficient balance, invalid symbol)
        logger.error(f"Binance API Error: Code={e.status_code} - {e.message}")
        return None
    except ValueError as ve:
        # Handle validation errors (e.g., missing required parameters)
        logger.error(f"Input Error: {ve}")
        return None
    except Exception as e:
        # Handle unexpected errors (e.g., network issues, unknown exceptions)
        logger.error(f"Unexpected System Error: {e}")
        return None