from django.db import models
from course.models import Course

class Proposal(models.Model):
    fio = models.CharField("ФИО", max_length=500)
    email = models.EmailField("Электронная почта")
    phone = models.CharField("Номер телефона", max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField("Дата последнего обновления", auto_now=True, null=True, blank=True)
    is_checked = models.BooleanField("Обработана", default=False)

    def __str__(self):
        return f"{self.fio} - {self.phone}"
    
    class Meta:
        verbose_name = "Заявка на обучение"
        verbose_name_plural = "Заявки на обучение"
