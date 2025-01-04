from django.db import models

class Post(models.Model):        #обращаемся к родительному классу Model, чтобы наследовать настройки
    '''данные о посте'''
    title = models.CharField('Заголовок записи', max_length=100)
    description = models.TextField('Текст запсии')
    author = models.CharField('Имя автора', max_length=100)
    date = models.DateField('Дата публикации')
    img = models.ImageField('Изображение', upload_to='image/%Y')
    def __str__(self):         #Отображаем в списке модели в админ панели
        return f'{self.title}, {self.author}'

    class Meta:                 #Создаем класс для определения различных вещей о модели
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

class Comments(models.Model):              #Создаем класс для комментов
    '''Комментарий'''
    email = models.EmailField()
    name = models.CharField('Имя', max_length=50)
    text_comments = models.TextField('Текст комментария', max_length=2000)
    post = models.ForeignKey(Post, verbose_name='Публикация', on_delete=models.CASCADE)    #Связываем две таблицы

    def __str__(self):         #Отображаем в списке модели в админ панели
        return f'{self.name}, {self.post}'

    class Meta:                 #Создаем класс для определения различных вещей о модели
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Likes(models.Model):
    '''лайки'''
    ip = models.CharField('ip-adres', max_length=100)
    pos = models.ForeignKey(Post, verbose_name='Публикация', on_delete=models.CASCADE)