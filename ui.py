import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from bot.orders import place_order
from bot.validators import (
    validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
)

class TradingBotUI(QWidget):
    """
    PyQt5 GUI for placing Binance Futures orders.
    Allows the user to input all order details, validates them, and displays results or errors.
    """
    def reset_fields(self):
        """Clears all input fields and resets dropdowns to default values."""
        self.symbol_input.clear()
        self.side_combo.setCurrentIndex(0)
        self.type_combo.setCurrentIndex(0)
        self.quantity_input.clear()
        self.price_input.clear()
        self.toggle_price_field(self.type_combo.currentText())

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Binance Futures Testnet Trading Bot")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        """Initializes the UI layout and widgets."""
        layout = QVBoxLayout()

        # Symbol input
        self.symbol_label = QLabel("Symbol (e.g., BTCUSDT):")
        self.symbol_input = QLineEdit()
        layout.addWidget(self.symbol_label)
        layout.addWidget(self.symbol_input)

        # Side selection
        self.side_label = QLabel("Side:")
        self.side_combo = QComboBox()
        self.side_combo.addItems(["BUY", "SELL"])
        layout.addWidget(self.side_label)
        layout.addWidget(self.side_combo)

        # Order type selection
        self.type_label = QLabel("Order Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["MARKET", "LIMIT", "STOP_LIMIT"])
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)

        # Quantity input
        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)

        # Price input (only enabled for LIMIT/STOP_LIMIT)
        self.price_label = QLabel("Price (required for LIMIT/STOP_LIMIT):")
        self.price_input = QLineEdit()
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)


        # Submit Button
        self.submit_btn = QPushButton("Place Order")
        self.submit_btn.clicked.connect(self.place_order)
        layout.addWidget(self.submit_btn)

        # Reset Button
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_fields)
        layout.addWidget(self.reset_btn)

        self.setLayout(layout)
        self.type_combo.currentTextChanged.connect(self.toggle_price_field)
        self.toggle_price_field(self.type_combo.currentText())

    def toggle_price_field(self, order_type):
        """
        Enables or disables the price input field based on the selected order type.
        Price is only required for LIMIT and STOP_LIMIT orders.
        """
        if order_type in ["LIMIT", "STOP_LIMIT"]:
            self.price_input.setEnabled(True)
        else:
            self.price_input.setEnabled(False)
            self.price_input.clear()

    def place_order(self):
        """
        Collects input values, validates them, places the order, and displays the result or error.
        """
        symbol = self.symbol_input.text().strip().upper()
        side = self.side_combo.currentText().upper()
        order_type = self.type_combo.currentText().upper()
        quantity = self.quantity_input.text().strip()
        price = self.price_input.text().strip() if self.price_input.isEnabled() else None

        # Validate all inputs
        if not validate_symbol(symbol):
            self.show_error("Invalid symbol. Must be uppercase, alphanumeric, e.g., BTCUSDT")
            return
        if not validate_side(side):
            self.show_error("Side must be BUY or SELL.")
            return
        if not validate_order_type(order_type):
            self.show_error("Order type must be MARKET, LIMIT, or STOP_LIMIT.")
            return
        if not validate_quantity(quantity):
            self.show_error("Quantity must be a positive number.")
            return
        if order_type in ["LIMIT", "STOP_LIMIT"]:
            if not validate_price(price):
                self.show_error(f"{order_type} order requires a positive price.")
                return
            price = float(price)
        else:
            price = None
        quantity = float(quantity)

        # Place the order and handle the response
        try:
            response = place_order(symbol, side, order_type, quantity, price)
            if response:
                msg = f"Order Placed!\nOrder ID: {response.get('orderId')}\nStatus: {response.get('status')}\nExecuted Qty: {response.get('executedQty')}"
                QMessageBox.information(self, "Success", msg)
                self.reset_fields()
            else:
                # Try to extract last error from log file for user-friendly popup
                error_msg = self.get_last_error_from_log()
                if error_msg:
                    self.show_error(error_msg)
                else:
                    self.show_error("Order failed. Check trading_bot.log for details.")
        except Exception as e:
            self.show_error(str(e))


    def get_last_error_from_log(self):
        """
        Reads the log file and returns the last error message for user-friendly error popups.
        """
        try:
            with open("trading_bot.log", "r", encoding="utf-8") as f:
                lines = f.readlines()
            # Find last error line
            for line in reversed(lines):
                if "ERROR" in line:
                    # Extract message after last ' - '
                    msg = line.split(" - ")[-1].strip()
                    # If Binance API error, extract after last dash
                    if "Binance API Error" in msg and "-" in msg:
                        # e.g. 'Binance API Error: Code=400 - Limit price can't be lower than 63113.16.'
                        important = msg.split("-", 1)[-1].strip()
                        return important
                    return msg
        except Exception:
            pass
        return None

    def show_error(self, message):
        """
        Displays an error message in a popup dialog.
        """
        QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingBotUI()
    window.show()
    sys.exit(app.exec_())
