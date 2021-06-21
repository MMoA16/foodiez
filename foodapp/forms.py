from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your forms here.

class NewUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ("username", "email", "password1","password2")