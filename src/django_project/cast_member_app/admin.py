from django.contrib import admin

from src.django_project.cast_member_app.models import CastMember


@admin.register(CastMember)
class CastMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")
    search_fields = ("name", "type")
