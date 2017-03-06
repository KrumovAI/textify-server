from django.contrib import admin

from .models import User, Drawing, ClassificationMachine

admin.site.register(User)
admin.site.register(Drawing)
admin.site.register(ClassificationMachine)