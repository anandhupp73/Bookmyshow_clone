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

    #for theatre management admin

    path('admin-panel/add-theatre/', views.add_theatre, name='add_theatre'),
    path('admin-panel/view-theatres/', views.view_theatres, name='view_theatres'),
    path('admin-panel/add-screen/', views.add_screen, name='add_screen'),
    path('admin-panel/add-show/', views.add_show, name='add_show'),
    path('admin-panel/view-shows/', views.view_shows, name='view_shows'),

    #-------------------------

    path('admin-panel/movie-detail/<int:movie_id>/',views.movie_detail,name='movie_details'),
    path('admin-panel/movies/<int:movie_id>/edit/', views.update_movie, name='update_movie'),
    path('admin-panel/movies/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),

    #for users 

    path('movie-booking/<int:id>/',views.movie_booking,name='movie_booking'),
    path('movie/add-review/<int:id>/',views.add_review,name='add_review'),
    path('wishlist/toggle/<int:movie_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('my-wishlist/', views.user_wishlist, name='user_wishlist'),
    path('movie/<int:movie_id>/select-theatre/', views.select_theatre, name='select_theatre'),
    path('movie/<int:movie_id>/select-show/<int:theatre_id>/', views.select_show, name='select_show'),
    path('book/<int:show_id>/', views.book_seats, name='book_seats'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('ticket/<int:booking_id>',views.generate_ticket_pdf, name='download_ticket'),

]