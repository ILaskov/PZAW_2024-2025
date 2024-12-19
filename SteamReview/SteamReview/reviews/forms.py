from django import forms
import json
import os
from django.conf import settings

class AppSelectForm(forms.Form):
    app_choice = forms.ChoiceField(
        label="Select Game",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, search_query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        file_path = os.path.join(settings.BASE_DIR, 'data', 'api.steampowered.com.json')

        with open(file_path, 'r') as file:
            data = json.load(file)

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
