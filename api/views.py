from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.models import CustomUser
from course.models import Qualification, Block, NormativeDocument, Course, Testing, Ticket, Question, Varient, QuestionList, LearningMaterial
from .serializers import QualificationSerializer, BlockSerializer, NormativeDocumentSerializer, QuestionDetailSerializer, CourseSerializer, TestingSerializer, TicketSerializer, QuestionSerializer, VarientSerializer, QuestionListSerializer, LearningMaterialSerializer
from usercourse.models import UserCourse, TaskQuestion, UserQuestion, UserTicket, UserAnswer, UserAnswerItem, QuestionTicket, UserCheckSkills, UserCheckSkillsQuestion
from .serializers import UserCourseSerializer, TaskQuestionSerializer, UserQuestionSerializer, UserTicketSerializer, UserAnswerSerializer, UserAnswerItemSerializer, QuestionTicketSerializer, UserCheckSkillsSerializer, UserCheckSkillsQuestionSerializer
import random
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
    
    # проверка правильности (пока вопросов больше чем ответов)
    @action(detail=True, methods=['post'], url_path='check-answer')
    def check_answer(self, request, pk=None):
        from datetime import timedelta
        question = self.get_object()
        answer_ids = request.data.get('answers', [])
        correct_answers = Varient.objects.filter(question=question, correct=True).values_list('id', flat=True)

        is_correct = set(answer_ids) == set(correct_answers)
        user = request.user

        # Обновление или создание объекта UserAnswer
        user_answer, created = UserAnswer.objects.get_or_create(
            user=user,
            question=question,
            defaults={'correct': is_correct, 'answer_time': timedelta(seconds=10)}  # Временное значение времени ответа
        )
        if not created:
            user_answer.correct = is_correct
            user_answer.save()

        response_data = {'is_correct': is_correct,}

        if not is_correct:
            question_serializer = QuestionDetailSerializer(question)
            response_data['details'] = question_serializer.data
        return Response(response_data)

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

    @action(detail=False, methods=['post'])
    def generate_random_ticket(self, request):
        from django.utils import timezone
        from datetime import timedelta
        from django.db import transaction

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

        user_questions = UserQuestion.objects.filter(user=user, question__course=course)
        new_questions = Question.objects.filter(course=course).exclude(id__in=user_questions.values('question_id')).order_by('?')
        good_questions = user_questions.filter(memorization__in=['Good', 'Excellent']).order_by('?')
        bad_satisfy_questions = user_questions.filter(memorization__in=['Bad', 'Satisfy']).order_by('?')

        new_questions = list(new_questions)
        good_questions = list(good_questions)
        bad_satisfy_questions = list(bad_satisfy_questions)

        random.shuffle(new_questions)
        random.shuffle(good_questions)
        random.shuffle(bad_satisfy_questions)

        total_questions_count = 40

        new_questions_count = int(total_questions_count * 0.1)
        good_questions_count = int(total_questions_count * 0.3)
        bad_satisfy_questions_count = total_questions_count - new_questions_count - good_questions_count
        
        if (good_questions_count + bad_satisfy_questions_count) < 36:
            new_questions_count = 40 - (good_questions_count + bad_satisfy_questions_count)

        if (new_questions_count + good_questions_count + bad_satisfy_questions_count) < total_questions_count:
            return Response({'detail': 'Недостаточно вопросов для генерации билета.'}, status=status.HTTP_400_BAD_REQUEST)

        selected_new_questions = new_questions[:new_questions_count]
        selected_good_questions = good_questions[:good_questions_count]
        selected_bad_satisfy_questions = bad_satisfy_questions[:bad_satisfy_questions_count]

        selected_questions = selected_new_questions + selected_good_questions + selected_bad_satisfy_questions
        random.shuffle(selected_questions)

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
                    number_in_ticket=i,  
                    question=selected_questions[i]  
                )

            # #получаем курс пользователя
            # user_course = UserCourse.objects.filter(user=user, course=course).first()
            # if not user_course:
            #     return Response({'detail': 'UserCourse не найден.'}, status=status.HTTP_400_BAD_REQUEST)

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

            #создаём связь между пользовательским билетом и вопросами
            for i, question in enumerate(selected_questions):
                QuestionTicket.objects.create(
                    user_ticket=user_ticket,
                    question=question,
                    number_in_ticket=i + 1,
                    user_answer=None,
                )

        serializer = UserTicketSerializer(user_ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    # Создать или обновить ответ пользователя
    @action(detail=False, methods=['post'])
    def create_or_update(self, request):
        user = request.user
        question_id = request.data.get('question_id')
        #продумать ответы! слабое место
        answer_ids = request.data.get('answer_ids')
        is_correct = request.data.get('is_correct')
        
        if not question_id:
            return Response({'detail': 'Question ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_answer, created = UserAnswer.objects.get_or_create(user=user, question_id=question_id)
        user_answer.answer_ids = answer_ids
        user_answer.correct = is_correct
        user_answer.save()

        serializer = UserAnswerSerializer(user_answer)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserAnswerItemViewSet(viewsets.ModelViewSet):
    queryset = UserAnswerItem.objects.all()
    serializer_class = UserAnswerItemSerializer

class QuestionTicketViewSet(viewsets.ModelViewSet):
    queryset = QuestionTicket.objects.all()
    serializer_class = QuestionTicketSerializer

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
        
    # создаём "умное тестирование", которое даёт 50% новых вопросов
    @action(detail=False, methods=['post'], url_path='smart-generate-check')
    def smart_generate_check(self, request):
        from django.db import transaction

        # Получаем не по сессии, а по айди!
        user_id = request.data.get('user_id')
        user = CustomUser.objects.get(id=user_id)

        user_course_id = request.data.get('user_course_id')
        difficulty = request.data.get('difficulty', 'Medium')
        question_count = int(request.data.get('question_count', 20))

        try:
            user_course = UserCourse.objects.get(id=user_course_id)
            course_id = user_course.course.id
        except UserCourse.DoesNotExist:
            return Response({'detail': 'Пользовательский курс не найден.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Временно уберём проверку на авторизацию
        # user = request.user
        # if not user.is_authenticated: 
        #     return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_check_skills = UserCheckSkills.objects.create(
            user=user,
            question_count=question_count,
            status="In Progress",
            difficulty=difficulty,
            user_course=user_course,
        )

        user_questions = UserQuestion.objects.filter(user=user, question__course_id=course_id)
        answered_questions_count = len(user_questions)
        
        new_questions = list(Question.objects.filter(course_id=course_id).order_by('?'))
        random.shuffle(new_questions)
        new_questions = list(new_questions[:question_count])

        # Делим вопросы по уровню запоминания
        answ_new_questions = user_questions.filter(memorization='New')
        bad_questions = user_questions.filter(memorization='Bad')
        satisfy_questions = user_questions.filter(memorization='Satisfy')
        good_questions = user_questions.filter(memorization='Good')

        # Если пользователь не отвечал на вопросы, возвращаем просто вопросы
        if answered_questions_count <= int(question_count / 2):
            # считаем, что в курсе изначально хватает вопросов, но лучше сделать обработку!
            selected_questions = list(new_questions)
        else:
            new_questions = Question.objects.filter(course_id=course_id).exclude(id__in=user_questions.values('question_id')).order_by('?')
            if len(new_questions) >= int(question_count / 2): # Если хватает, берем 50% новых вопросов
                new_questions_count = question_count // 2
            else: # Или сколько есть
                new_questions_count = len(new_questions)

            remaining_count = question_count - new_questions_count
            # Оставшиеся 50% делим между "Bad", "Satisfy" и "Good" вопросами с учетом сложности
            bad_count, satisfy_count, good_count = separate_questions(difficulty, remaining_count)

            selected_bad_questions = list(bad_questions.order_by('?')[:bad_count])
            selected_satisfy_questions = list(satisfy_questions.order_by('?')[:satisfy_count])
            selected_good_questions = list(good_questions.order_by('?')[:good_count])

            # добавляем вопросы, которые были оставлены без ответов при прохождении
            answ_new_count = 0
            if len(selected_bad_questions) + len(selected_satisfy_questions) + len(selected_good_questions) < remaining_count:
                answ_new_count = remaining_count - (len(selected_bad_questions) + len(selected_satisfy_questions) + len(selected_good_questions))
            selected_new_questions = answ_new_questions.order_by('?')[:answ_new_count]
            
            # добавляем новые вопросы (которые ещё не встречались)
            if len(selected_bad_questions) + len(selected_satisfy_questions) + len(selected_good_questions) + len(selected_new_questions) < question_count:
                new_questions_count = question_count - (len(selected_bad_questions) + len(selected_satisfy_questions) + len(selected_good_questions) + len(selected_new_questions))
            new_questions = new_questions[:new_questions_count]

            selected_questions = list(new_questions) + list(selected_new_questions) + list(selected_bad_questions) + list(selected_satisfy_questions) + list(selected_good_questions)

            #добавляем случай, когда надо добавить просто вопросы, чтобы сохранить +- пропорцию.
            remaining_needed = question_count - len(selected_questions)
            if remaining_needed > 0:
                remaining_questions = list(user_questions.filter(memorization='Bad').exclude(id__in=[q.id for q in selected_questions]).order_by('?')[:remaining_needed])
                remaining_needed -= len(remaining_questions)
                if remaining_needed > 0:
                    more_questions = list(user_questions.filter(memorization='Satisfy').exclude(id__in=[q.id for q in selected_questions]).order_by('?')[:remaining_needed])
                    remaining_questions += more_questions
                    remaining_needed -= len(more_questions)
                    if remaining_needed > 0:
                        more_questions = list(user_questions.filter(memorization='Good').exclude(id__in=[q.id for q in selected_questions]).order_by('?')[:remaining_needed])
                        remaining_questions += more_questions
                        remaining_needed -= len(more_questions)
                selected_questions += more_questions
            random.shuffle(selected_questions)

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

            # создание UserQuestion
            # Для новых вопросов необходимо создать отношение UserQuestion
            for index in range(len(new_questions)):
                UserQuestion.objects.create(
                    question=new_questions[index],
                    user=user,
                    selected=False,
                    memorization='New',
                )

        questions_serializer = UserCheckSkillsQuestionSerializer(created_questions, many=True)
        return Response(questions_serializer.data, status=status.HTTP_201_CREATED)
    
class UserCheckSkillsQuestionViewSet(viewsets.ModelViewSet):
    queryset = UserCheckSkillsQuestion.objects.all()
    serializer_class = UserCheckSkillsQuestionSerializer