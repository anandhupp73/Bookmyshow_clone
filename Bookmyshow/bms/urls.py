from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    
    #for admin
    
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/',views.admin_logout,name='admin_logout'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/add-movie/', views.add_movie, name='add_movie'),
    path('admin-panel/view-movies/', views.view_movies, name='view_movies'),
    path('admin-panel/add-castcrew/', views.add_castcrew, name='add_castcrew'),
    path('admin-panel/view-reviews/', views.view_reviews, name='view_reviews'),
    path('admin-panel/movie-detail/<int:movie_id>/',views.movie_detail,name='movie_details'),

    #for users 

    path('movie-booking/<int:id>/',views.movie_booking,name='movie_booking'),
    path('add-review/<int:id>/',views.add_review,name='add_review'),
    path('wishlist/toggle/<int:movie_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('my-wishlist/', views.user_wishlist, name='user_wishlist'),
    path('book-seats/<int:movie_id>/', views.book_seats, name='book_seats'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('ticket/<int:booking_id>/download/', views.download_ticket, name='download_ticket'),


]