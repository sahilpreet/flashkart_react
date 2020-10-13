from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.http import JsonResponse, HttpResponse
from .decorators import *
import json
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
import io
from django.db.models import Q
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, permissions
from .serializers import ProductSerializer, AllCategories, CartSerializer,AllCategoriesObj
from .models import Product, User ,Contact
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

# generate token for each user registereed save in cookie and use for login
@api_view(["GET","POST"])
def search_view_api(request,*args,**kwargs):
    if request.method == "GET":
        cart = cart_handle_api(request)
        if type(cart) == type(0):
            cart = cart
        else:
            cart = cart.count()
        products = Product.objects.all()
        all_categories_with_sub_category = categories_with_sub_categories_serilaized(products)
        obj = AllCategoriesObj(all_categories_with_sub_category)
        serializercategory = AllCategories(obj)
        product_name= kwargs.get('search')
        paginator = LimitOffsetPagination()
        paginator.max_limit = 10
        if product_name and len(product_name)<=70:
            filtered_products=products.filter(Q(name__icontains=product_name)|Q(category__icontains=product_name)|Q(sub_category__icontains=product_name)).order_by('name').distinct()
            if len(filtered_products)>0:
                result_page = paginator.paginate_queryset(filtered_products, request)
                serializer = ProductSerializer(result_page, many=True)
            else:
                result_page = paginator.paginate_queryset([], request)
                serializer = ProductSerializer(result_page, many=True)
        else:
            result_page = paginator.paginate_queryset([], request)
            serializer = ProductSerializer(result_page, many=True)
            

    return paginator.get_paginated_response({
        "categories": serializercategory.data,
        "cart": cart,
        "products":serializer.data,
        })


@api_view(["POST"])
def contactus_view_api(request):
    if request.method == "POST":
        qdict = [i for i in dict(request.POST).keys()]
        for post_dict in qdict:
            post_query_dict = json.loads(post_dict)
        post_dict = json.loads(post_dict)
        created=True
        try:
            customer_obj=Contact(name=post_dict.get("name"),email=post_dict.get("email"),comment=post_dict.get("comment"))
            customer_obj.save()
        except: 
            created=False
    return Response({"created":created})

@api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([AllowAny])
def cart_add_remove_api(request, *args, **kwargs):
    if request.method == "POST":
        qdict = [i for i in dict(request.POST).keys()]
        for post_dict in qdict:
            post_query_dict = json.loads(post_dict)
        post_dict = json.loads(post_dict)
        try:
            user_obj=Token.objects.get(key=request.headers['Authorization']).user
        except:
            user_obj="AnonymousUser"
        if user_obj!='AnonymousUser':
            try:
                if post_dict.get("action")=="remove":
                    user_obj.customer.cart.products.remove(post_dict.get("product_id"))
                elif post_dict.get("action")=="add":
                    product_to_add_cart=Product.objects.get(id=post_dict.get("product_id"))
                    user_obj.customer.cart.products.add(product_to_add_cart)
                elif post_dict.get("action")=="removeall":
                    [user_obj.customer.cart.products.remove(pid) for pid in post_dict.get("product_id")]
                else:
                    pass
            except:
                pass
            cart_all=user_obj.customer.cart.products.all()
            cart=cart_all.count()
            serializercart = ProductSerializer(cart_all, many=True)
            cart_all = serializercart.data
        products = Product.objects.all()
        all_categories_with_sub_category = categories_with_sub_categories_serilaized(products)
        obj = AllCategoriesObj(all_categories_with_sub_category)
        serializercategory = AllCategories(obj)
        return Response({
            "categories": serializercategory.data,
            "cart": cart,
            "cart_all": cart_all,
        })


@api_view(["POST"])
def api_register_view(request, *args, **kwargs):
    if request.method == "POST":
        qdict = [i for i in dict(request.POST).keys()]
        for post_dict in qdict:
            post_query_dict = json.loads(post_dict)
        post_dict = json.loads(post_dict)
        try:
            user_obj = User.objects.create_user(username=post_dict.get(
                'username'), password=post_dict.get("password1"))
            user = user_obj.save()
            token = "created"
            #token, created = Token.objects.get_or_create(user=user_obj)
        except:
            token = ""
    return Response({"token": str(token)})


@api_view(["POST"])
# @permission_classes([AllowAny])
def api_login_view(request, *args, **kwargs):
    if request.method == "POST":
        qdict = [i for i in dict(request.POST).keys()]
        for post_dict in qdict:
            post_query_dict = json.loads(post_dict)
        try:
            username = post_query_dict['username']
            password = post_query_dict['password']
            user = authenticate(request, username=username, password=password)
            token = Token.objects.get(user=user)
        except:
            token = ""
        return Response({"token": str(token)})


@api_view(["GET", "POST"])
def category_view_func(request, *args, **kwargs):
    if request.method == "GET":
        cart = cart_handle_api(request)
        if type(cart) == type(0):
            cart = cart
        else:
            cart = cart.count()
        products = Product.objects.all()
        all_categories_with_sub_category = categories_with_sub_categories_serilaized(products)
        obj = AllCategoriesObj(all_categories_with_sub_category)
        serializercategory = AllCategories(obj)
        category_products = products.filter(category=kwargs.get('category'))
        paginator = LimitOffsetPagination()
        paginator.max_limit = 10
        result_page = paginator.paginate_queryset(category_products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            "products": serializer.data,
            "categories": serializercategory.data,
            "cart": cart
        })


@api_view(["GET"])
def sub_category_view_func(request, *args, **kwargs):
    if request.method == "GET":
        cart = cart_handle_api(request)
        if type(cart) == type(0):
            cart = cart
        else:
            cart = cart.count()
        products = Product.objects.all()
        all_categories_with_sub_category = categories_with_sub_categories_serilaized(products)
        obj = AllCategoriesObj(all_categories_with_sub_category)
        serializercategory = AllCategories(obj)
        category_products = products.filter(
            sub_category=kwargs.get('sub_category'))
        paginator = LimitOffsetPagination()
        paginator.max_limit = 10
        result_page = paginator.paginate_queryset(category_products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            "products": serializer.data,
            "categories": serializercategory.data,
            "cart": cart
        })


@api_view(["GET"])
def product_view_func(request, *args, **kwargs):
    if request.method == "GET":
        cart = cart_handle_api(request)
        if type(cart) == type(0):
            cart = cart
        else:
            cart = cart.count()
        products = Product.objects.all()
        all_categories_with_sub_category = categories_with_sub_categories_serilaized(products)
        obj = AllCategoriesObj(all_categories_with_sub_category)
        serializercategory = AllCategories(obj)
        product = Product.objects.get(id=kwargs.get('id'))
        serializer = ProductSerializer([product], many=True)
        products = Product.objects.filter(category=product.category)
        serializerproducts = ProductSerializer(products[:22], many=True)
        return Response({
            "product": serializer.data[0],
            "categories":serializercategory.data,
            "cart": cart,
            "products": serializerproducts.data
        })
    if request.method == "POST":
        qdict = [i for i in dict(request.POST).keys()]
        for post_dict in qdict:
            post_query_dict = json.loads(post_dict)
        product = Product.objects.get(id=post_query_dict["product_id"])
        serializer = ProductSerializer([product], many=True)
        return Response({"products": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def cart_view_func(request):
    if request.method == "GET":
        cart = cart_handle_api(request)
        if type(cart) == type(0):
            cart_all = []
            cart = 0
        else:
            cart_all = cart
            cart = cart.count()
            serializercart = ProductSerializer(cart_all, many=True)
            cart_all = serializercart.data
        products = Product.objects.all()
        all_categories_with_sub_category = categories_with_sub_categories_serilaized(products)
        obj = AllCategoriesObj(all_categories_with_sub_category)
        serializercategory = AllCategories(obj)
        return Response({
            "categories": serializercategory.data,
            "cart": cart,
            "cart_all": cart_all,
        })


@api_view(["GET"])
def all_categories(request):
    if request.method == "GET":
        cart = cart_handle(request)
        if type(cart) == type(0):
            cart = cart
        else:
            cart = cart.count()
        products = Product.objects.all()
        all_categories_with_sub_category = categories_with_sub_categories_serilaized(
            products)
        return Response({
            "categories": json.dumps(all_categories_with_sub_category),
            "cart": cart,
        })

@api_view(["GET", "POST"])
def product_list_func(request):
    if request.method == "GET":
        cart = cart_handle_api(request)
        if type(cart) == type(0):
            cart = cart
        else:
            cart = cart.count()
        products = Product.objects.all().order_by('id')
        all_categories_with_sub_category = categories_with_sub_categories_serilaized(products)
        obj = AllCategoriesObj(all_categories_with_sub_category)
        serializercategory = AllCategories(obj)
        serializer = ProductSerializer(products[:45], many=True)
        return Response({
            "products": serializer.data[:45],
            "categories": serializercategory.data,
            "cart": cart
        })
    elif request.method == 'POST':
        qdict = [i for i in dict(request.data).keys()]
        for post_dict in qdict:
            post_query_dict = json.loads(post_dict)
        product = Product.objects.get(id=post_query_dict["product_id"])
        serializer = ProductSerializer([product], many=True)
        return Response({"products": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# only andle get and post otherwise return 400 bad request
@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
def product_func(request, id):
    try:
        product = Product.objects.get(id=id)
    except product.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        serializer = ProductSerializer([product], many=True)
        return Response({"products": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
