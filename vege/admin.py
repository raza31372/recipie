from django.contrib import admin

# Register your models here.
from .models import *

# admin register
admin.site.register(Recipie)

admin.site.register(StudentID)
admin.site.register(Student)
admin.site.register(Department)
