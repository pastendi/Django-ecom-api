from rest_framework import serializers

from .models import (
    Attribute,
    AttributeValue,
    Brand,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductType,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ("id",)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("id",)


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = (
            "id",
            "name",
        )


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = (
            "attribute",
            "attribute_value",
        )


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ("price", "sku", "stock", "order", "product_image", "attribute_value")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute_value")
        attr_values = {}
        for key in av_data:
            attr_values.update({key["attribute"]["name"]: key["attribute_value"]})
        data.update({"specifications": attr_values})
        return data


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="brand.name")
    category = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True)
    attribute = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "description",
            "brand",
            "category",
            "attribute",
            "product_line",
        )

    def get_attribute(self, instance):
        attribute = Attribute.objects.filter(product_type_attribute__product__id=instance.id)
        return AttributeSerializer(attribute, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute")
        attr_values = {}
        for key in av_data:
            attr_values.update({key["id"]: key["name"]})
        data.update({"specifications": attr_values})
        return data
