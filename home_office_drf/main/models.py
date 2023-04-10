from django.db import models


MAX_NAME_LEN = 15


class Company(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name='Название компании',
        blank=True
    )
    prompt_client = models.TextField(
        verbose_name='Промт для бота'
    )
    prompt_secured = models.TextField(
        verbose_name='Закрытый промт'
    )
    date_create = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    def __str__(self):
        return self.name[:MAX_LEN]

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"


class User(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name='Название компании',
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='user',
    )
    telegram_id = models.CharField(
        max_length=20,
        verbose_name='Телеграмм ID'
    )
