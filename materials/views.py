import pytz
from datetime import datetime, timedelta

from django.conf import settings
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from timezone_field.backends import pytz

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPaginator
from materials.serializer import CourseSerializer, LessonSerializer, SubscriptionSerializer
from materials.tasks import send_information_about_course_update
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPaginator

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        course = serializer.save()
        course.save()

        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_4_hours_ago = datetime.now(zone) - timedelta(hours=4)

        if course.updated_at < current_datetime_4_hours_ago:
            send_information_about_course_update.delay(course.pk)

class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        new_lesson = serializer.save()

        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_4_hours_ago = datetime.now(zone) - timedelta(hours=4)

        course = get_object_or_404(Course, pk=new_lesson.course.pk)
        if new_lesson.course.updated_at < current_datetime_4_hours_ago:
            send_information_about_course_update.delay(course.pk)

        course.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MaterialsPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)

    def perform_update(self, serializer):
        new_lesson = serializer.save()
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_4_hours_ago = datetime.now(zone) - timedelta(hours=4)
        course = get_object_or_404(Course, pk=new_lesson.course.pk)
        if new_lesson.course.updated_at < current_datetime_4_hours_ago:
            send_information_about_course_update.delay(course.pk)
        course.save()


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)
        sub_item = Subscription.objects.all().filter(user=user).filter(course=course)

        if sub_item.exists():
            sub_item.delete()
            message = 'Подписка отключена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка включена'
        return Response({"message": message})
