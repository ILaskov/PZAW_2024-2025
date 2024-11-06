from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, reverse

open_polls = {
    "No Man's Sky": {
        "question": "What world do you live in?",
        "options": [
            {
                "text": "Somewhere",
                "votes": 0,
            },
            {
                "text": "Here",
                "votes": 0,
            }
        ]
    },
    "THE FINALS": {
        "question": "What class do you play?",
        "options": [
            {
                "text": "Light",
                "votes": 0,
            },
            {
                "text": "Medium",
                "votes": 0,
            },
            {
                "text": "Heavy",
                "votes": 0,
            }
        ]
    },
    "Balatro": {
        "question": "What deck do you play?",
        "options": [
            {
                "text": "Red",
                "votes": 0,
            },
            {
                "text": "Blue",
                "votes": 0,
            }
        ]
    }
}

# Create your views here.
def index(request, poll_name):
    context = {"polls": open_polls}
    return render(request, "polls/single.html", context)

def forms(request):
    if request.method == 'GET':
        return render(request, "polls/forms.html", {})
    if request.method == 'POST':
        return render(request, "polls/post.html", {'params': request.POST})
    else:
        return HttpResponseBadRequest("Unsupported method")

def vote(request, poll_name):
    if poll_name in poll_names:
        selected_choice = open_polls[poll_name]['options'][int(request.POST["choice"])]
        selected_choice['votes'] += 1
        return HttpResponseRedirect(reverse("polls:results", args=[poll_name]))
    else:
        return render( request, "polls/detail.html", { "poll_name": poll_name, },)

def results(request, poll_name):
    context = { "poll_name": poll_name, }
    retcode = 200
    if poll_name in poll_names:
        context['poll'] = open_polls[poll_name]
        context['total_votes'] = max(1, sum(option['votes'] for option in open_polls[poll_name]['options']))
    else:
        retcode = 404
    return render(request, "polls/results.html", context, status=retcode)
