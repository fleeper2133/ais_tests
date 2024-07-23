from django.core.management import BaseCommand
from course.models import Qualification, Block, NormativeDocument, Course, Testing, Ticket, Question, Varient, QuestionList, LearningMaterial
from django.contrib.auth.models import User
from faker import Faker
from mixer.backend.django import mixer
import random
from django.utils import timezone
from datetime import timedelta

fake = Faker("ru_RU")

class Command(BaseCommand):
    help = 'Генерация моделей для приложения course'

    def add_arguments(self, parser):
        parser.add_argument(
            "--wipe",
            action="store_true",
            help="Удаление всех существующих данных"
        )
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Количество курсов"
        )

    def handle(self, *args, **options):
        count = options["count"]
        
        if options["wipe"]:
            Qualification.objects.all().delete()
            Block.objects.all().delete()
            NormativeDocument.objects.all().delete()
            Course.objects.all().delete()
            Testing.objects.all().delete()
            Ticket.objects.all().delete()
            Question.objects.all().delete()
            Varient.objects.all().delete()
            QuestionList.objects.all().delete()
            LearningMaterial.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Всё успешно удалено"))

        qualifications = []
        for _ in range(5):
            qualification = mixer.blend(Qualification)
            qualifications.append(qualification)

        blocks = []
        for qualification in qualifications:
            for _ in range(3):
                block = mixer.blend(Block, qualification=qualification)
                blocks.append(block)

        for _ in range(10):
            mixer.blend(NormativeDocument)

        learning_materials = []
        for _ in range(10):
            material = mixer.blend(LearningMaterial)
            learning_materials.append(material)

        courses = []
        for _ in range(count):
            course = mixer.blend(Course, qualification=random.choice(qualifications))
            courses.append(course)

            testing = mixer.blend(Testing, course=course)

            tickets = []
            for _ in range(5):
                ticket = mixer.blend(Ticket, testing=testing)
                tickets.append(ticket)

                questions = []
                for _ in range(20):
                    question = mixer.blend(Question, course=course, block=random.choice(blocks))
                    questions.append(question)

                    for _ in range(4):
                        mixer.blend(Varient, question=question)

                    question.calculate_right_answer_count()
                    question.calculate_answer_count()

                for i, question in enumerate(questions):
                    mixer.blend(QuestionList, ticket=ticket, question=question, number_in_ticket=i+1)

        self.stdout.write(self.style.SUCCESS(f'Успешно сгенерировали {count} курсов'))
