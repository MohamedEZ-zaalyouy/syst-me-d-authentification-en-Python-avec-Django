from django.shortcuts import render
from django.http import HttpResponse

#########################
# Create index views here.
#########################
def index(request):
    return render(request,'app/index.html')



#########################
# Create register views here.
#########################
def register(request):
    return render(request,'app/register.html')



#########################
# Create login views here.
#########################
def login(request):
    return render(request,'app/login.html')



#########################
# Create logout views here.
#########################
def logout(request):
    pass