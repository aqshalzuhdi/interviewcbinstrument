from django.db import models

class Student(models.Model):
    name = models.TextField(max_length=100)
    grade = models.IntegerField()

    def __str__(self):
        return self.name