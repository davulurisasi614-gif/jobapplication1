from django.contrib import admin
from .models import Job, Application

admin.site.site_header = "Alexa Administration"
admin.site.site_title = "Alexa Admin Portal"
admin.site.index_title = "Welcome to Alexa Admin"

admin.site.register(Job)
admin.site.register(Application)
