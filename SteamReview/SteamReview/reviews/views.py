from django.shortcuts import render, redirect, get_object_or_404
from .forms import AppSelectForm
import requests, markdown
from .models import Review

#Creating main page with all reviews ordered by date
def index(request):
    reviews = Review.objects.all().order_by('-timestamp')
    return render(request, 'index.html', {'reviews': reviews})

#Creating page where you make reviews
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
