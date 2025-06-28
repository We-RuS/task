import pytest
from main import split_condition, filter_by_condition, aggregation, read_csv


@pytest.fixture()
def sample_data():
    data = [
        {'name': 'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
        {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'},
        {'name': 'redmi note 12', 'brand': 'xiaomi', 'price': '199', 'rating': '4.6'}
    ]
    return data


def test_split_condition():
    assert split_condition("price>500") == ("price", ">", "500")


def test_split_condition_error():
    with pytest.raises(ValueError):
        split_condition("price500")


def test_filter_by_condition_equal(sample_data):
    assert filter_by_condition("brand=apple", sample_data) == [sample_data[0]]


def test_filter_by_condition_less(sample_data):
    assert filter_by_condition("rating<4.7", sample_data) == [sample_data[2]]


def test_filter_by_condition_bigger(sample_data):
    assert filter_by_condition("price>1000", sample_data) == [sample_data[1]]


def test_aggregate_column_avg(sample_data):
    assert aggregation(sample_data, "price=avg") == [{'avg': 799}]


def test_aggregate_column_max(sample_data):
    assert aggregation(sample_data, "price=max") == [{'max': 1199}]


def test_aggregate_column_error_1(sample_data):
    with pytest.raises(ValueError):
        aggregation(sample_data, "price500")


def test_aggregate_column_error_2(sample_data):
    with pytest.raises(ValueError):
        aggregation(sample_data, "price=foo")


def test_aggregate_column_min(sample_data):
    assert aggregation(sample_data, "price=min") == [{'min': 199}]


def test_read_csv():
    assert not read_csv('test.csv')
