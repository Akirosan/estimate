from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Расширяем стандартную модель юзера, далее сможем легко ее изменить"""
    biography = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Биография',
        help_text='Не стесняйтесь, расскажите о себе'
    )
