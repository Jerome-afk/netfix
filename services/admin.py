from django.contrib import admin
from .models import Service, RequestedService

admin.site.register(Service)
admin.site.register(RequestedService)
