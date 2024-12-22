from django.shortcuts import render, redirect, get_object_or_404
from .forms import AppSelectForm
import requests, markdown
from .models import Review

def index(request):
    photo_data = {
        'photo_1': 'https://picsum.photos/seed/1/300/200',
        'photo_2': 'https://picsum.photos/seed/2/300/400',
        'photo_3': 'https://picsum.photos/seed/3/300/300',
        'photo_4': 'https://picsum.photos/seed/4/300/300',
        'photo_5': 'https://picsum.photos/seed/5/300/300',
        'photo_6': 'https://picsum.photos/seed/6/300/300',
        'photo_7': 'https://picsum.photos/seed/7/300/400',
        'photo_8': 'https://picsum.photos/seed/8/300/300',
        'photo_9': 'https://picsum.photos/seed/9/300/200',
        'photo_10': 'https://picsum.photos/seed/10/300/100',
        'photo_11': 'https://picsum.photos/seed/11/300/400',
        'photo_12': 'https://picsum.photos/seed/12/300/400',
    }
    return render(request, 'index.html', photo_data)

def newReview(request):
    search_query = request.GET.get('q', '')
    form = AppSelectForm(search_query=search_query)
    game_details = None
    formatted_text = None
    # rating = None

    if request.method == 'POST':
        if 'app_choice' in request.POST:
            app_id = request.POST.get('app_choice')

            if app_id:
                url = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    api_data = response.json()
                    game_details = api_data.get(app_id, {}).get('data', {})
                except requests.RequestException as e:
                    game_details = {'error': str(e)}

                return render(request, 'newReview.html', {
                    'form': form,
                    'game_details': game_details,
                    'app_id': app_id,
                })
        else:
            app_id = request.POST.get('app_id')
            review_text = request.POST.get('review_text')
            # rating = request.POST.get('rating')

            if review_text:
                formatted_text = markdown.markdown(review_text)

                review = Review.objects.create(
                    app_id=app_id,
                    review_text=formatted_text,
                    # rating=rating,
                )
                return redirect('review_detail', pk=review.pk)

    return render(request, 'newReview.html', {
        'form': form,
        'game_details': game_details,
        'formatted_text': formatted_text,
        # 'rating': rating
    })

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.app_id:
        url = f"http://store.steampowered.com/api/appdetails?appids={review.app_id}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            api_data = response.json()
            game_details = api_data.get(review.app_id, {}).get('data', {})
        except requests.RequestException as e:
            game_details = {'error': str(e)}

    return render(request, 'review.html', {'review': review, 'game_details':game_details})
