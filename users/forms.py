from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User, Instagram


class InstagramForm(forms.ModelForm):
    class Meta:
        model = Instagram
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class RegisterForm(UserCreationForm):
    print("fffffffffffffffffff")
    first_name = forms.CharField(max_length=50, required=True )
    # last_name = forms.CharField(max_length= 50, required= True)
    email = forms.EmailField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        print("ssssssssssssssssssssssss")
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            print("cccccccccccccccccc")
            user.save()
        return user