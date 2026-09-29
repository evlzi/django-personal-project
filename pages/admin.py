from django.contrib import admin
from .models import *

# Register your models here.


class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "about",
        "location",
    )


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "about",
        "course_type",
        "institution",
    )


class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "about",
        "due",
        "course",
    )


class GradeAdmin(admin.ModelAdmin):
    list_display = (
        "grade_type",
        "value",
        "assignment",
    )


admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Grade, GradeAdmin)
