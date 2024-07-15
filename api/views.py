# Course/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from course.models import Qualification, Block, NormativeDocument, Course, Testing, Ticket, Question, Varient, QuestionList, LearningMaterial
from .serializers import QualificationSerializer, BlockSerializer, NormativeDocumentSerializer, CourseSerializer, TestingSerializer, TicketSerializer, QuestionSerializer, VarientSerializer, QuestionListSerializer, LearningMaterialSerializer
from usercourse.models import UserCourse, TaskQuestion, UserQuestion, UserTicket, UserAnswer, UserAnswerItem, QuestionTicket, UserCheckSkills, UserCheckSkillsQuestion
from .serializers import UserCourseSerializer, TaskQuestionSerializer, UserQuestionSerializer, UserTicketSerializer, UserAnswerSerializer, UserAnswerItemSerializer, QuestionTicketSerializer, UserCheckSkillsSerializer, UserCheckSkillsQuestionSerializer

from rest_framework.permissions import IsAdminUser, IsAuthenticated

class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer

class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

class NormativeDocumentViewSet(viewsets.ModelViewSet):
    queryset = NormativeDocument.objects.all()
    serializer_class = NormativeDocumentSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class TestingViewSet(viewsets.ModelViewSet):
    queryset = Testing.objects.all()
    serializer_class = TestingSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class VarientViewSet(viewsets.ModelViewSet):
    queryset = Varient.objects.all()
    serializer_class = VarientSerializer

class QuestionListViewSet(viewsets.ModelViewSet):
    queryset = QuestionList.objects.all()
    serializer_class = QuestionListSerializer

class LearningMaterialViewSet(viewsets.ModelViewSet):
    queryset = LearningMaterial.objects.all()
    serializer_class = LearningMaterialSerializer

# --------------------------------------------------------------

class UserCourseViewSet(viewsets.ModelViewSet):
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer

    #для страницы "все курсы" (Все курсы пользователя + 3 любых новых)
    @action(detail=False, methods=['get'])
    def user_courses(self, request):
        user_courses = Course.objects.filter(user=request.user)
        user_courses_serializer = CourseSerializer(user_courses, many=True)

        other_courses = Course.objects.exclude(user=request.user)[:3]
        other_courses_serializer = CourseSerializer(other_courses, many=True)

        response_data = {
            'user_courses': user_courses_serializer.data,
            'other_courses': other_courses_serializer.data,
        }
        return Response(response_data)
    
     # Получение последних 10 курсов пользователя
    @action(detail=False, methods=['get'])
    def last_ten_courses(self, request):
        user = request.user
        last_ten_courses = UserCourse.objects.filter(user=user).order_by('-start_date')[:10]
        serializer = self.get_serializer(last_ten_courses, many=True)
        return Response(serializer.data)

    # Получение последнего курса пользователя
    @action(detail=False, methods=['get'])
    def last_course(self, request):
        user = request.user
        try:
            #cтоит брать по последнему вхождению, скорее всего, если идёт паралельно несколько курсов
            last_course = UserCourse.objects.filter(user=user).order_by('-start_date').first()
            serializer = self.get_serializer(last_course)
            return Response(serializer.data)
        except UserCourse.DoesNotExist:
            return Response({'detail': 'Пользователь не записан на этот курс.'}, status=status.HTTP_404_NOT_FOUND)

    # Отметка курса как избранного
    @action(detail=True, methods=['post'])
    def mark_as_favorite(self, request, pk=None):
        try:
            user_course = self.get_object()
            user_course.selected = True
            user_course.save()
            return Response({'status': 'Курс отмечен как избранный'})
        except UserCourse.DoesNotExist:
            return Response({'detail': 'Курс не найден. Повторите позже'}, status=status.HTTP_404_NOT_FOUND)

    # Получение отложенных курсов пользователя
    @action(detail=False, methods=['get'])
    def delayed_courses(self, request):
        user = request.user
        delayed_courses = UserCourse.objects.filter(user=user, status='Delayed')
        serializer = self.get_serializer(delayed_courses, many=True)
        return Response(serializer.data)

    # Получение пройденных курсов пользователя
    @action(detail=False, methods=['get'])
    def completed_courses(self, request):
        user = request.user
        completed_courses = UserCourse.objects.filter(user=user, status='Completed')
        serializer = self.get_serializer(completed_courses, many=True)
        return Response(serializer.data)

class TaskQuestionViewSet(viewsets.ModelViewSet):
    queryset = TaskQuestion.objects.all()
    serializer_class = TaskQuestionSerializer

class UserQuestionViewSet(viewsets.ModelViewSet):
    queryset = UserQuestion.objects.all()
    serializer_class = UserQuestionSerializer

class UserTicketViewSet(viewsets.ModelViewSet):
    queryset = UserTicket.objects.all()
    serializer_class = UserTicketSerializer

class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

class UserAnswerItemViewSet(viewsets.ModelViewSet):
    queryset = UserAnswerItem.objects.all()
    serializer_class = UserAnswerItemSerializer

class QuestionTicketViewSet(viewsets.ModelViewSet):
    queryset = QuestionTicket.objects.all()
    serializer_class = QuestionTicketSerializer

class UserCheckSkillsViewSet(viewsets.ModelViewSet):
    queryset = UserCheckSkills.objects.all()
    serializer_class = UserCheckSkillsSerializer

class UserCheckSkillsQuestionViewSet(viewsets.ModelViewSet):
    queryset = UserCheckSkillsQuestion.objects.all()
    serializer_class = UserCheckSkillsQuestionSerializer