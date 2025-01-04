from django.urls import path
from . import views
from django.urls import path
from .views import log_to_file, PostListCreateView

urlpatterns = [path('', views.PostView.as_view()),
               path('<int:pk>/', views.PostDetail.as_view()),
               path('review/<int:pk>/', views.AddComments.as_view(), name='addcomments'),
               path('<int:pk>/add_likes/', views.AddLike.as_view(), name='add_likes'),
               path('<int:pk>/del_likes/', views.DelLike.as_view(), name='del_likes'),
               path('log/', log_to_file, name='log_to_file'),
               path('api/posts/', PostListCreateView.as_view(), name='post-list-create')]                   #Cоздаем списк где будут все пути для наших url