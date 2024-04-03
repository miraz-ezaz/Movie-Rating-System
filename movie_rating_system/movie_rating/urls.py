from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('add/',views.add,name='add'),
    path('search/',views.search_movie,name='search'),
    path('search/<id>',views.search_movie,name='search_id'),
    path('addrating/',views.add_rating,name='addrating'),


]