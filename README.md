
# Binance Futures Testnet Trading Bot

## Overview
A robust Python bot to place MARKET, LIMIT, and STOP_LIMIT orders on Binance USDT-M Futures Testnet. Features both a CLI and a GUI, with strong input validation, logging, error handling, and modular code.

---

## Features
- Place MARKET, LIMIT, and STOP_LIMIT orders (BUY/SELL)
- Interactive CLI (Typer & Rich) and GUI (PyQt5)
- Input validation for symbol, side, type, quantity, and price
- Logging of all requests, responses, and errors to `trading_bot.log`
- Modular code: separate client, orders, validators, logging
- .env support for API credentials
- Unit tests for order logic and validation

---

## Setup
1. **Clone the repo or unzip the folder**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Create a `.env` file in the root directory with your Binance Testnet API credentials:**
   ```env
   BINANCE_TESTNET_API_KEY=your_testnet_api_key
   BINANCE_TESTNET_API_SECRET=your_testnet_api_secret
   ```
   - Get credentials from https://testnet.binancefuture.com

---

## How to Use

### 1. Interactive CLI
Run:
```bash
python cli.py
```
You will be prompted for symbol, side, order type, quantity, and price (if needed) with menus and validation.

### 2. Command-Line Arguments (Automation)
You can use arguments for scripting or automation:

**MARKET Order Example:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**LIMIT Order Example:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 63106
```

**STOP_LIMIT Order Example:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT --quantity 0.01 --price 55000
```

### 3. Graphical User Interface (GUI)
Run:
```bash
python ui.py
```
You will get a window to enter all order details interactively. Errors and order confirmations are shown in popups.

---

## Logging
- All order requests, responses, and errors are logged in `trading_bot.log`.
- Check this file for troubleshooting and audit trail.

---

## Testing
Run unit tests for order logic and validation:
```bash
python -m unittest test_orders.py
```

---

## File Structure
- `cli.py` — Interactive CLI for order placement
- `ui.py` — PyQt5 GUI for order placement
- `bot/`
  - `client.py` — Binance client setup
  - `orders.py` — Order placement logic
  - `validators.py` — Input validation
  - `logging_config.py` — Logging setup
- `test_orders.py` — Unit tests
- `requirements.txt` — Dependencies
- `.env` — API credentials (not committed)

---

## Troubleshooting
- **API Key/Secret errors:** Ensure `.env` is present and correct.
- **Order fails:** Check `trading_bot.log` for error details.
- **GUI not launching:** Ensure PyQt5 is installed (`pip install -r requirements.txt`).
- **Network issues:** Ensure you have internet access for Binance Testnet and symbol validation.

---

## Requirements
See `requirements.txt` for all dependencies:
```
python-binance==1.0.19
typer==0.12.3
rich==13.7.1
python-dotenv==1.0.1
PyQt5==5.15.10
```