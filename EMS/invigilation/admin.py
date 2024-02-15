from django.contrib import admin
from .models import Lecturer, Hall, Invigilators, Supervisors, Block

# Register your models here.
admin.site.register(Lecturer)
admin.site.register(Hall)
admin.site.register(Invigilators)
admin.site.register(Supervisors)
admin.site.register(Block)
