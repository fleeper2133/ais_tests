from django.core.management import BaseCommand
from course.models import Qualification, Block, NormativeDocument, Course, Testing, Ticket, Question, Varient, QuestionList, LearningMaterial
from usercourse.models import UserCourse, TaskQuestion, UserQuestion, UserTicket, UserAnswer, \
    QuestionTicket, UserCheckSkills, UserCheckSkillsQuestion, UserAnswerItem

class Command(BaseCommand):
    help = 'Удаление всех моделей из приложения course и usercourse'

    def handle(self, *args, **options):
        # Хаос и удаление
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

        UserCourse.objects.all().delete()
        TaskQuestion.all().delete()
        UserQuestion.objects.all().delete()
        UserTicket.objects.all().delete()
        UserAnswer.objects.all().delete()
        QuestionTicket.objects.all().delete()
        UserCheckSkills.objects.all().delete()
        UserCheckSkillsQuestion.objects.all().delete()
        UserAnswerItem.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Всё успешно удалено"))
