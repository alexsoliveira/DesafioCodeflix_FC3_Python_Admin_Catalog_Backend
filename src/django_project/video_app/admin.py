from django.contrib import admin

from src.django_project.video_app.models import AudioVideoMedia, Video

# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    pass

class AudioVideoMediaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Video,VideoAdmin)
admin.site.register(AudioVideoMedia,AudioVideoMediaAdmin)