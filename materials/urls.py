from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView,
                             SubscriptionAPIView, )

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons-list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="create-lesson"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="retrieve-lesson"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="update-lesson"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="delete-lesson"),
    path("subscription", SubscriptionAPIView.as_view(), name="subscription"),
]
urlpatterns += router.urls
