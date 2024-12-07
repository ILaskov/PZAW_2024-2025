from .forms import VoteForm, NewPollForm
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, reverse
from .models import Poll,Choice
from django.db.models import Sum
from django.views import generic

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
def index(request):
    context = {
        "polls": Poll.objects.order_by("-pub_date")[:5]
    }
    return render(request, "polls/topic.html", context)

class IndexView(generic.ListView):
    template_name = "polls/single.html"
    context_object_name = "latest_polls"
    queryset = Poll.objects.order_by("-pub_date")[:5]

def single(request, poll_id):
    # if topic not in open_polls:
    #     return HttpResponseBadRequest("Page doesn't exist")
    # retcode = 200
    # poll = open_polls[topic]
    # context = {"title": f"{poll['question']}", "polls": [x for x in poll["options"]], "topic": topic}
    # if topic in open_polls:
    #     context['vote_form'] = VoteForm(open_polls[topic])
    # else:
    #     retcode = 404
    context = {}
    retcode = 200
    try:
        poll = Poll.objects.get(pk=poll_id)
        context['poll'] = poll
        context['vote_form'] = VoteForm(poll)
    except Poll.DoesNotExist:
        retcode = 404
    return render(request, "polls/poll.html", context, status=retcode)


class DetailView(generic.DetailView):
    model = Poll
    template_name = "polls/poll.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vote_form'] = VoteForm(self.object)
        return context

def forms(request):
    if request.method == 'GET':
        return render(request, "polls/forms.html", {})
    if request.method == 'POST':
        return render(request, "polls/post.html", {'params': request.POST})
    else:
        return HttpResponseBadRequest("Unsupported method")

# def vote(request, poll_id):
#     if request.method == 'GET':
#         return HttpResponseRedirect(reverse("polls:poll", args=[poll_id]))
#     elif request.method == 'POST':
#         try:
#             poll = Poll.objects.get(pk=poll_id)
#             vote_form = VoteForm(poll, data=request.POST)
#             if vote_form.is_valid():
#                 selected_choice = Choice.objects.get(pk=vote_form.cleaned_data['choice'])
#                 selected_choice.votes += 1
#                 selected_choice.save()
#                 return HttpResponseRedirect(reverse("polls:results", args=[poll_id]))
#             else:
#                 context = {
#                     'poll': poll,
#                     'vote_form': vote_form
#                 }
#                 return render(request, "polls/poll.html", context)
#
#         except Poll.DoesNotExist:
#             return render(request, "polls/poll.html", status=404)
#     else:
#         return HttpResponseBadRequest("Unsupported method")

def vote(request, poll_id):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse("polls:details", args=[poll_id]))
    try:
        # first time voter/new user handling
        if not 'voted' in request.session:
            request.session['voted'] = []
        poll = Poll.objects.get(pk=poll_id)
        vote_form = VoteForm(poll, data=request.POST)
        # already voted
        if poll.id in request.session['voted']:
            context = {
                'poll': poll,
                'vote_form': vote_form,
                'error_message': "You already voted!"
            }
            return render(request, "polls/poll.html", context)
        elif vote_form.is_valid():
            selected_choice = Choice.objects.get(pk=vote_form.cleaned_data['choice'])
            selected_choice.votes += 1
            selected_choice.save()
            # remember to record the vote took place
            request.session['voted'].append(poll.id)
            request.session.modified = True
            return HttpResponseRedirect(reverse("polls:results", args=[poll_id]))
        else:
            context = {
                'poll': poll,
                'vote_form': vote_form
            }
            return render(request, "polls/poll.html", context)

    except Poll.DoesNotExist:
        return render(request, "polls/poll.html", status=404)

def results(request, poll_id):
    context = {}
    retcode = 200
    try:
        poll = Poll.objects.get(pk=poll_id)
        context['poll'] = poll
        votes = poll.choice_set.aggregate(total=Sum('votes'))
        context['total_votes'] = max(1, votes['total'])
    except Poll.DoesNotExist:
        retcode = 404
    return render(request, "polls/results.html", context, status=retcode)

def new_poll(request):
    if request.method == 'GET':
        # User wants to create new poll
        context = {
            'form': NewPollForm()
         }
        return render(request, "polls/new.html", context)
    else:
        form = NewPollForm(request.POST)
        if form.is_valid() and choices_valid(form.cleaned_data['choices']):
            # Adding new poll based on form data
            topic = form.cleaned_data['topic']
            open_polls.append(topic)
            open_polls[topic] = {
                'question': form.cleaned_data['question'],
                'options': [
                    {
                        'text': choice,
                        'votes': 0,
                    } for choice in form.cleaned_data['choices']
                ],
            }
            return HttpResponseRedirect(reverse("polls:vote", args=[topic]))
        else:
            # Errors in form, render errors to user
            context = {
                'form': form,
            }
            if form.is_valid() and not choices_valid(form.cleaned_data['choices']):
                context['error_message'] = 'Correct the form of Choices field'
            return render(request, "polls/new.html", context)

def choices_valid(choices):
    return isinstance(choices, list) and all(isinstance(val, str) for val in choices)
