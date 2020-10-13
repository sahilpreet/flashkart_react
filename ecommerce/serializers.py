from rest_framework import serializers
from .models import Product, Cart
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        # fields=["id","name","category","sub_category","regular_price","discounted_price","image"]
    # def to_representation(self, value):
    #     return {"name":value.name}


class ProductsSerializer(serializers.RelatedField):

    # def to_representation(self, value):
    #     # return {"name":value.name,"id":value.id,"category":value.category,"sub_category":value.sub_category,"regular_price":value.regular_price,"discounted_price":value.discounted_price,"image":value.image}
    #     return value

    class Meta:
        model = Product
        # fields = ["id","name","category","sub_category","regular_price","discounted_price","image"]


class CartSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(read_only=True, many=True)
    # products= serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    # products=serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = Cart
        fields = ['products']

# class ProductSerializer(serializers.ModelSerializer):
#     # products=ProductsSerializer(many=True,read_only=True)

#     def to_representation(self, value):
#         return {"name":value.name,"id":value.id,"category":value.category,"sub_category":value.sub_category,"regular_price":value.regular_price,"discounted_price":value.discounted_price,"image":value.image}

#     class Meta:
#         model = Product
#         fields = ["id","name","category","sub_category","regular_price","discounted_price","image","products"]


# class (serializers.Serializer):
    # category=serializers.DictField(child=serializers.ListField(child=serializers.CharField()))

# class AllCategories(serializers.DictField):
#     child = serializers.ListField(child=serializers.CharField())


class AllCategoriesObj(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary


class AllCategories(serializers.Serializer):
    # intialize fields
    dictionary = serializers.DictField(child=serializers.ListField(child=serializers.CharField()))
    # def __init__(self, dictionary):
    #     self.dictionary = dictionary

# class RegisterSerializer(serializers.Serializer):
#     class Meta:
#         model=User
#         fields=['username','password1','password2']

#     def save(self):
#         user_obj=User(
#             username=validated_data['username'],
#             password1=validated_data['password1'],
#             password2=validated_data['password2'],
#         )
#         user_obj.save()
