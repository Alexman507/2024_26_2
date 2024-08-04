from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@sky.pro')
        self.course = Course.objects.create(title='DRF', description='DRF', owner=self.user)
        self.lesson = Lesson.objects.create(title='Урок 1', description='Урок 1', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:retrieve-lesson', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse('materials:create-lesson')
        data = {
            'title': 'Урок 2',
            'description': 'Урок 2',
            'course': self.course.pk
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse('materials:update-lesson', args=(self.lesson.pk,))
        data = {'title': 'Новый урок'}
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data.get('title'), 'Новый урок'
        )

    def test_lesson_delete(self):
        url = reverse('materials:delete-lesson', args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse('materials:lessons-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data,
            {'count': 1, 'next': None, 'previous': None, 'results':
                [{'id': self.lesson.pk, 'title': self.lesson.title, 'description': self.lesson.description,
                  'preview': None, 'url': None,
                  'course': self.lesson.course.pk, 'owner': self.lesson.owner.pk}]}
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@sky.pro')
        self.course = Course.objects.create(title='DRF', description='DRF', owner=self.user)
        self.lesson = Lesson.objects.create(title='Урок 1', description='Урок 1', course=self.course, owner=self.user)
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        url = reverse("materials:subscription")
        data = {
            "course": self.course.pk
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('message'), 'Подписка отключена'
        )
