from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.http import HttpResponse,FileResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.db.models import Avg, Count
from django.core.mail import send_mail
from django.conf import settings
from weasyprint import HTML
from django.template.loader import render_to_string,get_template
import io
import qrcode
from django.core.files.base import ContentFile
import base64




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


@admin_required
def admin_dashboard(request):
    
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

@admin_required
def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        movie.title = request.POST.get('title', movie.title)
        movie.description = request.POST.get('description', movie.description)
        movie.release_date = request.POST.get('release_date', movie.release_date)
        movie.duration = request.POST.get('duration', movie.duration)
        movie.language = request.POST.get('language', movie.language)
        movie.genre = request.POST.get('genre', movie.genre)

        if 'main_image' in request.FILES:
            movie.main_image = request.FILES['main_image']
        if 'cover_image' in request.FILES:
            movie.cover_image = request.FILES['cover_image']

        movie.save()
        messages.success(request, f"Movie '{movie.title}' updated successfully!")
        return redirect('view_movies')

    return render(request, 'adminpanel/update_movie.html', {'movie': movie})

@admin_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        # Manually delete related objects before deleting movie
        movie.reviews.all().delete()
        movie.castcrew.all().delete()
        movie.seats.all().delete()
        Wishlist.objects.filter(movie=movie).delete()
        Booking.objects.filter(movie=movie).delete()

        movie.delete()
        messages.success(request, f"'{movie.title}' and all related data have been deleted successfully.")
        return redirect('view_movies')

    messages.error(request, "Invalid request.")
    return redirect('view_movies')

# ======== USER SECTION ========


def movie_booking(request,id):
    movie = get_object_or_404(Movie, id=id)
    reviews = movie.reviews.all().order_by('-created_at')
    rating_info = movie.reviews.aggregate(avg_rating=Avg('rating'), total_votes=Count('id'))
    
    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(user=request.user, movie=movie).exists()

    return render(request,'users/movie_booking.html',{'movie':movie,'reviews':reviews,'avg_rating': rating_info['avg_rating'],
        'total_votes': rating_info['total_votes'],'is_wishlisted': is_wishlisted,})
    
@login_required
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


@login_required
def toggle_wishlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, movie=movie)

    if not created:
        # Already exists, so remove it
        wishlist_item.delete()
        messages.success(request, "Removed from your wishlist.")
    else:
        messages.success(request, "Added to your wishlist.")

    return redirect('movie_booking', id=movie.id)


@login_required
def user_wishlist(request):
    wishlist_items = request.user.wishlist.select_related('movie').all()
    # Extract movies from wishlist entries
    movies = [item.movie for item in wishlist_items]
    print(movies)
    return render(request, 'users/wish_movies.html', {'movies': movies})

#creating seats for booking

def create_seats_for_movie(movie, rows=5, seats_per_row=10):
    for row in range(rows):
        for seat_num in range(1, seats_per_row + 1):
            seat_label = f"{chr(65 + row)}{seat_num}"  # e.g., A1, B2
            Seat.objects.create(movie=movie, seat_number=seat_label)

@login_required
def book_seats(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Create seats automatically if none exist
    if not movie.seats.exists():
        create_seats_for_movie(movie, rows=5, seats_per_row=10)

    seats = movie.seats.all().order_by('seat_number')

    if request.method == 'POST':
        selected_seat_ids = request.POST.getlist('seats')

        already_booked = Seat.objects.filter(id__in=selected_seat_ids, is_booked=True)
        if already_booked.exists():
            messages.error(request, "Some selected seats are already booked. Please choose different seats.")
            return redirect('book_seats', movie_id=movie.id)

        seats_to_book = Seat.objects.filter(id__in=selected_seat_ids)
        seats_to_book.update(is_booked=True)

        booking = Booking.objects.create(user=request.user, movie=movie)
        booking.seats.set(seats_to_book)
        booking.save()
        
        
        # ===== Send email to user =====
        seat_numbers = ", ".join([seat.seat_number for seat in seats_to_book])
        subject = f"Your seats for {movie.title} are booked!"
        message = f"Hello {request.user.username},\n\n" \
                  f"You have successfully booked the following seats for {movie.title}:\n" \
                  f"{seat_numbers}\n\n" \
                  f"Enjoy the movie!\n\nRegards,\nMovie Booking Team"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL, 
            [request.user.email],
            fail_silently=False
        )

        messages.success(request, f"Successfully booked {len(selected_seat_ids)} seats.")
        return redirect('booking_confirmation', booking_id=booking.id)

    return render(request, 'users/book_seats.html', {'movie': movie, 'seats': seats})

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'users/booking_conform.html', {'booking': booking})

# <--------TICKET PDF -------->

@login_required
def generate_ticket_pdf(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    movie = booking.movie

    # --- QR Code ---
    qr_text = (
        f"🎬 Movie: {movie.title}\n"
        f"💺 Seats: {', '.join([seat.seat_number for seat in booking.seats.all()])}\n"
        f"🗓 Date: {booking.booked_at.strftime('%Y-%m-%d')}\n"
        f"🎫 Booking ID: {booking.id}"
    )
    qr_image = qrcode.make(qr_text)
    qr_io = io.BytesIO()
    qr_image.save(qr_io, format="PNG")
    qr_base64 = base64.b64encode(qr_io.getvalue()).decode()

    # --- Movie Poster ---
    if movie.main_image:
        with open(movie.main_image.path, "rb") as f:
            movie_poster = base64.b64encode(f.read()).decode()
        movie_poster = f"data:image/jpeg;base64,{movie_poster}"
    else:
        movie_poster = "https://via.placeholder.com/350x180.png?text=No+Image"

    # --- Render HTML with Context ---
    html_string = render_to_string("users/ticket.html", {
        "movie_title": movie.title,
        "movie_type": movie.genre,
        "language": movie.language,
        "show_date": booking.booked_at.strftime("%d %b %Y"),
        "show_time": "07:30 PM",  # Replace with real field if available
        "theatre_name": "PVR Cinemas",
        "screen": "Screen 3",
        "seat": ", ".join([seat.seat_number for seat in booking.seats.all()]),
        "booking_id": booking.id,
        "total_amount": "₹500.00",
        "movie_poster": movie_poster,
        "qr_code": qr_base64,
    })

    # --- Generate PDF ---
    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri()
    ).write_pdf()

    # --- Return as downloadable file ---
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{movie.title}_ticket.pdf"'
    return response