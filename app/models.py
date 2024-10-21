from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Profile(models.Model):
    """template class for company profile"""

    logotype = models.FileField(
        "Логотип организации", upload_to="upload/", blank=True, null=True, default=None
    )
    footer_logotype = models.FileField(
        "Логотип для футера (необязательно)",
        upload_to="upload/",
        blank=True,
        null=True,
        default=None,
    )
    short_name = models.CharField(
        "Краткое название организации",
        max_length=100,
        blank=True,
        null=True,
        default=None,
    )
    direction = models.CharField(
        "Направление деятельности организации",
        max_length=100,
        blank=True,
        null=True,
        default=None,
    )
    full_name = models.CharField(
        "Полное название организации",
        max_length=300,
        blank=True,
        null=True,
        default=None,
    )
    intro = models.TextField(
        "Текст для главной страницы", blank=True, null=True, default=None
    )

    phone = models.CharField(
        "Главный телефон организации",
        max_length=200,
        blank=True,
        null=True,
        default=None,
    )

    email = models.TextField(
        "Адрес электронной почты организации", blank=True, null=True, default=None
    )

    address = models.TextField(
        "Адрес местоположения организации", null=True, blank=True, default=None
    )

    req = RichTextUploadingField(verbose_name="Реквизиты организации")

    policy = RichTextUploadingField(
        "Политика конфиденциальности", null=True, blank=True
    )

    terms = RichTextUploadingField("Условия использования", null=True, blank=True)

    class Meta:
        verbose_name = "Профиль компании"
        verbose_name_plural = "Профили компаний"

    def __str__(self):
        return self.short_name
