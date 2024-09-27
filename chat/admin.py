from django.contrib import admin
from .models import Friendship, Message

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'timestamp')

admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(Message, MessageAdmin)

