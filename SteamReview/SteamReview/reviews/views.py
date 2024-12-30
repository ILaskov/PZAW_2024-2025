from django.shortcuts import render, redirect, get_object_or_404
from .forms import AppSelectForm, RegistrationForm
import requests, markdown, hashlib
from .models import Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

#Creating main page with all reviews ordered by date
def index(request):
    reviews = Review.objects.all().order_by('-timestamp')
    return render(request, 'index.html', {'reviews': reviews})

#Creating page where you make reviews
@login_required
def newReview(request):
    search_query = request.GET.get('q', '')
    form = AppSelectForm(search_query=search_query)
    game_details = None
    formatted_text = None
    rating = None

    if request.method == 'POST':
        #Showing game details after selecting game
        if 'app_choice' in request.POST:
            app_id = request.POST.get('app_choice')

            if app_id:
                #Getting data from steam site to then display on mine site
                url = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    api_data = response.json()
                    game_details = api_data.get(app_id, {}).get('data', {})
                except requests.RequestException as e:
                    game_details = {'error': str(e)}

                #Returning page with game details
                return render(request, 'newReview.html', {
                    'form': form,
                    'game_details': game_details,
                    'app_id': app_id,
                })
        else:
            #Getting what game was selected
            app_id = request.POST.get('app_id')
            review_text = request.POST.get('review_text')
            rating = request.POST.get('rating')

            if review_text:
                formatted_text = markdown.markdown(review_text)

                #Creating a review object from models.py to store in database
                if app_id:
                    # Getting data from my site and steam site to make review object
                    url = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
                    try:
                        response = requests.get(url, timeout=10)
                        response.raise_for_status()
                        api_data = response.json()
                        game_details = api_data.get(app_id, {}).get('data', {})
                        app_name = game_details.get('name')
                        app_developers = ', '.join(game_details.get('developers', []))
                        image_url = game_details.get('header_image')
                        user = request.user
                    except requests.RequestException as e:
                        game_details = {'error': str(e)}

                    #Creating review object
                    review = Review.objects.create(
                        app_id=app_id,
                        app_name=app_name,
                        app_developers=app_developers,
                        image_url=image_url,
                        review_text=formatted_text,
                        rating=rating,
                        user=user,
                    )

                    #Redirect to page with review
                    return redirect('review_detail', pk=review.pk)

    #Rendering page with all data
    return render(request, 'newReview.html', {
        'form': form,
        'game_details': game_details,
        'formatted_text': formatted_text,
        'rating': rating
    })

#Creating a site with posted review
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.app_id:
        # Getting data from steam site to then display on mine site
        url = f"http://store.steampowered.com/api/appdetails?appids={review.app_id}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            api_data = response.json()
            game_details = api_data.get(review.app_id, {}).get('data', {})
        except requests.RequestException as e:
            game_details = {'error': str(e)}

    #Rendering site with all necessary data
    return render(request, 'review.html', {'review': review, 'game_details':game_details})

#Creating a site that user can register in
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        #Checks if everything was filled
        if not username or not password or not confirm_password:
            return render(request, 'register.html', {'error': 'All fields are required.'})

        #Checks if passwords match
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})

        #Checks if the username is already taken
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists.'})

        #Create a new user with hashed password
        user = User.objects.create(
            username=username,
            #Hashing the password
            password=make_password(password)
        )
        user.save()

        #Redirect to the login page after successful registration
        return redirect('login')
    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            #Log the user in
            login(request, user)
            #Redirect to the home page
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request, 'login.html')
