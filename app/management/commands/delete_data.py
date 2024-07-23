from django.core.management import BaseCommand
from course.models import Qualification, Block, NormativeDocument, Course, Testing, Ticket, Question, Varient, QuestionList, LearningMaterial

class Command(BaseCommand):
    help = 'Удаление всех моделей из приложения course'

    def handle(self, *args, **options):
        # Deleting data from all models
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
