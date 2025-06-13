from django.contrib import admin
from .models import Vacation, Like


@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ['country', 'start_date', 'end_date', 'price', 'likes_count']
    list_filter = ['country', 'start_date', 'price']
    search_fields = ['description', 'country__name']
    ordering = ['start_date']

    def likes_count(self, obj):
        return obj.likes_count

    likes_count.short_description = 'Likes'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'vacation', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'vacation__country__name']