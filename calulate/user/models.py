from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Расширяем стандартную модель юзера, в дальнейшем сможем легко ее изменить"""
    biography = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Биография',
        help_text='Не стесняйтесь, расскажите о себе'
    )