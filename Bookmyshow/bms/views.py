from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,'home.html')

def movies(request):
    return render(request,'movie.html')

def admin_dashboard(request):
    movie_count = Movie.objects.count()
    cast_count = CastCrew.objects.count()
    review_count = Review.objects.count()
    return render(request, 'adminpanel/dashboard.html', {
        'movie_count': movie_count,
        'cast_count': cast_count,
        'review_count': review_count
    })


def add_movie(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        release_date = request.POST['release_date']
        duration = request.POST['duration']
        language = request.POST['language']
        genre = request.POST['genre']
        main_image = request.FILES.get('main_image')
        cover_image = request.FILES.get('cover_image')

        Movie.objects.create(
            title=title,
            description=description,
            release_date=release_date,
            duration=duration,
            language=language,
            genre=genre,
            main_image=main_image,
            cover_image=cover_image
        )
        messages.success(request, 'Movie added successfully')
        return redirect('view_movies')
    return render(request, 'adminpanel/add_movie.html')


def view_movies(request):
    movies = Movie.objects.all().order_by('-release_date')
    return render(request, 'adminpanel/view_movies.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'adminpanel/movie_detail.html', {'movie': movie})


def add_castcrew(request):
    movies = Movie.objects.all()
    if request.method == 'POST':
        movie_id = request.POST['movie']
        name = request.POST['name']
        role = request.POST['role']
        profile_image = request.FILES.get('profile_image')
        CastCrew.objects.create(
            movie_id=movie_id,
            name=name,
            role=role,
            profile_image=profile_image
        )
        messages.success(request,'Cast/Crew added succesfully')
        return redirect('view_movies')
    return render(request, 'adminpanel/add_castcrew.html', {'movies': movies})


def view_reviews(request):
    reviews = Review.objects.all().select_related('movie')
    return render(request, 'adminpanel/view_reviews.html', {'reviews': reviews})