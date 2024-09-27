from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class E_learning(models.Model):
    title = models.CharField(max_length=100)
    video = models.CharField(max_length=500)
    # notes =models.FileField(upload_to='media',max_length=250,default=None,null=True)
    thumnail = models.ImageField(upload_to='media',default=0)


class feedback(models.Model):
    uid=models.ForeignKey(User,db_column="uid", on_delete=models.CASCADE)
    E_learning_id=models.ForeignKey(E_learning,db_column="E_learning_id", on_delete=models.CASCADE)
    ratings = models.CharField(max_length=1, blank=True, null=True)
    review = models.CharField(max_length=500, blank=True, null=True,default="no feedback given")


class Course(models.Model):
    title = models.CharField(max_length=100,primary_key=True)
    duration = models.IntegerField(default=None)
    certificate = models.ImageField(upload_to='media',default=0)
    thumnail = models.ImageField(upload_to='media',default=0)
    fees = models.IntegerField(default=None)
    video = models.CharField(max_length=500,null=True)
    notes =models.FileField(upload_to='media',max_length=250,default=None,null=True)
    video1 = models.CharField(max_length=500,null=True)






class course_skills(models.Model):
    course_name = models.ForeignKey(Course,db_column="course_name", on_delete=models.CASCADE)
    skill = models.CharField(max_length=100,null=True,default=None)
    chapter = models.CharField(max_length=500,default=None)


class enrolled(models.Model):
    uid=models.ForeignKey(User,db_column="uid", on_delete=models.CASCADE)
    course_name = models.ForeignKey(Course,db_column="course_name", on_delete=models.CASCADE)
    paid=models.BooleanField(default=False)

class coursefeedback(models.Model):
    uid=models.ForeignKey(User,db_column="uid", on_delete=models.CASCADE)
    course_title=models.ForeignKey(Course,db_column="E_learning_id", on_delete=models.CASCADE)
    ratings = models.CharField(max_length=1, blank=True, null=True)
    review = models.CharField(max_length=500, blank=True, null=True,default="no feedback given")
    



# class skills_topic(models.Model):
#     course_name = models.ForeignKey(Course,db_column="course_name", on_delete=models.CASCADE)
#     course_skills_id = models.ForeignKey(course_skills,db_column="course_skills_name", on_delete=models.CASCADE)
#     chapter = models.CharField(max_length=100)