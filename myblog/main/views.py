from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.core.serializers import serialize
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import request
from django.shortcuts import redirect
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
from rest_framework.response import Response
from rest_framework.views import APIView
import os

from .tasks import parse_tweet

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from .models import Blog, GoogleUser
from rest_framework import generics
from .serializer import BlogSerializer
# Create your views here.
def toMain(request):
    user = request.user
    post = Blog.objects.order_by('-date')
    #parse_tweet()
    parse_tweet.delay()

    return render(request, 'main/blogs.html', {'post': post, 'user': user})

def toCurrent(request, blog_id):
    username = request.user.username if request.user.is_authenticated else 'Гость'
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'main/currentblog.html', {'blog': blog, 'username': username})
def toLogin(request):

    if request.POST:
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user=user)

            return redirect('home')
    return render(request, 'main/login.html')
def toLogout(request):
    logout(request)
    return redirect('home')






BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'secrets/client_secret.json')
def google_auth(request):
    # Initialize the OAuth flow
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri=request.build_absolute_uri('/oauth2callback/')
    )

    # Generate the authorization URL
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    # Save the state in the session for later verification
    request.session['state'] = state

    # Redirect the user to the authorization URL
    return redirect(authorization_url)

def oauth2callback(request):
    state = request.session.get('state')

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile'],
        state=state,
        redirect_uri=request.build_absolute_uri('/oauth2callback/')
    )

    # Получаем токен
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    # Получаем учетные данные
    credentials = flow.credentials

    # Используем учетные данные для получения информации о пользователе
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()

    # Сохраняем или обновляем пользователя в базе данных
    user, created = GoogleUser.objects.update_or_create(
        google_id=user_info['id'],  # Уникальный идентификатор Google
        defaults={
            'email': user_info['email'],
            'name': user_info['name'],
            'profile_picture': user_info.get('picture')  # Может быть отсутствует
        }
    )

    # Вы можете сохранить информацию о пользователе в сессии, если это необходимо
    request.session['user_id'] = user.id

    # Перенаправляем пользователя на главную страницу
    return redirect('/')




















class BlogAPIView(APIView):
    def get(self, request):
        b = Blog.objects.all()
        return Response({'Blogs': BlogSerializer(b, many =True).data})

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        blog_new = serializer.create(serializer.validated_data)
        return Response({'blog': BlogSerializer(blog_new).data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk",None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Blog.objects.get(pk=pk)
        except:
            return Response({"error": "Object doesn't exists"})

        serializer = BlogSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"blog": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error", "Method DELETE not allowed"})

        try:
            instance = Blog.objects.get(pk=pk)
            instance.delete()
        except:
            return Response({"ERROR": "Object Not Found !"})

        return Response({"post": "delete post" + str(pk)})




#class BlogAPIView(generics.ListAPIView):
#    queryset = Blog.objects.all()
#    serializer_class = BlogSerializer
#restful api сервер + salary брокер. + комментарии и лайки на пользователе, авторизация через сторонние сервисы  .