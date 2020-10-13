"""flashkart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from .views import index_page_ecomm,category_view,sub_category_view,product_view,cart_view,register_view,login_view,logout_view,customer_view,cart_add_ajax,cart_remove_ajax,search_view,contactus_view,about_view

#rest framework 
from rest_framework import routers
from .api import ProductViewSet,product_list_func,product_func,product_view_func,all_categories,api_login_view,category_view_func,sub_category_view_func,api_register_view,cart_view_func,cart_add_remove_api,contactus_view_api,search_view_api
#,api_root

router = routers.DefaultRouter()
router.register('product',ProductViewSet)
#router.register('product_func',product_list_func)


app_name='ecommerce' 
urlpatterns = [
    #rest framework
    #path('api/', include(router.urls),name="products_api"),
    #path('api/product/',api_root,name="api_root"),
    path('api/product_list_func/',product_list_func,name="product_list_api"),
    path('api/category/<str:category>',category_view_func,name="category_api"),
    path('api/sub_category/<str:sub_category>',sub_category_view_func,name="sub_category_api"),
    path('api/product_func/<int:id>',product_func,name="product_api"),
    path('api/product_view_func/<int:id>',product_view_func,name="product_view_api"),
    path('api/login',api_login_view,name="login_api"),
    path('api/register',api_register_view,name="register_api"),
    path('api/cart',cart_view_func,name="cart_view_api"),
    path('api/cart_add_remove',cart_add_remove_api,name="cart_add_remove_api"),
    path('api/all_categories',all_categories,name="all_categories"),
    path('api/contactus',contactus_view_api,name="contactus_api"),
    path('api/search/<str:search>',search_view_api,name="search_api"),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #used to generate sitemap
    #path('sitemap.xml', sitemap,{'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}},name='django.contrib.sitemaps.views.sitemap'),
    
    path('',index_page_ecomm,name='appindex'),
    path('category/<str:category>',category_view,name='category'),
    path('sub_category/<str:sub_category>',sub_category_view,name='sub_category'),
    path('product_view/<int:id>',product_view,name='product_view'),
    path('cart',cart_view,name='cart'),
    path('cart_add_ajax',cart_add_ajax,name='cart_add_ajax'),
    path('cart_remove_ajax',cart_remove_ajax,name='cart_remove_ajax'),
    path('search_view',search_view,name='search_view'),
    path('contactus',contactus_view,name='contactus'),
    path('about',about_view,name='about'),
    
    path('register',register_view,name='register'),
    path('login',login_view,name='login'),
    path('logout',logout_view,name='logout'),
    path('customer',customer_view,name='customer'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


