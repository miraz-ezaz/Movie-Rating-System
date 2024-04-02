from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True,unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    password = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Movie(models.Model):
    id = models.IntegerField(primary_key=True,unique=True)
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    ratings = models.CharField(max_length=10)
    release_date = models.DateField()

    def __str__(self):
        return self.name

class Rating(models.Model):
    id = models.IntegerField(primary_key=True,unique=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie,on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    def __str__(self):
        return f"{self.user_id} rated {self.movie_id} {self.rating}"
