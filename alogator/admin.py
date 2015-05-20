from django.contrib import admin

from .models import LogFile, LogActor, LogSensor


class LogFileAdmin(admin.ModelAdmin):
    list_display = ('path', 'lastModified')
    date_hierarchy = 'lastModified'
    readonly_fields = ('lastModified', 'lastPosition', 'lastSize', )


class LogActorAdmin(admin.ModelAdmin):
    list_display = ('email', 'active', 'mute')
    list_filter = ('active', 'mute')


class LogSensorAdmin(admin.ModelAdmin):
    list_display = ('pattern', 'caseSensitive', 'actor')


admin.site.register(LogFile)  # , LogFileAdmin)
admin.site.register(LogActor)  # , LogActorAdmin)
admin.site.register(LogSensor)  # , LogSensorAdmin)
