from django.contrib import admin

from .models import FavoriteLine

class FavoriteLineAdmin(admin.ModelAdmin):
    list_display = ["user", "__unicode__", "status"]

    class Meta:
        model = FavoriteLine

admin.site.register(FavoriteLine, FavoriteLineAdmin)
