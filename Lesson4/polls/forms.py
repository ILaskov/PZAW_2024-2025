from django import forms
from .models import Poll, Choice

class VoteForm(forms.Form):
    choice = forms.ChoiceField(
        widget=forms.RadioSelect,
        required=True,
    )

    def __init__(self, poll, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].choices = [(choice.id, choice.choice_text) for choice in poll.choice_set.all()]
        self.fields['choice'].label = poll.question_text

class NewPollForm(forms.Form):
    poll_name = forms.CharField(max_length=50, required=True)
    question = forms.CharField(max_length=500, required=True)
    choices = forms.JSONField(
        initial=["Choice 1", "Choice 2"],
        help_text='List of choices in the form: ["choice 1", "choice 2", "choice 3"]',
        required=True)
