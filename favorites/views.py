from products.views import home
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponseRedirect
from favorites.models import Favorites
from products.models import Product

@login_required(login_url='home')
def favorite_process(request,id):
    product = Product.objects.get(id=id)
    
    if Favorites.objects.filter(product_id=product.id,user=request.user).exists():
        Favorites.objects.get(product_id=product.id,user=request.user).delete()
    else:
        Favorites.objects.create(product=product,user=request.user)
        
def add_favorite(request,id):
    favorite_process(request,id)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER","/products"))

def delete_favorite(request,id):
    favorite_process(request,id)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER","/products"))

def favorite_list(request):
    favorites = Favorites.objects.filter(user=request.user)
    favarites_count = favorites.count()
    products=[]
    for i in favorites:
        products.append(i.product)
    context = {
        'favorites' : products,
        'favarites_count' : favarites_count,
        'user' : request.user
    }

    return render(request,'products/favorite_list.html',context)