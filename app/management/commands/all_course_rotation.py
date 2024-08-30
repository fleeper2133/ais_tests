from django.core.management import BaseCommand, call_command
from course.models import Course

class Command(BaseCommand):
    help = 'Создание ротаций для всех курсов единомоментно'

    def handle(self, *args, **options):
        courses = Course.objects.all()        

        for course in courses:
            course.update_question_count()
            total_questions = course.question_count  #(будет актуальным после парсинга)
            if total_questions > 0:
                count = int(total_questions * 0.3)

                if count < 1:
                    count = 1

                # Вызываем команду 'make_rotation' для каждого курса с параметрами
                course.question_count = total_questions
                course.save()
                call_command('make_rotation', course=course.id, count=count)
                #self.stdout.write(self.style.SUCCESS(f"Ротация успешно создана для курса {course.id}"))

        self.stdout.write(self.style.SUCCESS("Ротации успешно произведены для всех курсов"))