from products.models import Category,Product
from django.contrib import admin



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['user','product_name','price','amount']



admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
