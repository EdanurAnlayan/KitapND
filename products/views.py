from django.contrib import messages
from django.db import models
from products.models import Category, Product,ProductImages
from products.forms import addProductForm,ImageForm
from comment.models import Comment
from comment.forms import CommentForm
from django.shortcuts import redirect, render
from django.forms import modelformset_factory
from django.db.models import Avg
from favorites.models import Favorites
from django.contrib.auth.decorators import login_required

def home(request):
    categories = Category.objects.all()
    context ={

        'categories' : categories
    }
    return render(request,'products/homepage.html',context)

#My products
@login_required(login_url='home')
def view_products(request):
    products = Product.objects.filter(user_id=request.user.id)
    
    if request.method == 'POST':
        ordering = request.POST['ordering']
        if ordering == "Eklenme Tarihi":
            products = products.order_by('-updated_time')
        elif ordering == "Ürün Adı":
            products = products.order_by('product_name')
        elif ordering == "Fiyat":
            products = products.order_by('price')  
    context = {
        'products': products, 
    }
    return render(request,'products/my_products.html',context)

#Add_product_yönlendirme
def add_product_yonlendirme(request,form,Image_formset):
    if request.method == 'POST':
        form = border_form_input(form)
    formset = Image_formset(queryset=ProductImages.objects.none())
    context = {
        'form' : form,
        'formset' : formset,
    }
    return render(request, "products/add-product.html",context)

#Add_image
def add_image(formset,form_save):
    for form_image in formset.cleaned_data:
        if form_image:
            image = form_image['image']
            photo = ProductImages(product = form_save, image=image)
            photo.save()

#Add product
@login_required(login_url='home')
def add_product(request):
    ImageFormSet = modelformset_factory(ProductImages,form=ImageForm,extra=5)
    form = addProductForm(data=request.POST or None)
    if request.method == 'POST':
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImages.objects.none())
        if form.is_valid() and formset.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
            if formset[0].cleaned_data.get('image') != None: 
                pass

            else:
                messages.success(request,"En az bir ürün fotoğrafı eklemeniz gerekmektedir.",extra_tags="danger")
                form = addProductForm(data=request.POST)
                return add_product_yonlendirme(request,form,ImageFormSet)

            try:
                form.save()  

            except Exception as e:
                messages.success(request,str(e),extra_tags="danger")
                form = addProductForm()
                return add_product_yonlendirme(request,form,ImageFormSet)

            add_image(formset,form_save)
            messages.info(request,"Ürün başarılı bir şekilde eklenmiştir. Bizi tercih ettiğiniz için teşekkür ederiz.",extra_tags="info")
            return redirect('add_product')

        else:
            form = addProductForm(request.POST or None)
            return add_product_yonlendirme(request,form,ImageFormSet)
    else:
        form = addProductForm()
    return add_product_yonlendirme(request,form,ImageFormSet)

#Edit product
@login_required(login_url='home')
def edit_product(request,id):
    product = Product.objects.get(id=id)
    form = addProductForm(instance=product)
    if request.user == product.user:
        if request.method == 'POST':
            form = addProductForm(request.POST, instance=product)
            if form.is_valid():
                try:
                    form.save()
                except Exception as e:
                    messages.success(request,"Bir hata oluştu! Lütfen tekrar deneyin.",extra_tags="danger")
                    form = addProductForm(instance=product)
                    context = {
                        'form' : form,
                    }
                    return render(request, "product/edit_product.html",context)
                messages.info(request,"Ürün başarılı bir şekilde güncellenmiştir.",extra_tags="info")
                return redirect('view_products')
            else:
                messages.success(request,"Bir hata oluştu! Lütfen tekrar deneyin.",extra_tags="danger")
                return redirect('view_products')
        context = {
            'form' : form,
        }
        return render(request, 'products/edit_product.html',context)
    else:
        messages.success(request,"Bu sayfaya erişim izniniz bulunmamaktadır!",extra_tags="danger")
        return redirect('home')

#Delete product
@login_required(login_url='home')
def delete_product(request,id):
    product = Product.objects.get(id=id)
    if request.user == product.user:
        if request.method == 'POST':
            product.delete()
            return redirect("view_products")
        context = {
            'product' : product
        }
        return render(request,'products/delete_product.html',context)
    else:
        messages.success(request,"Bu sayfaya erişim izniniz bulunmamaktadır!",extra_tags="danger")
        return redirect('home')

def context_al(request,reviews,product,images,categories,form,is_favorite):
    avg_rate = reviews.aggregate(Avg('rate'))
    
    if avg_rate["rate__avg"] is not None:
        avg_rate= round(avg_rate["rate__avg"])
    else :
        avg_rate= 0

    ratelist=[]

    for i in range(5,0,-1):
        ratelist.append(reviews.filter(rate=i).count()*100)
    
    context = {
                'reviews' : reviews,
                'product' : product,
                'images' : images,
                'categories' : categories,
                'form' : form,
                'avg_rate': avg_rate,
                'ratelist' : ratelist,
                'is_favorite' : is_favorite
            }
    return render(request,'products/single_product.html',context)

#Single product
def detail_product(request,id):
    product = Product.objects.get(id=id)
    images = ProductImages.objects.filter(product_id=id)
    categories = product.categories.all()
    form = CommentForm(data=request.POST or None)
    reviews = Comment.objects.filter(product_id=id)
    is_favorite= False
    if Favorites.objects.filter(product_id=product.id,user=request.user).exists():
        is_favorite= True
    if request.method == 'POST':
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user=request.user
            form_save.product_id = id
            form.save()
            messages.success(request,'Yorumunuz başarılı bir şekilde alınmıştır. Teşekkür ederiz.')
            return redirect('detail_product',id)
        else:
            messages.success(request,'Puan vermeniz gerekmektedir.',extra_tags='danger')
            return context_al(request,reviews,product,images,categories,form,is_favorite)
    else:
        form=CommentForm()
    return context_al(request,reviews,product,images,categories,form,is_favorite)

def border_form_input(form):
    for field in form:
        if field.errors:
            form.fields[field.name].widget.attrs["class"]+=" is-invalid"
        else:
            form.fields[field.name].widget.attrs["class"]+=" is-valid"
    return form

def category_page(request,slug):
    products = Product.objects.filter(categories__slug = slug)
    rate = Comment.objects.filter(product__categories__slug = slug)
    rate_list = []
    for i in products:
        reviews=rate.filter(product_id = i.id)
        avg_rate = reviews.aggregate(Avg('rate'))
        rate_list.append(avg_rate)
    context = {
        'products' : products,
        'rate_list' : rate_list
    }
    return render(request,'products/categorypage.html',context)

