from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Car


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        
        
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
        
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "brand",
            "model",
            "year",
            "mileage",
            "fuel",
            "price",
            "description",
            "image",
        ]