from django.contrib import admin
from .models import CustomUser, Case, Mediator, Lawyer

admin.site.register(CustomUser)
admin.site.register(Case)
admin.site.register(Mediator)
admin.site.register(Lawyer)
