from django.contrib import admin
from .models import Post, Comments

@admin.register(Post)                  #Регистрируем модель Post
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')    #Создаем кортеж для отображения их

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'post')