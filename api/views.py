from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions
from users.models import CustomUser
from course.models import Qualification, Block, NormativeDocument, Course, Testing, Ticket, Question, Varient, QuestionList, LearningMaterial, Rotation, RotationQuestion
from .serializers import QualificationSerializer, BlockSerializer, NormativeDocumentSerializer, QuestionDetailSerializer, CourseSerializer, TestingSerializer, TicketSerializer, QuestionSerializer, VarientSerializer, QuestionListSerializer, LearningMaterialSerializer
from usercourse.models import UserCourse, TaskQuestion, UserQuestion, UserTicket, UserAnswer, UserAnswerItem, QuestionTicket, UserCheckSkills, UserCheckSkillsQuestion
from .serializers import UserCourseSerializer, TaskQuestionSerializer, UserQuestionSerializer, UserTicketSerializer, UserAnswerSerializer, UserAnswerItemSerializer, QuestionTicketSerializer, UserCheckSkillsSerializer, UserCheckSkillsQuestionSerializer, CourseQuestionDetailSerializer, UserQuestionStatisticSerializer
import random
from django.db import transaction
# создание + прохождение билета покрыть в тестах.

class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    #permission_classes = [IsAdminUser]

class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    #permission_classes = [IsAdminUser]

class NormativeDocumentViewSet(viewsets.ModelViewSet):
    queryset = NormativeDocument.objects.all()
    serializer_class = NormativeDocumentSerializer
    #permission_classes = [IsAdminUser]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    #permission_classes = [IsAuthenticated]

    # При нажатии кнопки начать у курса создаём курс-пользователя
    @action(detail=True, methods=['post'])
    def start_course(self, request, pk=None):
        from django.utils import timezone
        user = request.user
        if not user.is_authenticated: 
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)

        course = self.get_object()
        
        user_course, created = UserCourse.objects.get_or_create(
            user=user, 
            course=course,
            defaults={'start_date': timezone.now().date(), 'progress': 0, 'status': 'New'}
        )
        if not created:
            return Response({'detail': 'Пользователь уже проходит этот курс.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserCourseSerializer(user_course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # Отметка курса как отложенного
    @action(detail=True, methods=['post'])
    def mark_as_delayed(self, request, pk=None):
        from django.utils import timezone
        user = request.user
        if not user.is_authenticated: 
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)

        course = self.get_object()
        
        user_course, created = UserCourse.objects.get_or_create(
            user=user, 
            course=course,
            defaults={'start_date': timezone.now().date(), 'progress': 0, 'status': 'Delayed'}
        )
        if not created:
            user_course.status = "Delayed"
            user_course.save()

        serializer = UserCourseSerializer(user_course)
        return Response({'status': 'Курс отмечен как отложенный', 'user_course': serializer.data}, status=status.HTTP_201_CREATED)

class TestingViewSet(viewsets.ModelViewSet):
    queryset = Testing.objects.all()
    serializer_class = TestingSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(detail=True, methods=['post'])
    def detail_user_ticket(self, request, pk=None):
        user = request.user
        if not user.is_authenticated: 
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)
        ticket = self.get_object()

        if len(UserCourse.objects.filter(user=user, course=ticket.testing.course)) == 0:
            return Response({'detail': 'Пользовательский курс не найден.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_ticket = UserTicket.objects.create(
            ticket=ticket,
            user=user,
            user_course=UserCourse.objects.filter(user=user, course=ticket.testing.course).first(),
            attempt_count=0,
        )
        user_ticket.update_attempt_count()

        serializer = UserTicketSerializer(user_ticket, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    permission_classes = [IsAuthenticated]

    # получение детальной информации по вопросу
    @action(detail=True, methods=['get'], url_path='detail')
    def get_question_detail(self, request, pk=None):
        question = self.get_object()
        serializer = QuestionDetailSerializer(question, context={'request': request})
        return Response(serializer.data)

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
    permission_classes = [IsAuthenticated]

    # Статистика по вопросам
    @action(detail=True, methods=['get'])
    def get_statistic(self, request, pk=None):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)
        user_course = self.get_object()
        if user_course.user != user:
            return Response({'detail': 'Пользователь не проходит этот курс.'}, status=status.HTTP_403_FORBIDDEN)

        # Получаем все записи UserQuestion для данного пользователя и курса
        user_questions = UserQuestion.objects.filter(user=user, question__course=user_course.course)

        if not user_questions.exists():
            return Response({'detail': 'Нет статистики по вопросам для данного курса.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserQuestionStatisticSerializer(user_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # вопросы курса
    @action(detail=True, methods=['get'])
    def course_questions(self, request, pk=None):
        user_course = self.get_object()
        user = request.user

        if not user.is_authenticated:
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)

        if user_course not in list(UserCourse.objects.filter(user=user)):
            return Response({'detail': 'Пользователь не проходит этот курс.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Получаем доступные вопросы из текущей активной ротации
        questions = user_course.course.get_available_questions()
        
        serializer = QuestionDetailSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data)

    #история прохождения тестирования и проверок себя
    @action(detail=True, methods=['get'])
    def course_history(self, request, pk=None):
        user_course = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)

        check_skills = UserCheckSkills.objects.filter(user=user, user_course=user_course)
        tickets = UserTicket.objects.filter(user=user, user_course=user_course)

        # Собираем события в один список и сортируем по времени
        events = []
        for check in check_skills:
            events.append({
                'type': 'check_skill',
                'id': check.id,
                'created_at': check.created_at,
                'status': check.status,
                'difficulty': check.difficulty,
                'question_count': check.question_count
            })

        for ticket in tickets:
            events.append({
                'type': 'ticket',
                'id': ticket.id,
                'created_at': ticket.created_at,
                'status': ticket.status,
                'attempt_count': ticket.attempt_count,
                'right_answers': ticket.right_answers,
                'time_ticket': ticket.time_ticket
            })

        # Сортируем события по времени создания
        events = sorted(events, key=lambda x: x['created_at'])
        return Response(events, status=status.HTTP_200_OK)

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

    # обновление последнего времени посещения курса при get запросе
    def retrieve(self, request, pk=None):
        from django.utils import timezone
        user_course = self.get_object()
        if user_course:
            user_course.last_visited = timezone.now()
            user_course.save()
        serializer = self.get_serializer(user_course)
        return Response(serializer.data)
    
    # Получение последнего посещённого курса пользователя 
    @action(detail=False, methods=['get'], url_path='last-course')
    def last_course(self, request):
        user = request.user
        last_course = UserCourse.objects.filter(user=user).order_by('-last_visited').first()

        if last_course:
            serializer = UserCourseSerializer(last_course)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Пользователь не записан ни на один курс.'}, status=status.HTTP_404_NOT_FOUND)
    
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
        if not user.is_authenticated: 
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_question = self.get_object()
        user_question.selected = True
        user_question.save()
        return Response({'status': 'Вопрос отмечен как избранный'})
    
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
    permission_classes = [IsAuthenticated]

    # завершаем прохождение билета
    @action(detail=True, methods=['post'])
    def end_ticket(self, request, pk=None):
        user = request.user
        if not user.is_authenticated: 
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)

        user_ticket = self.get_object()

        if user_ticket not in list(UserTicket.objects.filter(user=user)):
            return Response({'detail': 'Пользователь не проходил этот билет.'}, status=status.HTTP_403_FORBIDDEN)
        
        user_ticket.update_status()
        user_ticket.update_right_answers()
        user_ticket.update_attempt_count()
        user_ticket.save()

        serializer = UserTicketSerializer(user_ticket, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #генерируем случайный билет для проверки знаний
    @action(detail=False, methods=['post'])
    def generate_random_ticket(self, request):
        from django.utils import timezone
        from datetime import timedelta

        user = request.user
        if not user.is_authenticated: 
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_course_id = request.data.get('user_course_id')
        try:
            user_course = UserCourse.objects.get(id=user_course_id)
            course_id = user_course.course.id
        except UserCourse.DoesNotExist:
            return Response({'detail': 'Пользовательский курс не найден.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'Курс не найден.'}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем доступные вопросы из текущей активной ротации
        questions = user_course.course.get_available_questions()
        print(len(questions))
        random.shuffle(questions)

        total_questions_count = 5

        if (len(questions)) < total_questions_count:
            return Response({'detail': 'Недостаточно вопросов для генерации билета.'}, status=status.HTTP_400_BAD_REQUEST)

        selected_questions = questions[:total_questions_count]

        with transaction.atomic():
            #подкаиваем тестирование
            testing = Testing.objects.get(course=course)

            #создаём билет
            ticket = Ticket.objects.create(
                name=f"Random Ticket for {course_id}",
                difficulty='medium',
                question_count=len(selected_questions),
                testing=testing
            )

            #создаём вопросы в билете
            for i in range(len(selected_questions)):
                question_list = QuestionList.objects.create(
                    ticket=ticket,
                    number_in_ticket=i + 1,  
                    question=selected_questions[i]  
                )

            #создаём его связь со сгенерированным билетом
            user_ticket = UserTicket.objects.create(
                user=user,
                ticket=ticket,
                user_course=user_course,
                status='Not started',
                attempt_count=1,
                right_answers=0,
                time_ticket=timedelta(minutes=30)
            )
            mass =[]
            #создаём связь между пользовательским билетом и вопросами
            for i, question in enumerate(selected_questions):
                temp = QuestionTicket.objects.create(
                    user_ticket=user_ticket,
                    question=question,
                    number_in_ticket=i + 1,
                    user_answer=None,
                    status='Not Answered',
                )
                mass.append(temp)

        serializer = QuestionTicketSerializer(mass, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    # Добавление вопросу уровня запоминания
    @action(detail=True, methods=['post'])
    def post_user_memorization(self, request, pk=None):
        user = request.user
        if not user.is_authenticated: 
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            user_mem = request.data.get('user_memorization')
            if user_mem not in ['New','Bad', 'Satisfactorily', 'Good','Excellent', 'No']:
                return Response({'detail': 'Недопустимый уровень запоминания'}, status=status.HTTP_400_BAD_REQUEST)

            user_answer = self.get_object()
            if user_answer.user != user:
                return Response({'detail': 'Ответ не принадлежит пользователю'}, status=status.HTTP_403_FORBIDDEN)
            if user_answer.correct == 1.0:
                user_answer.user_memorization = user_mem
                user_answer.save()

                uq = UserQuestion.objects.filter(user=user, question=user_answer.question).first()
                uq.calculate_average_memorization()
                return Response({'status': 'Вопросу добавлена степень запоминания'})
            else:
                return Response({'status': 'Пользователь не имеет права изменять статус с неправильным ответом!'})
        except UserAnswer.DoesNotExist:
            return Response({'detail': 'Ответ не найден. Повторите позже'}, status=status.HTTP_404_NOT_FOUND)

class UserAnswerItemViewSet(viewsets.ModelViewSet):
    queryset = UserAnswerItem.objects.all()
    serializer_class = UserAnswerItemSerializer

class QuestionTicketViewSet(viewsets.ModelViewSet):
    queryset = QuestionTicket.objects.all()
    serializer_class = QuestionTicketSerializer

    # создаём ответ на вопрос тестирования
    @action(detail=True, methods=['post'], url_path='create_answer')
    def create_answer(self, request, pk=None):
        from datetime import timedelta

        user = request.user
        if not user.is_authenticated: 
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)

        question_ticket = self.get_object()
        user_answer_items = request.data.get('answer_items')
        answer_time = request.data.get('answer_time')

        with transaction.atomic():
            user_answer = UserAnswer.objects.create(
                question=question_ticket.question,
                user=user,
                answer_time=timedelta(seconds=answer_time),
                correct=0.0,
            )
            question_ticket.user_answer = user_answer
            for index, item in enumerate(user_answer_items):
                UserAnswerItem.objects.create(
                    user_answer=user_answer,
                    answer_varient=Varient.objects.filter(question=question_ticket.question, answer_number=item).first(),
                    order_answer=index + 1,
                )
            user_answer.check_correctness()
            q = UserQuestion.objects.filter(user=user, question=user_answer.question).last()
            q.update_memorization()
            q.save()
            question_ticket.update_status()

        questions_serializer = QuestionTicketSerializer(question_ticket, many=False)
        return Response(questions_serializer.data, status=status.HTTP_201_CREATED)

def separate_questions(difficulty, remaining_count):
    if difficulty == 'Easy':
        bad_count = int(remaining_count * 0.2)
        satisfy_count = int(remaining_count * 0.3)
        good_count = remaining_count - bad_count - satisfy_count
    elif ((difficulty == 'Hard') or (difficulty == 'Extrem')):
        bad_count = int(remaining_count * 0.6)
        satisfy_count = int(remaining_count * 0.3)
        good_count = remaining_count - bad_count - satisfy_count
    else:  # Medium
        bad_count = int(remaining_count * 0.4)
        satisfy_count = int(remaining_count * 0.4)
        good_count = remaining_count - bad_count - satisfy_count
    return [bad_count, satisfy_count, good_count]

class UserCheckSkillsViewSet(viewsets.ModelViewSet):
    queryset = UserCheckSkills.objects.all()
    serializer_class = UserCheckSkillsSerializer

    # завершаем проверь себя
    @action(detail=True, methods=['post'])
    def end_check(self, request, pk=None):
        user = request.user
        if not user.is_authenticated: 
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_check = self.get_object()
        user_check.status = 'Completed'
        # можно добавить число правильных ответов
        user_check.save()

        serializer = UserCheckSkillsSerializer(user_check, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # Создание "умного тестирования"
    @action(detail=False, methods=['post'], url_path='smart-generate-check')
    def smart_generate_check(self, request):
        user = request.user
        if not user.is_authenticated: 
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)

        user_course_id = request.data.get('user_course_id')
        difficulty = request.data.get('difficulty', 'Medium')
        question_count = int(request.data.get('question_count', 20))

        try:
            user_course = UserCourse.objects.get(id=user_course_id)
            course_id = user_course.course.id
        except UserCourse.DoesNotExist:
            return Response({'detail': 'Пользовательский курс не найден.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Создаем запись UserCheckSkills
        user_check_skills = UserCheckSkills.objects.create(
            user=user,
            question_count=question_count,
            status="In Progress",
            difficulty=difficulty,
            user_course=user_course,
        )

        # Получение вопросов из последней ротации
        rotation_questions = user_course.course.get_available_questions()
        rotation_questions_ids = [q.id for q in rotation_questions]
        new_questions = Question.objects.filter(id__in=rotation_questions_ids).exclude(
            id__in=UserQuestion.objects.filter(user=user, question__course_id=course_id).values_list('question_id', flat=True)
        )

        # Деление вопросов по уровню запоминания
        user_questions = UserQuestion.objects.filter(user=user, question__course_id=course_id)
        answered_questions_count = len(user_questions)
        
        answ_new_questions = user_questions.filter(memorization='New')
        bad_questions = user_questions.filter(memorization='Bad')
        satisfy_questions = user_questions.filter(memorization='Satisfactorily')
        good_questions = user_questions.filter(memorization='Good')

        # Если пользователь не отвечал на вопросы, возвращаем просто вопросы
        if answered_questions_count <= int(question_count / 2):
            selected_questions = list(new_questions[:question_count])
        else:
            if new_questions.exists() and new_questions.count() >= int(question_count / 2):
                new_questions_count = question_count // 2
            else:
                new_questions_count = new_questions.count()

            remaining_count = question_count - new_questions_count
            
            bad_count, satisfy_count, good_count = separate_questions(difficulty, remaining_count)
            
            selected_bad_questions = list(bad_questions.order_by('?')[:bad_count])
            selected_satisfy_questions = list(satisfy_questions.order_by('?')[:satisfy_count])
            selected_good_questions = list(good_questions.order_by('?')[:good_count])

            answ_new_count = 0
            if len(selected_bad_questions) + len(selected_satisfy_questions) + len(selected_good_questions) < remaining_count:
                answ_new_count = remaining_count - (len(selected_bad_questions) + len(selected_satisfy_questions) + len(selected_good_questions))
            selected_new_questions = list(answ_new_questions.order_by('?')[:answ_new_count])
            
            new_questions = list(new_questions[:new_questions_count])

            selected_questions = list(new_questions) + list(selected_new_questions) + list(selected_bad_questions) + list(selected_satisfy_questions) + list(selected_good_questions)

            remaining_needed = question_count - len(selected_questions)
            if remaining_needed > 0:
                remaining_questions = list(user_questions.filter(memorization='Bad').exclude(question__id__in=[q.id for q in selected_questions]).order_by('?')[:remaining_needed])
                remaining_needed -= len(remaining_questions)
                if remaining_needed > 0:
                    more_questions = list(user_questions.filter(memorization='Satisfactorily').exclude(question__id__in=[q.id for q in selected_questions]).order_by('?')[:remaining_needed])
                    remaining_questions += more_questions
                    remaining_needed -= len(more_questions)
                if remaining_needed > 0:
                    more_questions = list(user_questions.filter(memorization='Good').exclude(question__id__in=[q.id for q in selected_questions]).order_by('?')[:remaining_needed])
                    remaining_questions += more_questions
                selected_questions += remaining_questions

        # Проверяем, чтобы выбранное количество вопросов совпадало с необходимым
        if len(selected_questions) < question_count:
            missing_count = question_count - len(selected_questions)
            additional_questions = list(rotation_questions.exclude(id__in=[q.id for q in selected_questions]).order_by('?')[:missing_count])
            selected_questions += additional_questions

        user_check_skills.question_count = len(selected_questions)
        user_check_skills.save()

        with transaction.atomic():
            created_questions = []
            for index, question in enumerate(selected_questions):
                if isinstance(question, UserQuestion):
                    question = question.question
                created_question = UserCheckSkillsQuestion.objects.create(
                    user_check_skills=user_check_skills,
                    question=question,
                    number_in_check=index + 1,
                    status='Not Answered',
                    user_answer=None,
                )
                created_questions.append(created_question)

            for question in new_questions:
                UserQuestion.objects.create(
                    question=question,
                    user=user,
                    selected=False,
                    memorization='New',
                )

        questions_serializer = UserCheckSkillsQuestionSerializer(created_questions, many=True)
        return Response(questions_serializer.data, status=status.HTTP_201_CREATED)
    
class UserCheckSkillsQuestionViewSet(viewsets.ModelViewSet):
    queryset = UserCheckSkillsQuestion.objects.all()
    serializer_class = UserCheckSkillsQuestionSerializer

    @action(detail=True, methods=['post'], url_path='create_answer')
    def create_answer(self, request, pk=None):
        from datetime import timedelta

        user = request.user
        if not user.is_authenticated: 
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_check_skills_question = self.get_object()
        except UserCheckSkillsQuestion.DoesNotExist:
            return Response({'detail': 'Вопрос не найден.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'Произошла ошибка при получении вопроса: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user_answer_items = request.data.get('answer_items')
        answer_time = request.data.get('answer_time')

        if not user_answer_items:
            return Response({'detail': 'Ответы не найдены.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                try:
                    user_answer = UserAnswer.objects.create(
                        question=user_check_skills_question.question,
                        user=user,
                        answer_time=timedelta(seconds=answer_time),
                        correct=0.0,
                    )
                except Exception as e:
                    return Response({'detail': f'Ошибка при создании ответа пользователя: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                user_check_skills_question.user_answer = user_answer

                try:
                    for index, item in enumerate(user_answer_items):
                        answer_variant = Varient.objects.filter(question=user_check_skills_question.question, answer_number=item).first()
                        if not answer_variant:
                            return Response({'detail': f'Вариант ответа с номером {item} не найден.'}, status=status.HTTP_400_BAD_REQUEST)

                        UserAnswerItem.objects.create(
                            user_answer=user_answer,
                            answer_varient=answer_variant,
                            order_answer=index + 1,
                        )
                except Exception as e:
                    return Response({'detail': f'Ошибка при создании элементов ответа пользователя: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                try:
                    user_answer.check_correctness()
                except Exception as e:
                    return Response({'detail': f'Ошибка при проверке корректности ответа: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                try:
                    q = UserQuestion.objects.filter(user=user, question=user_answer.question).last()
                    if q:
                        try:
                            q.update_memorization()
                        except Exception as e:
                            return Response({'detail': f'Ошибка при обновлении данных запоминания: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                        try:
                            q.save()
                        except Exception as e:
                            return Response({'detail': f'Ошибка при сохранении данных о вопросе пользователя: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response({'detail': 'Вопрос пользователя не найден.'}, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        user_check_skills_question.update_status()
                    except Exception as e:
                        return Response({'detail': f'Ошибка при обновлении статуса вопроса: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                except Exception as e:
                    return Response({'detail': f'Общая ошибка при обновлении данных вопроса пользователя: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            questions_serializer = UserCheckSkillsQuestionSerializer(user_check_skills_question, many=False)
            return Response(questions_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': f'Произошла ошибка при обработке ответа: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)