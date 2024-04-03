from django.shortcuts import render,redirect
from django.utils.dateparse import parse_datetime
from .models import User, Movie, Ratings,IDS
from django.http import HttpResponse
from django.urls import reverse
import datetime
from statistics import mean
def get_id(type):
    ids = IDS.objects.all()
    if ids:
        if type == 'movie':
            return ids[0].movie_id
        elif type == 'user':
            return ids[0].user_id
        elif type == 'rating':
            return ids[0].rating_id
        else:
            return None
def update_id(type,val):
    val += 1
    ids = IDS.objects.all()
    if ids:
        if type == 'movie':
            ids[0].movie_id = val
            ids[0].save()
        elif type == 'user':
            ids[0].user_id = val
            ids[0].save()
        elif type == 'rating':
            ids[0].rating_id = val
            ids[0].save()
        else:
            return None
def get_average_rating(movie_id):
    try:
        return mean([current_rating.rating for current_rating in Ratings.objects.filter(movie_id=movie_id)])
    except Exception as e:
        print(e)

def home(request):
    ratings = ['G','PG','PG-13','R','N-17']
    genre = ['Comedy', 'Horror','Action','Drama', 'Thriller','Romance','Crime']
    ids = IDS.objects.all()
    if not ids:
        ids = IDS()
        ids.save()
    movies = Movie.objects.all()
    all_movies= []

    for movie in movies:
        current_movie_id = movie.id
        current_movie_average_rating = get_average_rating(current_movie_id)
        all_movies.append({'id':current_movie_id,'name':str(movie.name).title(),'genre':movie.genre,'rating':movie.rating,'release_date':str(movie.release_date),'average_rating':current_movie_average_rating})
    print(all_movies)
    return render(request,'home.html',{'ratings':ratings,'genre':genre,'all_movies':all_movies})
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user_id = get_id('user')
        try:
            new_user = User(id = user_id,name=name,email=email,phone=phone,password=password)
            new_user.save()
            request.session['user'] = True
            request.session['user_id'] = new_user.id
            update_id('user',user_id)
            return redirect('home')
        except Exception as e:
            print("Error:", e)



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if user:
                if password == user.password:
                    request.session['user'] = True
                    request.session['user_id'] = user.id
                    return redirect('home')
                else:
                    pass
        except Exception as e:
            print("Error:", e)

def logout(request):
    if request.method == 'POST':
        if 'user' in request.session:
            request.session.pop('user')
            request.session.pop('user_id')
            return redirect('home')

def add(request):
    if request.method == 'POST':
        name = str(request.POST.get('name')).lower()
        genre = request.POST.get('genre')
        ratings = request.POST.get('ratings')
        release_date = request.POST.get('date')
        release_date = datetime.datetime.strptime(release_date, '%m-%d-%Y').strftime('%Y-%m-%d')
        rating = request.POST.get('rate')
        movie_id = get_id('movie')
        rating_id = get_id('rating')
        try:
            new_movie = Movie(id = movie_id,name=name,genre=genre,rating=ratings,release_date=release_date)
            new_movie.save()
            update_id('movie',movie_id)
            new_rating = Ratings(id=rating_id,movie_id=new_movie,user_id = User.objects.get(id = request.session['user_id']),rating=float(rating))
            new_rating.save()
            update_id('rating',rating_id)
            return redirect('home')
        except Exception as e:
            print("Error:", e)
def add_rating(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        rating = request.POST.get('rating')
        rating_id = get_id('rating')
        try:
            movie = Movie.objects.get(id=movie_id)
            new_rating = Ratings(id=rating_id, movie_id=movie, user_id=User.objects.get(id=request.session['user_id']),rating=float(rating))
            new_rating.save()
        except Exception as e:
            print("Error:", e)
def search_movie(request):
    if request.method == 'POST':
        name = str(request.POST.get('search_movie')).lower()
        movie = Movie.objects.get(name=name)
        if movie:
            current_movie_id = movie.id
            current_movie_average_rating = get_average_rating(current_movie_id)
            movie = {'id':current_movie_id,'name':str(movie.name).title(),'Genre':movie.genre,'Rated':movie.rating,'Release_date':str(movie.release_date),'Average_rating':current_movie_average_rating}
            return render(request,'movie.html',{'movie':movie})
    if request.method == 'GET':
        movie_id = request.GET['id']










