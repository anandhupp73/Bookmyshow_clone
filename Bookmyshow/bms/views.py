from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import user_passes_test,login_required
from functools import wraps
from django.db.models import Avg, Count

# Create your views here.

def home(request):
    movies = Movie.objects.all()
    return render(request,'home.html',{'movies':movies})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:  
                login(request, user)
                request.session['is_admin_logged_in'] = True
                return redirect('admin_dashboard')  # your custom dashboard view
            else:
                messages.error(request, 'You are not authorized to access admin panel.')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'adminpanel/login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def is_admin_user(user):
    return user.is_authenticated and user.is_staff       #restricted to logged-in staff users:


#Custom Decorator for Admin Panel Access
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, "You must login as admin to access this page.")
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


# @login_required(login_url='/admin-login/')
# @user_passes_test(is_admin_user,login_url='/admin-login/')
@admin_required
def admin_dashboard(request):
    # if not request.user.is_authenticated:
    #     return redirect('admin_login')
    
    movie_count = Movie.objects.count()
    cast_count = CastCrew.objects.count()
    review_count = Review.objects.count()
    return render(request, 'adminpanel/dashboard.html', {
        'movie_count': movie_count,
        'cast_count': cast_count,
        'review_count': review_count
    })

@admin_required
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


@admin_required
def view_movies(request):
    movies = Movie.objects.all().order_by('-release_date')
    return render(request, 'adminpanel/view_movies.html', {'movies': movies})

@admin_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'adminpanel/movie_detail.html', {'movie': movie})

@admin_required
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

@admin_required
def view_reviews(request):
    reviews = Review.objects.all().select_related('movie').order_by('-created_at')
    return render(request, 'adminpanel/view_reviews.html', {'reviews': reviews})


# ======== USER SECTION ========

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('user_login')
    
    return render(request, 'users/user_register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['is_user_logged_in'] = True
            return redirect('home')
        else:
            return render(request, 'users/user_login.html', {'error': 'Invalid credentials'})
    return render(request,'users/user_login.html')


def user_logout(request):
    if 'is_user_logged_in' in request.session:
        del request.session['is_user_logged_in']
    return redirect('home')

def movie_booking(request,id):
    movie = get_object_or_404(Movie, id=id)
    reviews = movie.reviews.all().order_by('-created_at')
    rating_info = movie.reviews.aggregate(avg_rating=Avg('rating'), total_votes=Count('id'))

    return render(request,'users/movie_booking.html',{'movie':movie,'reviews':reviews,'avg_rating': rating_info['avg_rating'],
        'total_votes': rating_info['total_votes'],})

def add_review(request,id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            movie=movie,
            user_name=user_name,
            rating=rating,
            comment=comment
        )

        return redirect('movie_booking',id=movie.id) 


    return render(request,'users/add_review.html',{'movie':movie})