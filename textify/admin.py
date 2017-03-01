from django.contrib import admin

from .models import User, Note, Drawing, ClassificationMachine

admin.site.register(User)
admin.site.register(Note)
admin.site.register(Drawing)
admin.site.register(ClassificationMachine)