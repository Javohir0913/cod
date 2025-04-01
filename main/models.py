from django.db import models

# Create your models here.
class StudentInfo(models.Model):
    student_file = models.FileField(upload_to='student_file/')
    file_id = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return f'{self.file_id}'