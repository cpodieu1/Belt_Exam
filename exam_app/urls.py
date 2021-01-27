from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('wishes', views.wishes),
    path('hacker', views.hacker),
    path('new', views.new),
    path('edit/<int:id>', views.edit),
    path('stats', views.stats),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('new_wish', views.new_wish),
    path('grant', views.grant),
    path('update/<int:id>', views.update),
    path('delete', views.delete),
    # path('process_likes', views.likes)
]