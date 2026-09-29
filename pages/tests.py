from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Institution

# Create your tests here.


class InstitutionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser', email='test@gmail.com', password='password'
        )

        cls.post = Institution.objects.create(
            name='name', about='about', location='location'
        )

    def test_institution_model(self):
        self.assertEqual(self.post.name, "name")
        self.assertEqual(self.post.about, "about")
        self.assertEqual(self.post.location, "location")
        self.assertEqual(self.post.get_absolute_url(), "/institution/1/about")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get('/institution/1/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse('institution_list'))
        self.assertEqual(response.status_code, 200)

    def test_institution(self):
        response = self.client.get(reverse('institution_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name')
        self.assertTemplateUsed(response, 'institution/institution_list.html')

    def test_institution_about(self):
        response = self.client.get(
            reverse('institution_about', kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/post/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'about')
        self.assertTemplateUsed(response, 'institution/institution_about.html')

    def test_institution_institution_create(self):
        response = self.client.post(
            reverse("institution_create"),
            {
                "name": "name",
                "about": "about",
                "location": "location"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Institution.objects.last().name, "name")
        self.assertEqual(Institution.objects.last().about, "about")
        self.assertEqual(Institution.objects.last().location, "location")

    def test_institution_manage(self):
        response = self.client.post(
            reverse("institution_manage", args="1"),
            {
                "name": "new_name",
                "about": "new_about",
                "location": "new_location"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Institution.objects.last().name, "new_name")
        self.assertEqual(Institution.objects.last().about, "new_about")
        self.assertEqual(Institution.objects.last().location, "new_location")
