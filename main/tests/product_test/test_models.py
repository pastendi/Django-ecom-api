import pytest

pytestmark = pytest.mark.django_db
from django.core.exceptions import ValidationError


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange
        # Act
        x = category_factory(name="test_cat")

        # Assert
        assert x.__str__() == "test_cat"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        # Arrange
        # Act
        x = brand_factory(name="test_brand")

        # Assert
        assert x.__str__() == "test_brand"


class TestProductModel:
    def test_str_method(self, product_factory):
        # Arrange
        # Act
        x = product_factory(name="test_product")

        # Assert
        assert x.__str__() == "test_product"


class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        x = product_line_factory(sku="123")
        assert x.__str__() == "123"

    def test_duplicate_order_value(self, product_line_factory, product_factory):
        product = product_factory()
        product_line_factory(order=1, product=product)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=product).clean()
