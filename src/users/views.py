from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views import View

from .models import User
from users.tasks import send_confirmation_mail
from .forms import RegisterForm
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.utils.encoding import force_str, force_bytes
from users.tokens import account_activation_token



def HomePage(request):
    return render(request , 'users/homepage.html')


def ProfilePage(request):
    return render(request , 'users/profile.html')

class Register(View):
    form_class = RegisterForm
    template_name = 'users/login-register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = self.form_class(request.POST)
        print("valid")
        if form.is_valid():
            user = form.save(commit=False)
            print("post")
            user.is_active = False
            user.save()
            send_confirmation_mail(user)
            messages.success(request, 'We sent Confirmation Email !')
            return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})



def confirmation(request, uuidb64, token):
    uuid = force_str(urlsafe_base64_decode(uuidb64))
    user = User.objects.filter(id = int(uuid), is_active = False).first()
   
    if user and account_activation_token.check_token(user, token):
        messages.success(request, 'Your account activated') 
        user.is_active = True
        user.save()
        return redirect("login")
    else:
        messages.error(request, 'your link expired or link invalid')
        return redirect("/")