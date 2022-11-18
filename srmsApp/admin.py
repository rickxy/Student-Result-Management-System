from django.contrib import admin
from srmsApp import models

# Register your models here.
admin.site.register(models.Class)
admin.site.register(models.Subject)
admin.site.register(models.Student)
admin.site.register(models.Result)
admin.site.register(models.Student_Subject_Result)