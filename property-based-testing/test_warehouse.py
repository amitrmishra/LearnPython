from warehouse import Warehouse, order


# Unit test for specific arguments
def test_warehouse():
    wh = Warehouse({"shoes": 10, "hats": 2, "umbrellas": 0})
    # assert wh.in_stock("shoes")
    # assert wh.in_stock("hats")
    # assert not wh.in_stock("umbrellas")
    # wh.take_from_stock("shoes", 2)
    # assert wh.in_stock("shoes")
    # wh.take_from_stock("hats", 2)
    # assert not wh.in_stock("hats")

    assert wh.in_stock("shoes", 10)
    assert wh.in_stock("hats", 2)
    assert not wh.in_stock("umbrellas", 1)
    wh.take_from_stock("shoes", 2)
    assert wh.in_stock("shoes", 8)
    wh.take_from_stock("hats", 2)
    assert not wh.in_stock("hats", 1)


def test_order_in_stock():
    wh = Warehouse({"shoes": 10, "hats": 2, "umbrellas": 0})
    status, item, quantity = order(wh, "hats", 1)
    assert status == "ok"
    assert item == "hats"
    assert quantity == 1
    assert wh.stock_count("hats") == 1


def test_order_not_in_stock():
    wh = Warehouse({"shoes": 10, "hats": 2, "umbrellas": 0})
    status, item, quantity = order(wh, "umbrellas", 1)
    assert status == "not available"
    assert item == "umbrellas"
    assert quantity == 1
    assert wh.stock_count("umbrellas") == 0


# Add unit test for oversold items after detecting them from the property-based test
def test_order_oversold_item():
    wh = Warehouse({"shoes": 10, "hats": 2, "umbrellas": 0})
    status, item, quantity = order(wh, "hats", 3)
    assert status == "not available"
    assert item == "hats"
    assert quantity == 3
    assert wh.stock_count("hats") == 2


def test_order_unknown_item():
    wh = Warehouse({"shoes": 10, "hats": 2, "umbrellas": 0})
    status, item, quantity = order(wh, "bagel", 1)
    assert status == "not available"
    assert item == "bagel"
    assert quantity == 1


from hypothesis import given, strategies as st


# validate for the property that:
#   quantity ordered and current stock count should sum to the original stock count
@given(item=st.sampled_from(["shoes", "hats"]),
       quantity=st.integers(min_value=1, max_value=4))
def test_stock_level_plus_quantity_equals_original_stock_level(item, quantity):
    wh = Warehouse({"shoes": 10, "hats": 2, "umbrellas": 0})
    initial_stock_level = wh.stock_count(item)
    (status, item, quantity) = order(wh, item, quantity)
    if status == "ok":
        assert wh.stock_count(item) + quantity == initial_stock_level
