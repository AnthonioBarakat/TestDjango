from decimal import Decimal
from rest_framework import serializers
from .models import Category, MenuItem


class FunctionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)




################################################################################################
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

################################################################################################

        
class MenuItemSerializer(serializers.ModelSerializer):
    # to change the name of a column
    stock = serializers.IntegerField(source="inventory")

    # get new attribute from method below
    price_after_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    

    # get the name instead of the number of category entity
    category = CategorySerializer(read_only=True) # display the serializer class above
    # category = serializers.StringRelatedField() # display the __str__ magic method in model class

    # This line of code is to add a category != 1
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        # depth = 1

    # add a new column tax
    def calculate_tax(self, product:MenuItem):
        return round(product.price * Decimal(1.1), 2)
    

