from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.CharField(max_length=50, default="N/A")
    language = models.CharField(max_length=50, default="Unknown")
    genre = models.CharField(max_length=100, default="Uncategorized")

    main_image = models.ImageField(upload_to='movies/main_images/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='movies/cover_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class CastCrew(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='castcrew')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='castcrew/profile_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.role}"


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100)
    rating = models.IntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.movie.title}"
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    

# FOR -- BOOKING -- TICKETS

# class Show(models.Model):
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
#     show_date = models.DateField()
#     show_time = models.TimeField()

    # def __str__(self):
    #     return f"{self.movie.title} on {self.show_date} at {self.show_time}"


class Seat(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)  # e.g., "A1", "B3"
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat_number} - {'Booked' if self.is_booked else 'Available'}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE ,default=1)
    seats = models.ManyToManyField(Seat)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.seats.count()} seat(s) for {self.movie.title}"