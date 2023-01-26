from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CustomerRegisteration
from django.contrib import messages
# Create your views here.
def register(request):
  if request.method=="POST":
    register_form=CustomerRegisteration(request.POST)
    if register_form.is_valid():
      register_form.save()
      messages.success(request,("your now our part"))
      return redirect("todo")

  else:  
    print("get")
    register_form=CustomerRegisteration()
  return render(request,"users_app/register.html",{'register_form':register_form})
