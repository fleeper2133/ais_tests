from django.core.management import BaseCommand, call_command
from course.models import Course, Ticket, QuestionList, Testing
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
import random

class Command(BaseCommand):
    help = 'Создание 10 билетов для каждого курса'

    def handle(self, *args, **options):
        courses = Course.objects.all()        
        total_tickets_count = 10
        total_questions_count = 20
        for course in courses:
            testing = Testing.objects.filter(course=course).first()
            if len(Ticket.objects.filter(testing=testing)) >= total_tickets_count:
                continue

            questions = course.get_available_questions()
            for _ in range(total_tickets_count):
                random.shuffle(questions)
                selected_questions = questions[:total_questions_count]

                with transaction.atomic():
                    ticket = Ticket.objects.create(
                        name=f"Random Ticket for {course.id}",
                        difficulty='medium',
                        question_count=len(selected_questions),
                        testing=testing
                    )

                    for i in range(len(selected_questions)):
                        QuestionList.objects.create(
                            ticket=ticket,
                            number_in_ticket=i + 1,  
                            question=selected_questions[i]  
                        )
             
            self.stdout.write(self.style.SUCCESS(f"Успешно созданы билеты для курса {course.id}"))

        self.stdout.write(self.style.SUCCESS("Билеты успешно созданы для всех курсов"))