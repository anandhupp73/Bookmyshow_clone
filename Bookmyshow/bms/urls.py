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
]