from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),       # Página principal del chat
    path('register/', views.register, name='register'), # Registro de usuario
    path('login/', views.login_view, name='login'),     # Inicio de sesión
    path('logout/', views.logout_view, name='logout'),  # Cerrar sesión
    path('accept_friend/<int:friendship_id>/', views.accept_friend, name='accept_friend'),  # Aceptar solicitud
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),  # Enviar solicitud de amistad
    path('chat/<int:friend_id>/', views.chat_with_friend, name='chat_friend'),  # Chatear con un amigo
]
