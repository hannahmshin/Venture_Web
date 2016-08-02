#forms.py for tour app
#forms.py
from django import forms
from django.contrib.auth.models import User
from .models import tour_user, Tour, stops #relative import


class UserForm(forms.ModelForm):
    # username = forms.CharField(help_text="Please enter a username.")
    # email = forms.CharField(help_text="Please enter your email.")
    # password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class tour_user_Form(forms.ModelForm):
    class Meta:
        model = tour_user
        fields = [
            "User_Gender",
            "about_you",
            "phone_number",
            "profile_picture",
            "languages",
            "work",
            "hometown",
            "alma_meter",
            "hobbies",
        ]
       


class Tour_Form(forms.ModelForm):
    class Meta:
        model = Tour
        fields = [
            "title",
            "country",
            "state",
            "cityname",
            "tour_theme",
            "capacity",
            #"duration",
            "tour_intensity",
            "image",
            "content",
            "description",
            "draft",
        ]

class Stop_Form(forms.ModelForm):
    class Meta:
        model = stops
        fields = [
            "image",
            "content",
        ]


