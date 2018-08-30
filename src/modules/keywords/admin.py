from django.contrib import admin

from keywords.models import Keyword, VideoItem


class VideoItemAdmin(admin.ModelAdmin):
    """ Simple customization for admin interface """

    list_filter = ('keywords',)
    filter_horizontal = ('keywords', )
    search_fields = ('title',)
    list_display = ('__str__', 'published_at')
    readonly_fields = ('youtube_id',)


admin.site.register(Keyword)
admin.site.register(VideoItem, VideoItemAdmin)
