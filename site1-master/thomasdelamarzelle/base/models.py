from django.db import models
from django.contrib.auth.models import User
# Choices
GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
CATEGORY = (
    ('Ableton rack', 'Ableton rack'),
    ('Sample Pack', 'Sample Pack'),
    ('Lesson', 'Lesson'),
    ('Midi Pack', 'Midi Pack'),
)
STATUS = (
    ('Pending', 'Pending'),
    ('Out of Stock', 'Out of Stock'),
    ('Delivered', 'Delivered'),
)
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = phone = models.CharField(max_length=60, null=True)
    phone = models.CharField(max_length=60, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, choices=GENDER)
    date_created = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.name

class Tags(models.Model):
    name = models.CharField(max_length=240, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=240, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=240, null=True, choices=CATEGORY)
    description = models.CharField(max_length=240, null=True)
    tags = models.ManyToManyField(Tags)
    def __str__(self):
        return self.name




class Order(models.Model):

    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=240, null=True, choices=STATUS)
    date_created = models.DateField(auto_now_add=True, null=True)


'''class Goals(models.Model):
    name'''
