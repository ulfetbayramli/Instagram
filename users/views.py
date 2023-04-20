from django.shortcuts import render

# Create your views here.
import time
from celery import shared_task
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from .models import Instagram
from django.shortcuts import render, redirect
from django.views import View
from .models import User
from users.tasks import send_confirmation_mail
from .forms import RegisterForm
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.utils.encoding import force_str, force_bytes
from users.tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from selenium import webdriver
from django.shortcuts import render
from .models import Instagram
from .forms import InstagramForm


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
        if form.is_valid():
            user = form.save(commit=False)
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


@login_required
def account_list(request):
    if request.method == 'POST':
        form = InstagramForm(request.POST)

        if form.is_valid():
            instagram = form.save(commit=False)
            instagram.user = request.user

            # log in to the account using Selenium
            url = "https://www.instagram.com/accounts/login/" 
            option = Options() 
            option.headless = True
            option.add_argument("--no-sandbox")
            option.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',options=option)
            driver.get(url)
            username = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'username')))
            username.send_keys(instagram.username)
            time.sleep(2)
            password = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password')))
            password.send_keys(instagram.password)
            time.sleep(3)
            loginbutton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
            loginbutton.click()
            time.sleep(15)
            driver.get('https://www.instagram.com/' + instagram.username)
            time.sleep(10)
            following_count = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href="/' + instagram.username + '/following/"] span'))).text
            follower_count = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href="/' + instagram.username + '/followers/"] span'))).get_attribute('title')

            # update the Instagram object with the new counts and save it to the database
            instagram.followers = int(follower_count.replace(',', ''))
            instagram.following = int(following_count.replace(',', ''))
            instagram.save()

            # close the Selenium browser window
            driver.quit()
            return redirect('home_page')
    else:
        form = InstagramForm()
    instagrams = Instagram.objects.filter(user=request.user)
    return render(request, 'users/homepage.html', {'form': form, 'instagrams': instagrams})

