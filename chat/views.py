from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from .models import Friendship, Message

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}, tu cuenta ha sido creada con éxito.")
            return redirect('chat_home')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = RegistrationForm()
    return render(request, 'chat/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido de nuevo {user.username}!")
                return redirect('chat_home')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = LoginForm()
    return render(request, 'chat/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')

@login_required
def chat_home(request):
    user = request.user
    friendships = Friendship.objects.filter(sender=user, status='accepted') | Friendship.objects.filter(receiver=user, status='accepted')
    friends = []
    for friendship in friendships:
        if friendship.sender == user:
            friends.append(friendship.receiver)
        else:
            friends.append(friendship.sender)

    # Obtener mensajes no leídos
    unread_messages = Message.objects.filter(recipient=user, is_read=False)

    pending_requests = Friendship.objects.filter(receiver=user, status='pending')
    users = User.objects.exclude(id=user.id).exclude(id__in=[friend.id for friend in friends])

    return render(request, 'chat/chat_room.html', {
        'friends': friends,
        'pending_requests': pending_requests,
        'users': users,
        'unread_messages': unread_messages
    })

@login_required
def accept_friend(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id)
    if friendship.receiver == request.user:
        friendship.status = 'accepted'
        friendship.save()
        messages.success(request, "Solicitud de amistad aceptada.")
    return redirect('chat_home')

@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    Friendship.objects.create(sender=request.user, receiver=receiver, status='pending')
    messages.success(request, f"Solicitud de amistad enviada a {receiver.username}.")
    return redirect('chat_home')

@login_required
def chat_with_friend(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)

    # Marcar los mensajes no leídos como leídos cuando el usuario abre el chat
    Message.objects.filter(sender=friend, recipient=request.user, is_read=False).update(is_read=True)

    return render(request, 'chat/chat_with_friend.html', {
        'friend': friend
    })
