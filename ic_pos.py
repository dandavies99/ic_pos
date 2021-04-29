from collections import Counter
import warnings


def three_for_two(num_items, price):
    """
    Returns a 'three for the price of two' discounted price given
    the number of items and usual price per single item.

    Args:
        num_items (int): Number of items to which the discount
        should be applied.
        price (int): Usual price per item in pence.

    Returns:
        total (float): Price in pence after discount is applied.
    """
    outside_discount = num_items % 3
    within_discount = num_items - outside_discount
    # Add up total price
    total = (outside_discount * price) + (within_discount * price * 2 / 3)
    return(total)


def three_for_price(num_items, price, offer_price):
    """
    Returns a 'three for £x' discounted price given the number of
    items, the usual price per item, and the offer price for 3 items.
    e.g. to apply a 'three for £1' offer to 8 items at 40p each:
    `three_for_price(8, 40, 100)`.

    Args:
        num_items (int): Number of items to which the discount
        should be applied.
        price (int): Usual price per item in pence.
        offer_price (int): Offer price for 3 items in pence.

    Returns:
        total (float): Price in pence after discount is applied.
    """
    outside_discount = num_items % 3
    within_discount = num_items - outside_discount
    # Add up total price
    total = (outside_discount * price) + (within_discount / 3 * offer_price)

    # Raise a warning if this is a bad deal
    if total > num_items * price:
        warnings.warn("This is a bad deal! " +
                      "The total price is higher after the discount is applied. " +
                      "Price: {}p with discount, {}p without discount. ".format(
                          total, num_items * price))
    return(total)


def checkout(products, item_prices):
    """
    Returns total price in pence of supplied list of products
    after applying all relevant offers.

    Args:
        products (list of str): Product codes of items.
        item_prices (dict): Price in pence of each item, keyed by
        product code.

    Returns:
        price (float): Total price in pence.
    """

    # Check that there are no unrecognised products
    allowed_items = ['A', 'B', 'P']
    assert all(item in allowed_items for item in products),\
        "Unrecognised product code in products list! Allowed codes: {}.".format(
            allowed_items)

    # Check that all the products have a price in the supplied dict
    for item in products:
        assert item in item_prices.keys(),\
            "No entry in item_prices dict for {}.".format(item)

    # Count up the total number of each item
    product_count = Counter(products)
    grand_total = 0  # Start counting the total price

    # Work out price of products after offers and add to grand total
    if 'A' in products:
        grand_total += three_for_two(product_count['A'], item_prices['A'])
    if 'B' in products:
        grand_total += three_for_price(product_count['B'],
                                       item_prices['B'], 100)
    if 'P' in products:
        pears_total = product_count['P'] * item_prices['P']
        grand_total += pears_total

    return(grand_total)

class Checkout:
    """
    This class scans items by their item code and can return a total for the
    items scanned so far, after the application of any discounts.
    """

    def __init__(self, item_prices):
        """
        Instantiate Checkout class.

        Args:
            item_prices (dict): Price in pence of each item, keyed by
            product code.
        """

        self.item_prices = item_prices
        self.products = []

    def scan(self, item_code):
        """
        Appends an item to the list of scanned items.

        Args:
            item_code (str): Code of scanned item.
        """

        if item_code in self.item_prices.keys():
            self.products.append(item_code)
        else:
            raise KeyError(
                "No entry in item_prices dict for {}.".format(item_code))

    def total(self):
        """
        Calculates the total price in pence of all the items scanned so far after
        applying discounts.

        Returns:
            total_price (float): Total price in pence.
        """

        total_price = checkout(self.products, self.item_prices)
        return(total_price)
