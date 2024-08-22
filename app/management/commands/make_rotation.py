from django.core.management import BaseCommand
from course.models import Rotation, RotationQuestion, Question, Course
from datetime import timedelta
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Создание новой ротации вопросов для курса с course_id'

    def add_arguments(self, parser):
        parser.add_argument(
            "--course",
            type=int,
            help="ID курса"
        )
        parser.add_argument(
            "--count",
            type=int,
            help="Количество вопросов в ротации"
        )

    def handle(self, *args, **options):
        course_id = options["course"]
        count = options["count"]

        course = Course.objects.get(id=course_id)
        course.question_count = count
        
        # Извлекаем все вопросы, использованные в предыдущих ротациях
        old_questions = set(
            RotationQuestion.objects.filter(rotation__course=course).values_list('question', flat=True)
        )

        rotation = Rotation.objects.create(
            title=f"Ротация вопросов в курсе {course.name} под номером {Rotation.objects.filter(course=course).count()}",
            course=course,
            available_until=timezone.now() + timedelta(days=365), 
        )

        questions = list(Question.objects.filter(course=course))
        random.shuffle(questions)

        # Исключаем старые вопросы
        selected_questions = [q for q in questions if q.id not in old_questions]

        #если все вопросы уже были задействованы в ротациях
        if len(selected_questions) >= count:
            selected_questions = questions[:count]

        # Создаем записи в RotationQuestion
        for question in selected_questions:
            RotationQuestion.objects.create(
                rotation=rotation,
                question=question
            )

        self.stdout.write(self.style.SUCCESS("Ротация успешно произведена"))

  