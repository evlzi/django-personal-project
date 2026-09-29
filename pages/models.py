from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserType(models.IntegerChoices):
    STUDENT = 0, 'Student'
    TEACHER = 1, 'Teacher'
    ADMIN = 2, 'Admin'


class CourseType(models.IntegerChoices):
    REGULAR = 0, 'Regular'
    HONOURS = 1, 'Honours'
    DUAL = 2, 'Dual'
    AP = 3, 'AP'
    IB = 4, 'IB'


class GradeType(models.IntegerChoices):
    QUANTITATIVE = 0, "Quantitative"
    QUALITATIVE = 1, "Qualitative"

# Create your models here.


class Institution(models.Model):
    name = models.TextField()
    about = models.TextField()
    location = models.TextField()

    def get_absolute_url(self):
        return reverse("institution_about", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.TextField()
    about = models.TextField()
    course_type = models.IntegerField(
        choices=CourseType.choices, default=CourseType.REGULAR)
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name='courses')

    def get_absolute_url(self):
        return reverse("institution_course_about", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Assignment(models.Model):
    name = models.TextField()
    about = models.TextField()
    due = models.DateTimeField()
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='assignments')

    def __str__(self):
        return self.name


class Grade(models.Model):
    grade_type = models.IntegerField(
        choices=GradeType.choices, default=GradeType.QUANTITATIVE)
    value = models.TextField()
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='grades')

    def __str__(self):
        return f"{self.assignment.name} - {self.value}"


class UserProfile(models.Model):
    auth_user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', null=True)
    name = models.TextField()
    about = models.TextField()
    user_type = models.IntegerField(
        choices=UserType.choices, default=UserType.STUDENT)
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

    def join_institution(self, institution):
        self.institution = institution
        self.save()
        return reverse("institution_about", kwargs={"pk": institution.pk})

    def leave_institution(self, institution):
        is_admin = (self.user_type == UserType.ADMIN)

        self.institution = None
        self.user_type = UserType.STUDENT
        self.save()

        if is_admin:
            institution.delete()
            return reverse("institution_list")

        return reverse("institution_about", kwargs={"pk": institution.pk})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            auth_user=instance,
            name=instance.get_full_name() or instance.username,
            about=""
        )
