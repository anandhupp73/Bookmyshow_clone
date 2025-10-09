from django.db import models

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

    def str(self):
        return f"{self.name} - {self.role}"


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100)
    rating = models.IntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user_name} - {self.movie.title}"