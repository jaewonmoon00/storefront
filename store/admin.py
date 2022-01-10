from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models
# to add href (clickable)
from django.utils.html import format_html, urlencode
# not to hardcode
from django.urls import reverse

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    @admin.display(ordering='products_count')
    # CAUTION: THIS PART IS COMPLECATED
    def products_count(self, collection):
        # app_model_page
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode(
                {'collection__id': str(collection.id)}
            )
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        
    # every ModelAdmin has get_queryset method we can override.
    def get_queryset(self, request: HttpRequest) -> QuerySet: # you may delete the type annotation
        return super().get_queryset(request).annotate(
            # this part is override.
            products_count=Count('product')
        )

# using decorator we can skip the register line
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # ModelAdmin options (Notice that list_display contains inventory_status, which 
    # matches with the name of the method)
    list_display = [
        # collection_title can be replaced by collection in this case
        'title', 'unit_price', 'inventory_status', 'collection_title'
    ]
    list_editable = ['unit_price']
    list_per_pate = 10
    # this reduces the # of quries
    list_select_related = ['collection']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    # if we did not define __str__ method in collection class, we need to do this
    # to display collection title in the list_display
    def collection_title(self, product):
        return product.collection.title

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
# Register your models here.

# admin.site.register(models.Collection)
# admin.site.register(models.Product, ProductAdmin)