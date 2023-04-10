from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
# from templated_email import send_templated_mail

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy

# from celery import shared_task

from users.models import User

from users.tokens import account_activation_token
from django.conf import settings


# @shared_task
def send_confirmation_mail(user):
    token = account_activation_token.make_token(user) # check if user is exists
    uuid = urlsafe_base64_encode(force_bytes(user.id)) # check who is user
    redirect_url = f"http://127.0.0.1:8000{reverse_lazy('confirmation', kwargs={'uuidb64': uuid,'token': token})}"
    body = render_to_string('users/email/confirmation-email.html', context={'user': user, 'redirect_url': redirect_url})
    message = EmailMessage(subject = "Email Verification", body = body, from_email = settings.EMAIL_HOST_USER, to=[user.email])
    message.content_subtype = 'html'
    message.send()