from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Укажите телефон (необязательно)",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Добавьте аватар (необязательно)",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город (необязательно)",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    CASH = 'CASH'
    ONLINE = 'ONLINE'
    PAYMENT_TYPES = [
        (CASH, 'Наличными'),
        (ONLINE, 'Перевод'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', blank=True, null=True)
    payment_amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, verbose_name='Тип оплаты')

    def __str__(self):
        return f"{self.user} - {self.course if self.course else self.lesson}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
