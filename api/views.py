from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from course.models import Qualification, Block, NormativeDocument, Course, Testing, Ticket, Question, Varient, QuestionList, LearningMaterial
from .serializers import QualificationSerializer, BlockSerializer, NormativeDocumentSerializer, QuestionDetailSerializer, CourseSerializer, TestingSerializer, TicketSerializer, QuestionSerializer, VarientSerializer, QuestionListSerializer, LearningMaterialSerializer
from usercourse.models import UserCourse, TaskQuestion, UserQuestion, UserTicket, UserAnswer, UserAnswerItem, QuestionTicket, UserCheckSkills, UserCheckSkillsQuestion
from .serializers import UserCourseSerializer, TaskQuestionSerializer, UserQuestionSerializer, UserTicketSerializer, UserAnswerSerializer, UserAnswerItemSerializer, QuestionTicketSerializer, UserCheckSkillsSerializer, UserCheckSkillsQuestionSerializer

#допилить права на редактирование/удаление
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

    # При нажатии кнопки начать у курса создаём курс-пользователя
    @action(detail=True, methods=['post'])
    def start_course(self, request, pk=None):
        from django.utils import timezone
        user = request.user
        course = self.get_object()
        
        user_course, created = UserCourse.objects.get_or_create(
            user=user, 
            course=course,
            defaults={'start_date': timezone.now(), 'progress': 0, 'status': 'New'}
        )
        if not created:
            return Response({'detail': 'Пользователь уже проходит этот курс.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserCourseSerializer(user_course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TestingViewSet(viewsets.ModelViewSet):
    queryset = Testing.objects.all()
    serializer_class = TestingSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # получение детальной информации по вопросу
    @action(detail=True, methods=['get'], url_path='detail')
    def get_question_detail(self, request, pk=None):
        question = self.get_object()
        serializer = QuestionDetailSerializer(question)
        return Response(serializer.data)
    
    # # проверка правильности (пока вопросов больше чем ответов)
    # @action(detail=True, methods=['post'], url_path='check-answer')
    # def check_answer(self, request, pk=None):
    #     from datetime import timedelta
    #     question = self.get_object()
    #     answer_ids = request.data.get('answers', [])
    #     correct_answers = Varient.objects.filter(question=question, correct=True).values_list('id', flat=True)

    #     is_correct = set(answer_ids) == set(correct_answers)
    #     user = request.user

    #     # Обновление или создание объекта UserAnswer
    #     user_answer, created = UserAnswer.objects.get_or_create(
    #         user=user,
    #         question=question,
    #         defaults={'correct': is_correct, 'answer_time': timedelta(seconds=10)}  # Временное значение времени ответа
    #     )
    #     if not created:
    #         user_answer.correct = is_correct
    #         user_answer.save()

    #     response_data = {'is_correct': is_correct,}

    #     if not is_correct:
    #         question_serializer = QuestionDetailSerializer(question)
    #         response_data['details'] = question_serializer.data
    #     return Response(response_data)

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
    permission_classes = [IsAuthenticated]

    #отметить вопрос, как избранный
    @action(detail=True, methods=['post'])
    def mark_as_favorite(self, request, pk=None):
        user = request.user
        question = self.get_object()
        user_question, created = UserQuestion.objects.get_or_create(user=user, question=question)
        user_question.selected = True
        user_question.save()
        return Response({'status': 'question marked as favorite'})
    
    # получить избранные вопросы
    @action(detail=False, methods=['get'], url_path='favorites')
    def get_favorites(self, request):
        user = request.user
        favorite_questions = UserQuestion.objects.filter(user=user, selected=True)
        serializer = UserQuestionSerializer(favorite_questions, many=True)
        return Response(serializer.data)

    # получить вопросы с плохой степенью запоминания
    @action(detail=False, methods=['get'], url_path='memorization/bad')
    def get_bad_memorization(self, request):
        user = request.user
        bad_memorization_questions = UserQuestion.objects.filter(user=user, memorization='Bad')
        serializer = UserQuestionSerializer(bad_memorization_questions, many=True)
        return Response(serializer.data)

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

    #Генерация тестирования по выбранной сложности для выбранного числа вопросов
    @action(detail=True, methods=['post'])
    def generate_questions(self, request, pk=None):
        user_check_skills = self.get_object()
        difficulty = request.data.get('difficulty')
        question_count = request.data.get('question_count')

        if not difficulty or not question_count:
            return Response({'detail': 'Пожалуйста укажите сложность и количество вопросов.'}, status=status.HTTP_400_BAD_REQUEST)

        available_questions = Question.objects.filter(difficulty=difficulty)
        selected_questions = available_questions.order_by('?')[:int(question_count)]

        user_check_skills.question_count = len(selected_questions)
        user_check_skills.save()

        for index, question in enumerate(selected_questions):
            UserCheckSkillsQuestion.objects.create(
                user_check_skills=user_check_skills,
                question=question,
                number_in_check=index + 1,
                status='Not Answered'
            )

        questions_serializer = UserCheckSkillsQuestionSerializer(selected_questions, many=True)
        return Response(questions_serializer.data)

class UserCheckSkillsQuestionViewSet(viewsets.ModelViewSet):
    queryset = UserCheckSkillsQuestion.objects.all()
    serializer_class = UserCheckSkillsQuestionSerializer