from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Basket
from products.models import Product

@login_required(login_url='home')
def basket_process(request,id):
    product = Product.objects.get(id=id)
    
    if Basket.objects.filter(product_id=product.id,user=request.user).exists():
        Basket.objects.get(product_id=product.id,user=request.user).delete()
    else:
        Basket.objects.create(product=product,user=request.user)
        
def add_basket(request,id):
    basket_process(request,id)
    return redirect('basket_list')

def basket_list(request):
    products = Basket.objects.filter(user=request.user)
    products_count = products.count()
    products_in_basket=[]
    total_price = 0
    for i in products:
        products_in_basket.append(i.product)
        total_price += i.product.price
    
    context = {
        'total_price' : total_price,
        'products' : products_in_basket,
        'products_count' : products_count,
        'user' : request.user
    }

    return render(request,'products/basket.html',context)

def basket_details(request):
    return render(request,'products/checkout-details.html')

def basket_payment(request):
    return render(request,'products/checkout-payment.html')

def basket_review(request):
    return render(request,'products/checkout-review.html')

def basket_complete(request):
    return render(request,'products/checkout-complete.html')