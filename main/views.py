from django.shortcuts import render
from django.views import View


class indexView(View):
    def get(self, request):
        return render(request, template_name='index.html')


class aboutView(View):
    def get(self, request):
        return render(request)

class contactView(View):
    def get(self, request):
        return render(request)
    
