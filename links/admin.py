from django.contrib import admin
from .models import LinkPage, Link


class LinkInline(admin.TabularInline):
    model = Link
    extra = 1


@admin.register(LinkPage)
class LinkPageAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "bio")
    inlines = [LinkInline]


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "page", "order", "is_active")
    list_filter = ("page", "is_active")
    list_editable = ("order", "is_active")