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
    def test_str_method(self, product_line_factory, attribute_value_factory):
        attr = attribute_value_factory(attribute_value="test")
        x = product_line_factory(sku="123", attribute_value=(attr,))
        assert x.__str__() == "123"

    def test_duplicate_order_value(self, product_line_factory, product_factory):
        product = product_factory()
        product_line_factory(order=1, product=product)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=product).clean()


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        x = product_image_factory(order=1)
        assert x.__str__() == "1"


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        x = attribute_factory(name="test_attribute")
        assert x.__str__() == "test_attribute"


class TestAttributeValueModel:
    def test_str_method(self, attribute_value_factory, attribute_factory):
        attr = attribute_factory(name="test_attribute")
        x = attribute_value_factory(attribute_value="test_value", attribute=attr)
        assert x.__str__() == "test_attribute-test_value"


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        attr = attribute_factory(name="test")
        x = product_type_factory(name="test_type", attribute=(attr,))
        assert x.__str__() == "test_type"
