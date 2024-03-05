from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createUser/', views.createUser, name='createUser'),
    path('reconhecimento_facial/', views.reconhecimento_facial, name='reconhecimento_facial'),
    path('adicionar-pessoa/', views.adicionar_pessoa, name='adicionar_pessoa'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('registros/', views.registos, name='registros'),
    path('filtroRegistos/', views.listar_registros, name='listar_registros'),
    path('estacao/', views.estacaoForms, name='estacaoForms'),
    path('estacao/create/', views.estacao_create, name='estacao_create'),
    path('read_pessoa/', views.listPessoas, name='read_pessoa'),
    path('update/<int:pk>/', views.update_pessoa, name='update_pessoa'),
    path('delete/<int:pk>/', views.delete_pessoa, name='delete_pessoa'),


]
