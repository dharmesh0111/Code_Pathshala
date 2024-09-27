from django.contrib import admin
from myapp.models import E_learning,Course,course_skills


# Register your models here.
class E_learningAdmin(admin.ModelAdmin):
    list_display=['id','title','video','thumnail']

admin.site.register(E_learning,E_learningAdmin)


class courseAdmin(admin.ModelAdmin):
    list_display=['title','duration','certificate','thumnail','fees',"notes",'video',"video1"]

admin.site.register(Course,courseAdmin)



class course_skillAdmin(admin.ModelAdmin):
    list_display=['course_name','skill','chapter']

admin.site.register(course_skills,course_skillAdmin)

