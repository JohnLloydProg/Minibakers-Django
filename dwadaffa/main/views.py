from django.shortcuts import render
from django.views import View
from products.models import Product


class indexView(View):
    def get(self, request):
        return render(request)


class aboutView(View):
    def get(self, request):
        return render(request)

class contactView(View):
    def get(self, request):
        return render(request)
    
