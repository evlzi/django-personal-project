from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import *

# Create your views here.


@login_required
def join_institution(request, pk):
    institution = get_object_or_404(Institution, pk=pk)
    profile = UserProfile.objects.get(auth_user=request.user)
    redirect_url = profile.join_institution(institution)
    return redirect(redirect_url)


@login_required
def leave_institution(request, pk):
    institution = get_object_or_404(Institution, pk=pk)
    profile = UserProfile.objects.get(auth_user=request.user)
    redirect_url = profile.leave_institution(institution)
    return redirect(redirect_url)


class HomePage(TemplateView):
    template_name = 'home.html'


class InstitutionPage(ListView):
    model = Institution
    template_name = 'institution/institution_list.html'


class InstitutionCreatePage(CreateView):
    model = Institution
    template_name = 'institution/institution_create.html'
    fields = ['name', 'about', 'location']

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.user.is_authenticated:
            profile, created = UserProfile.objects.get_or_create(
                auth_user=self.request.user)
            profile.user_type = UserType.ADMIN
            profile.institution = self.object
            profile.save()

        return response


class InstitutionManagePage(UpdateView):
    model = Institution
    template_name = 'institution/institution_manage.html'
    fields = ['name', 'about', 'location']


class InstitutionAboutPage(DetailView):
    model = Institution
    template_name = 'institution/institution_about.html'


class InstitutionCoursesPage(DetailView):
    model = Institution
    template_name = 'institution/institution_courses.html'


class InstitutionDiscussionsPage(DetailView):
    model = Institution
    template_name = 'institution/institution_discussions.html'


class InstitutionCourseCreatePage(CreateView):
    model = Course
    template_name = 'institution/course/course_create.html'
    fields = ['name', 'about', 'course_type']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Fetch the institution using the pk from the URL and add it to the context
        context['institution'] = get_object_or_404(
            Institution, pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        # Automatically assign the institution from the URL before saving
        form.instance.institution = get_object_or_404(
            Institution, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the manage page or course list after creation
        return reverse('institution_manage', kwargs={'pk': self.kwargs.get('pk')})


class InstitutionCourseAboutPage(DetailView):
    model = Course
    template_name = 'institution/course/course_about.html'

    def get_object(self, queryset=None):
        # Fetch the specific course, and ensure it belongs to this institution
        return get_object_or_404(
            Course,
            pk=self.kwargs.get('course_pk'),
            institution_id=self.kwargs.get('institution_pk')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the institution to the context so your breadcrumbs and templates can use it
        context['institution'] = get_object_or_404(
            Institution, pk=self.kwargs.get('institution_pk'))
        return context
