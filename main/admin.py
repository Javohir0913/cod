from django.contrib import admin
from .models import StudentInfo

class StudentAdmin(admin.ModelAdmin):
    search_fields = ['file_id']
admin.site.register(StudentInfo, StudentAdmin)
