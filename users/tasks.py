from __future__ import absolute_import,unicode_literals
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy
from users.models import User
from users.tokens import account_activation_token
from django.conf import settings
from celery import shared_task
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from .models import Instagram
import time



def send_confirmation_mail(user):
    token = account_activation_token.make_token(user) # check if user is exists
    uuid = urlsafe_base64_encode(force_bytes(user.id)) # check who is user
    redirect_url = f"http://127.0.0.1:8000{reverse_lazy('confirmation', kwargs={'uuidb64': uuid,'token': token})}"
    body = render_to_string('users/email/confirmation-email.html', context={'user': user, 'redirect_url': redirect_url})
    message = EmailMessage(subject = "Email Verification", body = body, from_email = settings.EMAIL_HOST_USER, to=[user.email])
    message.content_subtype = 'html'
    message.send()

@shared_task
def update_instagram_stats():
    instagrams = Instagram.objects.all()
    for instagram in instagrams:
        # log in to the account using Selenium
        url = "https://www.instagram.com/accounts/login/"
        option = Options()
        option.headless = True
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',options=option)
        try:
            driver.get(url)
            time.sleep(2)
            username = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'username')))
            username.send_keys(instagram.username)
            time.sleep(2)
            password = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password')))
            password.send_keys(instagram.password)
            time.sleep(3)
            loginbutton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
            loginbutton.click()
            time.sleep(10)

            driver.get('https://www.instagram.com/' + instagram.username)
            time.sleep(10)
            follower_count = driver.find_element(By.CSS_SELECTOR, 'a[href="/' + instagram.username + '/followers/"] span').get_attribute('title')
            following_count= driver.find_element(By.CSS_SELECTOR, 'a[href="/' + instagram.username + '/following/"] span').text

            print(follower_count)
            print(following_count)

            # update the Instagram object with the new counts and save it to the database
            instagram.followers = int(follower_count.replace(',', ''))
            instagram.following = int(following_count.replace(',', ''))
            instagram.save()

            print("Done==============================>")
        finally:
            # close the Selenium browser window
            driver.quit()
