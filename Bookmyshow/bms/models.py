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

class Theatre(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    total_screens = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f"{self.name} - {self.location}"

class Screen(models.Model):
    theatre = models.ForeignKey(Theatre,on_delete=models.CASCADE,related_name="screens")
    screen_number = models.CharField(max_length=10)
    total_seats = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f"{self.theatre.name} - Screen{self.screen_number}"
    
class Show(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="shows")
    theatre = models.ForeignKey(Theatre,on_delete=models.CASCADE,related_name="shows")
    screen = models.ForeignKey(Screen,on_delete=models.CASCADE)
    show_time = models.TimeField()
    show_date = models.DateField()
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.movie.title} @ {self.theatre.name} - {self.show_time}"

class Seat(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)  # e.g., "A1", "B3"
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat_number} - {self.show}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True, blank=True)  # allow null temporarily
    seats = models.ManyToManyField(Seat)
    booked_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} booked {self.seats.count()} seat(s) for {self.show.movie.title}"