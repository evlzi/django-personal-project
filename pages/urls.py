from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name = 'home'),
    path('institution', InstitutionPage.as_view(), name = 'institution_list'),
    path('institution/create', InstitutionCreatePage.as_view(), name = 'institution_create'),
    path('institution/<int:pk>/', InstitutionAboutPage.as_view(), name='institution_about'),
    path('institution/<int:pk>/about', InstitutionAboutPage.as_view(), name='institution_about'),
    path('institution/<int:pk>/courses', InstitutionCoursesPage.as_view(), name='institution_courses'),
    path('institution/<int:pk>/manage', InstitutionManagePage.as_view(), name = 'institution_manage'),
    path('institution/<int:pk>/manage/create_course', InstitutionCourseCreatePage.as_view(), name = 'institution_course_create'),
    path('institution/<int:institution_pk>/course/<int:course_pk>', InstitutionCourseAboutPage.as_view(), name='institution_course_about'),
    path('institution/<int:institution_pk>/course/<int:course_pk>/about', InstitutionCourseAboutPage.as_view(), name='institution_course_about'),
    path('institution/<int:pk>/join/', join_institution, name='join_institution'),
    path('institution/<int:pk>/leave/', leave_institution, name='leave_institution'),
]
