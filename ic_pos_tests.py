import unittest
from ic_pos import checkout, three_for_price, three_for_two, Checkout

# Test sets to cycle through of inputs and expected ouptuts for the function
# including various edge cases.
param_list = [
    ((['B', 'A', 'B', 'P', 'B'], {'A': 25, 'B': 40, 'P': 30}), 155.0),
    (([], {'A': 25, 'B': 40, 'P': 30}), 0.0),
    ((['B', 'A', 'A', 'A', 'P', 'A', 'B'], {
     'A': 25, 'B': 40, 'P': 30, 'D': 50}), 185.0),
    ((['B', 'B', 'B', 'A', 'A', 'A', 'P'],
     {'A': 25, 'B': 40, 'P': 30}), 180.0),
]


class TestSequence(unittest.TestCase):
    # --------- Test the checkout function --------- #
    # Test parameter sets that should give sensible answers
    def test_checkout_function(self):
        for actual, expected in param_list:
            with self.subTest(msg='Testing checkout function',
                              actual=actual, expected=expected):
                self.assertEqual(checkout(*actual), expected)

    # Test situations where certain Exceptions should be raised
    def test_checkout_urecognised_prod(self):
        with self.assertRaises(Exception) as context:
            checkout(['D', 'B', 'B'], {'A': 25, 'B': 40, 'P': 30})
        self.assertTrue(
            'Unrecognised product code in products list!' in str(
                context.exception))

    def test_checkout_missing_price(self):
        with self.assertRaises(Exception) as context:
            checkout(['A', 'B', 'B'], {'A': 25, 'P': 30})
        self.assertTrue(
            'No entry in item_prices dict for B.' in str(
                context.exception))

    # ------- Simple unit tests for other functions ------ #
    # We should check the offer functions separately
    def test_three_for_two(self):
        discount_price = three_for_two(8, 40)
        self.assertEqual(discount_price, 240.0)

    def test_three_for_price(self):
        discount_price = three_for_price(5, 40, 100)
        self.assertEqual(discount_price, 180.0)

    # ----------- Test the Checkout class ----------- #
    def test_Checkout_class(self):
        co = Checkout({'A': 25, 'B': 40, 'P': 30})
        # Scan some items and check products list and total
        for i in ['B', 'A', 'B', 'P', 'B']:
            co.scan(i)
        self.assertCountEqual(co.products, ['B', 'A', 'B', 'P', 'B'])
        self.assertEqual(co.total(), 155.0)
        # Scan another item and check updated total
        co.scan('B')
        self.assertEqual(co.total(), 195.0)


if __name__ == '__main__':
    unittest.main()
