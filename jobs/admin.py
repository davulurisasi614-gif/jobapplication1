from django.contrib import admin # type: ignore
from .models import Job, Application

admin.site.register(Job)
admin.site.register(Application)
