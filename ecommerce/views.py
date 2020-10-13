#not used donot delete
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core import serializers
#used here
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.views import View
from django.core.paginator import Paginator
from django.shortcuts import render,redirect,get_list_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404,JsonResponse
from django.contrib.auth.decorators import login_required
from django.http.request import QueryDict
from django.db.models import Q
#custom created
from .decorators import *
from .forms import CreateUserForm,LoginForm,CustomerForm,UserForm,ContactForm
from .models import Product,Customer,Cart
import json

# Create your views here.

#redirect anonymous user to login use for cart ==0
# @login_required(login_url='ecommerce:register')
def index_page_ecomm(request):
    print(request.user)
    cart=cart_handle(request)
    if type(cart)==type(0):
        cart=cart
    else:
        cart=cart.count()
    print(request.COOKIES)
    products = Product.objects.all()
    all_categories_with_subcategories=categories_with_sub_categories(products)
    context = {
        "username":str(request.user)[:15],
        "products": products[:42],
        "categories": all_categories_with_subcategories,
        "cart":cart,
    }
    # print(all_categories_with_subcategories)
    return render(request, "e-commerce-components.html", context)

def category_view(request,**kwargs):
    cart=cart_handle(request)
    if type(cart)==type(0):
        cart=cart
    else:
        cart=cart.count()
    products=Product.objects.all()
    filtered_products=products.filter(category=kwargs.get('category')).order_by('name')
    all_categories_with_subcategories=categories_with_sub_categories(products)
    page_obj=pagination_handle(request,filtered_products,num_of_objects=6)
    context = {
        "username":str(request.user)[:15],
        #"object_list":filtered_products, page_obj works here
        "categories": all_categories_with_subcategories,
        "page_obj":page_obj,
        "cart":cart,
    }
    return render(request,'category.html',context)

def sub_category_view(request,**kwargs):
    cart=cart_handle(request)
    if type(cart)==type(0):
        cart=cart
    else:
        cart=cart.count()
    products=Product.objects.all()
    filtered_products=products.filter(sub_category=kwargs.get('sub_category')).order_by('name')
    all_categories_with_subcategories=categories_with_sub_categories(products)
    page_obj=pagination_handle(request,filtered_products,num_of_objects=6)
    context = {
        "username":str(request.user)[:15],
        #"object_list":filtered_products, page_obj works here
        "categories": all_categories_with_subcategories,
        "page_obj":page_obj,
        "cart":cart,
    }
    return render(request,'sub_category.html',context)

def product_view(request,*args,**kwargs):
    if request.method=='POST':
        if request.user.is_authenticated:
            product_id=request.POST.get('product_id')
            product_to_add_cart=Product.objects.get(id=product_id)
            cart_obj=request.user.customer.cart
            cart_obj.products.add(product_to_add_cart)
            cart=cart_obj.products.all().count()
        else:
            return redirect('ecommerce:register')
    cart=cart_handle(request)
    if type(cart)==type(0):
        cart=cart
    else:
        cart=cart.count()
    products=Product.objects.all()
    product_view=get_list_or_404(Product,id=kwargs.get('id'))[0]
    all_categories_with_subcategories=categories_with_sub_categories(products)
    context = {
        "username":str(request.user)[:15],
        "products":products.filter(category=product_view.category).exclude(id=product_view.id)[:20],
        "object":product_view,
        "categories": all_categories_with_subcategories,
        "cart":cart,
    }
    return render(request,'product_view_ajax.html',context)
  
@login_required(login_url='ecommerce:register')
def cart_view(request):
    if request.method=="POST":
        cart_obj=request.user.customer.cart
        if request.POST.get('product_id'):
            product_id=request.POST.get('product_id')
            product_to_remove_cart=Product.objects.get(id=product_id)
            cart_obj.products.remove(product_to_remove_cart)
        if request.POST.get('product_id_all'):
            products_cart_all=cart_obj.products.all()
            for product in products_cart_all:
                product_to_remove_cart=Product.objects.get(id=product.id)
                cart_obj.products.remove(product_to_remove_cart)
            
    total_price=0            
    cart=cart_handle(request)
    if type(cart)==type(0):
        cart_all=cart
        cart=cart.count()
    else:
        cart_all=cart
        cart=cart.count()
        for product in cart_all:
            total_price+=product.discounted_price 
    products=Product.objects.all()
    all_categories_with_subcategories=categories_with_sub_categories(products)
    context = {
        "username":str(request.user)[:15],
        "categories": all_categories_with_subcategories,
        "cart":cart,
        "cart_all":cart_all,
        "total_price":total_price,
    }
    return render(request,"cart.html",context)
 
@login_required(login_url='ecommerce:register') 
def cart_add_ajax(request,*args,**kwargs):
    #if request.is_ajax() and request.method=="POST":
    if request.method=="POST":
        print(request.POST)
        qdict=[i for i in dict(request.POST).keys()]
        for post_dict in qdict:
            product_dict=json.loads(post_dict)
            # print(product_dict)
            for key,values in product_dict.items():
                # print(key,values)
                product_to_add_cart=Product.objects.get(id=values)
                cart_obj=request.user.customer.cart
                cart_obj.products.add(product_to_add_cart)
                cart=cart_obj.products.all().count()
                # print(cart)
                response = JsonResponse({'cart': cart})
                return response

@login_required(login_url='ecommerce:register') 
def cart_remove_ajax(request,*args,**kwargs):
    print(request.POST)
    #if request.is_ajax() and request.method=="POST":
    if request.method=="POST":
        qdict=[i for i in dict(request.POST).keys()]
        for post_dict in qdict:
            product_dict=json.loads(post_dict)
            print(product_dict)
            for key,values in product_dict.items():
                # print(key,values)
                product_to_add_cart=Product.objects.get(id=values)
                cart_obj=request.user.customer.cart
                cart_obj.products.remove(product_to_add_cart)
                cart=cart_obj.products.all().count()
                response = JsonResponse({'cart': cart})
                return response

def contactus_view(request):
    form=ContactForm()
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ecommerce:appindex')
    context={"form":form}
    return render(request,'contactus.html',context)

def about_view(request):
    cart=cart_handle(request)
    if type(cart)==type(0):
        cart=cart
    else:
        cart=cart.count()
    products=Product.objects.all()
    all_categories_with_subcategories=categories_with_sub_categories(products)
    context = {
        "username":str(request.user)[:15],
        "categories": all_categories_with_subcategories,
        "cart":cart,
    }
    return render(request,'about.html',context)

@unauthenticated_user
def register_view(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                return render(request,"register.html",{"user_exist":True,"form":CreateUserForm()})
            else:    
                # print(User.objects.filter(email=form.cleaned_data['username']))
                user_created=form.save()
                username=form.cleaned_data.get('username')
                #this will appear in redirected page or in here login page
                messages.success(request,'Account was created for '+username)
                user_obj=User.objects.get(username=form.cleaned_data['username'])
                user_obj.email=user_obj.username
                user_obj.save(update_fields=['email'])
                return redirect('ecommerce:login')
    context={"form":form}
    return render(request,'register.html',context)

@unauthenticated_user
def login_view(request):
    form=LoginForm()
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('ecommerce:appindex')
        else:
            messages.info(request,"username or password is incorrect")
    context={"form":form}
    return render(request,'login.html',context)

def logout_view(request):
    logout(request)
    # return redirect('ecommerce:login')
    return redirect('ecommerce:appindex')

@login_required(login_url='ecommerce:register')
def customer_view(request):
    customer=request.user.customer
    #instance make form associate with user
    #initial will fill that data in form
    # form=CustomerForm(instance=user,initial={"user":user})
    u_form=UserForm(instance=request.user)
    c_form=CustomerForm(instance=customer)
    if request.method=="POST":
        u_form=UserForm(request.POST,instance=request.user)
        c_form=CustomerForm(request.POST,instance=customer)
        if c_form.is_valid():
            # u_form.save()
            c_form.save()
            return redirect('ecommerce:appindex')
            # print(form.cleaned_data)
    # form=CustomerForm()
    context={
        "u_form":u_form,
        "c_form":c_form,
        }
    return render(request,'customer.html',context)
    
def search_view(request):
    cart=cart_handle(request)
    if type(cart)==type(0):
        cart=cart
    else:
        cart=cart.count()
    products=Product.objects.all()
    all_categories_with_subcategories=categories_with_sub_categories(products)
    product_name=request.GET.get("product-search")
    print(product_name)
    if product_name and len(product_name)<=70:
        filtered_products=products.filter(Q(name__icontains=product_name)|Q(category__icontains=product_name)|Q(sub_category__icontains=product_name)).order_by('name').distinct()
        if len(filtered_products)>0:
            page_obj=pagination_handle(request,filtered_products,num_of_objects=6)
        else:
            page_obj=pagination_handle(request,[],num_of_objects=6)
    else:
        page_obj=pagination_handle(request,[],num_of_objects=6)
    context = {
        "username":str(request.user)[:15],
        #"object_list":filtered_products, page_obj works here
        "categories": all_categories_with_subcategories,
        "page_obj":page_obj,
        "cart":cart,
        "tagname":f"product-search={product_name}",
    }
    return render(request,'search_view.html',context)

#######################           not used               ###########################


def prod_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404("product does not exist")
    # product=Product.objects.get(id=id)
    return render(request, "prod_view.html", {"product": product})
    # return HttpResponseNotFound(status=404)

class SubCategoryView(ListView):
    model = Product
    template_name = 'sub_category.html'
    # paginate_by = 1

    def get_context_data(self,**kwargs):
        context = super(**kwargs).get_context_data(**kwargs)
        products = Product.objects.all()
        all_categories_with_subcategories = dict()
        for product in products:
            if all_categories_with_subcategories.get(product.category) == None:
                all_categories_with_subcategories[product.category] = [product]
            else:
                sub_category_list = all_categories_with_subcategories[product.category]
                if product.sub_category not in sub_category_list:
                    all_categories_with_subcategories[product.category].append(
                        product.sub_category)
        filtered_products=products.filter(sub_category=self.kwargs.get('sub_category'))
        paginator = Paginator(filtered_products, 10)
        #print(paginator.num_pages)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        #print(page_obj)
        context = {
            #"object_list":filtered_products, page_obj works here
            "categories": all_categories_with_subcategories,
            "page_obj":page_obj,
        }
        # print(context)
        return context

    #overided method gives value to get_context_data therefore not used
    def get_queryset(self, **kwargs):
        qs = super(**kwargs).get_queryset()
        # print(self.kwargs.get('category'))
        cat_name = self.kwargs.get('sub_category')
        # print(qs.filter(category=cat_name).order_by('name'))
        return qs.filter(sub_category=cat_name).order_by('name')


# class Product_view(TemplateView):
#     template_name = 'prod_view.html'

#     def get_context_data(self, **kwargs):
#         try:
#             products_dict=dict()
#             id=self.kwargs.get('id')
#             # products_dict=super().get_context_data(**kwargs)
#             products_dict['product'] = Product.objects.get(id=id)
#         except Product.DoesNotExist:
#             raise Http404("product does not exist")
#     # product=Product.objects.get(id=id)
#         return products_dict

# class products_detail(DetailView):  #only work with slug or pk in urlconf
#     template_name = 'products_detail.html'
#     model=Product

#     def get_context_data(self,**kwargs):
#         try:
#             id=self.kwargs.get('id')
#             product = Product.objects.get(id=id)
#         except Product.DoesNotExist:
#             raise Http404("product does not exist")
#     # product=Product.objects.get(id=id)
#         return {"product": product}

#used to handle pagination
class products_list(ListView):
    template_name='products_list.html'
    model=Product
    paginate_by=10
    #will generate json of data
    data = serializers.serialize("json",Product.objects.all())
    #print(data)


#     # def get_queryset(self,*args,**kwargs):
#     #     # products=super.get_queryset(*args,**kwargs)  #return whole set to be filtered later
#     #     products=Product.objects.all()
#     #     return products

#     # def get_context_data(self,**kwargs):
#     #     try:
#     #         # id=self.kwargs.get('id')
#     #         products = Product.objects.all()
#     #     except Product.DoesNotExist:
#     #         raise Http404("product does not exist")
#     # # product=Product.objects.get(id=id)
#     #     return {"products": products}


###########################           for dict of category with sub_category    ###################
 # categories=set([product.category for product in products])
    # all_categories=dict()
    # for category in categories:
    #     products_with_category=Product.objects.filter(category=category)
    #     all_categories[category]=[product.sub_category for product in products_with_category]
    # # print(all_categories)

       
        

# class ProductView(DetailView):
#     model = Product
#     template_name = 'product_view.html'

    # #data passed by context
    # def get_object(self, **kwargs):
    #     qs = self.get_queryset()
    #     # print(self.kwargs.get('id'))
    #     return qs.get(id=self.kwargs.get('id'))
    
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     products = Product.objects.all()
    #     all_categories_with_subcategories = dict()
    #     for product in products:
    #         if all_categories_with_subcategories.get(product.category) == None:
    #             all_categories_with_subcategories[product.category] = [product]
    #         else:
    #             sub_category_list = all_categories_with_subcategories[product.category]
    #             if product.sub_category not in sub_category_list:
    #                 all_categories_with_subcategories[product.category].append(
    #                     product.sub_category)
    #     product_view=products.get(id=self.kwargs.get('id'))
    #     context = {
    #         "products":products.filter(category=product_view.category)[:18],
    #         "object":product_view,
    #         "categories": all_categories_with_subcategories,
    #     }
    #     # print(context)
    #     return context