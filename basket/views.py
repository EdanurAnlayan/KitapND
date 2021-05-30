from django.shortcuts import redirect, render
from .models import Basket
from products.models import Product

def basket_process(request,id):
    product = Product.objects.get(id=id)
    
    if Basket.objects.filter(product_id=product.id,user=request.user).exists():
        Basket.objects.get(product_id=product.id,user=request.user).delete()
    else:
        Basket.objects.create(product=product,user=request.user)
        
def add_basket(request,id):
    basket_process(request,id)
    return redirect('detail_product',id)

def delete_basket(request,id):
    basket_process(request,id)
    return redirect('basket_list')

def basket_list(request):
    products = Basket.objects.filter(user=request.user)
    products_count = products.count()
    products_in_basket=[]
    for i in products:
        products_in_basket.append(i.product)
    context = {
        'products' : products_in_basket,
        'products_count' : products_count,
        'user' : request.user
    }

    return render(request,'products/basket.html',context)