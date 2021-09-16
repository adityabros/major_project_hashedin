from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(User_Profile)
admin.site.register(Labels)
admin.site.register(event_logs)
admin.site.register(Comments)