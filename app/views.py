from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
#from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib import messages
from authentification import settings
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .token import generatorToken



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
        mon_utilisateur.is_active = False
        mon_utilisateur.save()

        messages.success(request,'Votre conpte a ete cree avec success')

        #send Email de Bienvenu
        subject = "Bienvenu dans système d'authentification"
        message = "Bienvenue "+ mon_utilisateur.first_name + " " + mon_utilisateur.last_name + ", \n Nous somme heureux de vous compter parmi nous \n\n\n Merci"
        from_email = settings.EMAIL_HOST_USER
        to_list = [mon_utilisateur.email]
        send_mail(subject, message, from_email, to_list, fail_silently= False)

        #send Email de confirmation
        current_site = get_current_site(request)
        email_subject = "Confirm your email address"
        contextMail = {
            'name':mon_utilisateur.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(mon_utilisateur.pk)),
            'token': generatorToken.make_token(mon_utilisateur)
        }
        messageconfirm = render_to_string("emailconfirm.html", contextMail)

        email = EmailMessage(
            email_subject,
            messageconfirm,
            settings.EMAIL_HOST_USER,
            [mon_utilisateur.email]
        )

        email.fail_silently = False
        email.send()
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
        my_user = User.objects.get(username = username)
        if user is not None:
            auth.login(request, user)
            firstname = user.first_name
            context = {
                'firstname' : firstname,
            }
            return render(request,'app/index.html', context)
        elif my_user.is_active == False:
            messages.error(request,"Vous n'avez pas confirmer votre address email faite le avant de vous connecter merci!")
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
    

# Activate function 

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Votre conpte a ete actived felicatation!")
        return redirect('login')
    else:
        messages.error(request, "Activation echoue... !")
        return redirect('login')
    