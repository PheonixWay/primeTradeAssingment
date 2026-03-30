import os
from dotenv import load_dotenv
from binance.client import Client
from bot.logging_config import logger

# Load environment variables from .env file
load_dotenv()

# Retrieve API credentials from environment
API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
API_SECRET = os.getenv("BINANCE_TESTNET_API_SECRET")

def get_binance_client():
    """
    Initializes and returns a Binance Client for the Testnet.
    Raises an error if credentials are missing or connection fails.
    Returns:
        Client: Authenticated Binance client instance.
    """
    if not API_KEY or not API_SECRET:
        logger.error("API Key or Secret not found!")
        raise ValueError("API credentials missing")
    try:
        client = Client(API_KEY, API_SECRET, testnet=True)
        client.futures_ping()  # Test connection
        logger.info("Binance Futures Testnet Connection Successful!")
        return client
    except Exception as e:
        logger.error(f"Binance API Connection Failed: {e}")
        raise e

if __name__ == "__main__":
    print("Testing Binance Testnet Connection...")
    try:
        client = get_binance_client()
        account_info = client.futures_account_balance()
        print("\nConnection Successful!")
        print(f"Total USDT Balance in Testnet: {account_info[1]['balance']} USDT")
    except Exception as e:
        print(f"\nConnection Failed: {e}")