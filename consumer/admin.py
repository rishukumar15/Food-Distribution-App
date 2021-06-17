from django.contrib import admin

# Register your models here.
from .models import Consumer, Provider, Display, History

admin.site.register(Consumer)
admin.site.register(Provider)
admin.site.register(Display)
admin.site.register(History)