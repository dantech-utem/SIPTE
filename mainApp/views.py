from django.shortcuts import render
from django.views import View

# Create your views here.
class inicio(View):
   def get(self, request):
        return render(request, 'inicio.html')
     
class loginTest(View):
   def get(self, request):
      return render(request,'test/prueba.html')