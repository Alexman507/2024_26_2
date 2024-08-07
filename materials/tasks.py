from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config.settings import EMAIL_HOST_USER
from materials.models import Course, Subscription


@shared_task
def send_information_about_course_update(pk):
    """Отправляет сообщение пользователю об обновлении курса"""
    subscriptions = Subscription.objects.filter(course=pk)
    course = get_object_or_404(Course, pk=pk)
    email_list = []
    message = f"Ваш курс {course.title} был обновлен!"
    for s in subscriptions:
        email_list.append(s.user.email)
        print(f"email added = {s.user.email}")

    if email_list:
        print(email_list)
        send_mail(
            f"Обновление курса.",
            message,
            EMAIL_HOST_USER,
            email_list
        )
