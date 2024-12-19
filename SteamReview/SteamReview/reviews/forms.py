from django import forms
import json, os, requests
from django.conf import settings

class AppSelectForm(forms.Form):
    app_choice = forms.ChoiceField(
        label="Select Game",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, search_query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            games = data.get('applist', {}).get('data', {})
        except requests.RequestException as e:
            games = []
            self.fields['app_choice'].choices = [('', f"Error fetching games: {str(e)}")]

        apps = data['applist']['apps']

        if search_query:
            matches = [app for app in apps if search_query.lower() in app['name'].lower()]
        else:
            matches = apps

        limited_choices = sorted(
            [(app['appid'], app['name']) for app in matches if app['name']],
            key=lambda x: x[1]
        )[:10]

        self.fields['app_choice'].choices = limited_choices
