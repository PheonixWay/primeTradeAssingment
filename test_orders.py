import unittest
from unittest.mock import patch, MagicMock

from bot import orders
from bot import validators

class TestOrderLogic(unittest.TestCase):
    def setUp(self):
        self.valid_symbol = "BTCUSDT"
        self.valid_side = "BUY"
        self.valid_type = "MARKET"
        self.valid_quantity = 0.01
        self.valid_price = 60000.0

    @patch("bot.orders.client")
    def test_place_market_order_success(self, mock_client):
        mock_client.futures_create_order.return_value = {
            'orderId': 123,
            'symbol': self.valid_symbol,
            'side': self.valid_side,
            'type': self.valid_type,
            'status': 'NEW',
            'executedQty': '0.01',
            'avgPrice': '60000.0'
        }
        response = orders.place_order(self.valid_symbol, self.valid_side, self.valid_type, self.valid_quantity)
        self.assertIsNotNone(response)
        self.assertEqual(response['orderId'], 123)


    def test_invalid_symbol(self):
        self.assertFalse(validators.validate_symbol("btc_usdt"))
        self.assertFalse(validators.validate_symbol(""))

    def test_invalid_side(self):
        self.assertFalse(validators.validate_side("HOLD"))

    def test_invalid_type(self):
        self.assertFalse(validators.validate_order_type("ICEBERG"))

    def test_invalid_quantity(self):
        self.assertFalse(validators.validate_quantity(-1))
        self.assertFalse(validators.validate_quantity(0))

    def test_invalid_price(self):
        self.assertFalse(validators.validate_price(-100))
        self.assertFalse(validators.validate_price(0))
        self.assertFalse(validators.validate_price(None))

    @patch("bot.orders.client")
    def test_api_error_handling(self, mock_client):
        from binance.exceptions import BinanceAPIException
        class MockResponse:
            text = '{"msg": "Test error"}'
        mock_client.futures_create_order.side_effect = BinanceAPIException(MockResponse(), 400, "Test error")
        response = orders.place_order(self.valid_symbol, self.valid_side, self.valid_type, self.valid_quantity)
        self.assertIsNone(response)

if __name__ == "__main__":
    unittest.main()
