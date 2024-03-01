from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createUser/', views.createUser, name='createUser'),
    path('reconhecimento_facial/', views.reconhecimento_facial, name='reconhecimento_facial'),
    path('adicionar-pessoa/', views.adicionar_pessoa, name='adicionar_pessoa'),
    path('video_feed/', views.video_feed, name='video_feed'),

]
