from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.shortcuts import render
# Q for or operator, F for referencing a field
from django.db.models import Q,F
#from django.http import HttpResponse
from store.models import Product

# Create your views here.
def say_hello(request):
    try:
        # sort by price in decreasing order & alphabetical order
        queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20).order_by("-unit_price","title")#.reverse()
    #queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    #queryset = Product.objects.filter(inventory__lt=F('collection__id'))
    except ObjectDoesNotExist:
        pass
    return render(request, 'hello.html', {'name':'Jaewon', 'product':list(queryset)})
    #return HttpResponse("Hello World")