from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
#from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib import messages

#########################
# Create index views here.
#########################
def index(request):
    return render(request,'app/index.html')



#########################
# Create register views here.
#########################
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if User.objects.filter(username = username):
            messages.error(request, 'Username  a ete deja pris')
            return redirect('register')
        
        if User.objects.filter(email = email):
            messages.error(request, 'cet email  a ete deja un compte')
            return redirect('register')
        
        if not username.isalnum():
            messages.error(request, 'Username doit etre alphanumeric')
            return redirect('register')
        
        if password != password1:
            messages.error(request, 'les deux password ne coincide pas.')
            return redirect('register')
        
        mon_utilisateur = User.objects.create_user(username, email, password)
        mon_utilisateur.first_name = firstname
        mon_utilisateur.last_name = lastname
        mon_utilisateur.save()

        messages.success(request,'Votre conpte a ete cree avec success')
        return redirect('login')
    
    else:
        return render(request,'app/register.html')



#########################
# Create login views here.
#########################

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password=password)
        if user is not None:
            auth.login(request, user)
            firstname = user.first_name
            context = {
                'firstname' : firstname,
            }
            return render(request,'app/index.html', context)
        else:
            messages.error(request, 'Mauvaise authentification')
            return redirect('login')
    
    return render(request,'app/login.html')



###########################
# Create logout views here.
###########################
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')