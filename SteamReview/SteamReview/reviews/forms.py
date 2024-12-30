from typing import Required

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import requests

#Creating a class that searches through Steam game database
class AppSelectForm(forms.Form):
    app_choice = forms.ChoiceField(
        label="Select Game:",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, search_query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Getting data from Steam JSON file with games from their API
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            self.fields['app_choice'].choices = [('', f"Error fetching games: {str(e)}")]

        #Creating variable that stores all the games
        apps = data['applist']['apps']

        #Searching through all games to find those that match what user is searching for
        if search_query:
            matches = [app for app in apps if search_query.lower() in app['name'].lower()]
        else:
            matches = apps

        #Displaying only 10 most accurate results
        limited_choices = sorted(
            [(app['appid'], app['name']) for app in matches if app['name']],
            key=lambda x: x[1]
        )[:10]

        self.fields['app_choice'].choices = limited_choices

#Form for user registration
class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
