from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Likes
from .form import CommentsForm
from rest_framework import generics
from .serializers import PostSerializer
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def log_to_file(request):
    if request.method == 'POST':
        try:
            data = request.POST
            log_level = data.get('level', 'INFO')
            log_message = data.get('message', '')

            # Определите уровень логирования в соответствии с вашими требованиями
            if log_level == 'INFO':
                logger.info(log_message)
            elif log_level == 'ERROR':
                logger.error(log_message)
            else:
                logger.debug(log_message)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

class PostView(View):
    '''вывод записей'''

    def get(self, request):
        try:
            posts = Post.objects.all()  # ссылаемся на всю информацию из нашей таблицы
            return render(request, 'blog/blog.html', {'post_list': posts})
        except Exception as e:
            # Обработка ошибок при выполнении запроса к базе данных
            error_message = f'An error occurred while fetching posts: {str(e)}'
            return HttpResponseServerError(error_message)

class PostDetail(View):
    '''отдельная страница записи'''
    def get(self, request, pk):             #получаем id конкретной записи
        post = Post.objects.get(id=pk)
        return render(request, 'blog/blog_detail.html', {'post' : post})

class AddComments(View):
    '''Добавление комментариев'''
    def post(self, request, pk):
        form = CommentsForm(request.POST)
        if form.is_valid():                  #проверяем валидность
            form = form.save(commit=False)
            form.post_id = pk
            form.save()
        return redirect(f'/{pk}')

def get_client_ip(request):
    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')   #Храним ip-адрес клиента
    if x_forward_for:
        ip = x_forward_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        return ip

class AddLike(View):
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        try:
            Likes.objects.get(ip=ip_client, pos_id=pk)
            return redirect(f'/{pk}')
        except:
            new_like = Likes()
            new_like.ip = ip_client
            new_like.pos_id = int(pk)
            new_like.save()
            return redirect(f'/{pk}')

class DelLike(View):
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        try:
            lik = Likes.objects.get(ip=ip_client)
            lik.delete()
            return redirect(f'/{pk}')
        except:
            return redirect(f'/{pk}')

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer