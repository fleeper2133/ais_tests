from rest_framework import serializers
from course.models import Qualification, Block, NormativeDocument, Course, Testing, Ticket, Question, Varient, QuestionList, LearningMaterial
from usercourse.models import UserCourse, TaskQuestion, UserQuestion, UserTicket, UserAnswer, UserAnswerItem, QuestionTicket, UserCheckSkills, UserCheckSkillsQuestion, UserDays

class UserDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDays
        fields = ['id', 'user', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'week_start']

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'

class NormativeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormativeDocument
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    testing = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_testing(self, obj):
        testing = Testing.objects.filter(course=obj).first()
        if testing:
            # Передаем контекст, включая request, в TestingSerializer
            return TestingSerializer(testing, context=self.context).data
        return None

class TicketSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'name', 'difficulty', 'question_count', 'status']
    
    def get_status(self, obj):
        user = self.context['request'].user
        user_ticket = UserTicket.objects.filter(user=user, ticket=obj).last()
        return user_ticket.status if user_ticket else False

class TestingSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True, source='ticket_set')

    class Meta:
        model = Testing
        fields = ['id', 'course', 'description', 'price', 'tickets'] 

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class VarientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Varient
        fields = ['id', 'answer_number', 'answer_text', 'correct', 'expert_check']

class QuestionDetailSerializer(serializers.ModelSerializer):
    selected = serializers.SerializerMethodField()
    normative_documents = NormativeDocumentSerializer(source='ndocument', read_only=True)
    varients = VarientSerializer(source='varient_set', many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'name', 'question_text', 'explanations', 'normative_documents', 'varients', 'selected', 'normative_point']

    def get_selected(self, obj):
        user = self.context['request'].user
        user_question = UserQuestion.objects.filter(user=user, question=obj).first()
        return user_question.selected if user_question else False

class QuestionTicketDetailSerializer(serializers.ModelSerializer):
    question_ticket_id = serializers.IntegerField(source='id')
    name = serializers.CharField(source='question.name')
    question_text = serializers.CharField(source='question.question_text')
    explanations = serializers.CharField(source='question.explanations')
    normative_documents = NormativeDocumentSerializer(source='question.ndocument', read_only=True)
    varients = VarientSerializer(source='question.varient_set', many=True, read_only=True)
    selected = serializers.SerializerMethodField()

    class Meta:
        model = QuestionTicket
        fields = ['question_ticket_id', 'name', 'question_text', 'explanations', 'normative_documents', 'varients', 'selected']

    def get_selected(self, obj):
        user = self.context['request'].user
        user_question = UserQuestion.objects.filter(user=user, question=obj.question).first()
        return user_question.selected if user_question else False

class QuestionListSerializer(serializers.ModelSerializer):
    question = QuestionDetailSerializer()

    class Meta:
        model = QuestionList
        fields = '__all__'

class LearningMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningMaterial
        fields = '__all__'

class UserCourseSerializer(serializers.ModelSerializer):
    good_memorization_count = serializers.SerializerMethodField()
    bad_memorization_count = serializers.SerializerMethodField()
    medium_memorization_count = serializers.SerializerMethodField()

    class Meta:
        model = UserCourse
        fields = '__all__'

    def get_good_memorization_count(self, obj):
        user = self.context['request'].user
        available_questions = obj.course.get_available_questions()  # Получаем доступные вопросы для курса
        return UserQuestion.objects.filter(
            user=user, 
            question__in=available_questions,  # Фильтруем вопросы, которые находятся в ротации
            memorization__in=['Good', 'Excellent']  # Учитываем "Good" и "Excellent"
        ).count()

    def get_bad_memorization_count(self, obj):
        user = self.context['request'].user
        available_questions = obj.course.get_available_questions()  # Получаем доступные вопросы для курса
        return UserQuestion.objects.filter(
            user=user, 
            question__in=available_questions,  # Фильтруем вопросы, которые находятся в ротации
            memorization__in=['Bad', 'New']  # Учитываем "Bad" и "New"
        ).count()

    def get_medium_memorization_count(self, obj):
        user = self.context['request'].user
        available_questions = obj.course.get_available_questions()  # Получаем доступные вопросы для курса
        return UserQuestion.objects.filter(
            user=user, 
            question__in=available_questions,  # Фильтруем вопросы, которые находятся в ротации
            memorization='Satisfactorily'  # Учитываем только "Satisfactorily"
        ).count()

class TaskQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskQuestion
        fields = '__all__'

class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestion
        fields = '__all__'

class UserQuestionStatisticSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(source='question.id')
    user_question_id = serializers.IntegerField(source='id')
    question_text = serializers.CharField(source='question.question_text')
    answers = serializers.SerializerMethodField()

    class Meta:
        model = UserQuestion
        fields = ['user_question_id', 'question_id', 'question_text', 'correct_count', 
                  'incorrect_count', 'average_answer_time', 'selected', 'memorization', 'answers']

    def get_answers(self, obj):
        user_answers = UserAnswer.objects.filter(user=obj.user, question=obj.question)
        return UserAnswerSerializer(user_answers, many=True).data
    
class UserTicketSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = UserTicket
        fields = ['id', 'ticket', 'time_ticket', 'status', 'user', 'attempt_count', 'updated_at', 'right_answers', 'questions']

    def get_questions(self, obj):
        request = self.context.get('request', None)
        questions = Question.objects.filter(questionlist__ticket=obj.ticket).order_by('questionlist__number_in_ticket')
        #return QuestionDetailSerializer(questions, many=True, context={'request': request}).data
        serialized_data = QuestionDetailSerializer(questions, many=True, context={'request': request}).data

        # Добавляем question_ticket_id к каждому вопросу
        question_tickets = QuestionTicket.objects.filter(user_ticket=obj)

        # Создаем словарь для быстрого поиска question_ticket по question_id
        question_ticket_map = {qt.question_id: qt.id for qt in question_tickets}

        # Добавляем question_ticket_id в каждую запись вопроса
        for question_data in serialized_data:
            question_id = question_data['id']
            question_ticket_id = question_ticket_map.get(question_id)
            question_data['question_ticket_id'] = question_ticket_id

        return serialized_data
    
        # questions = QuestionTicket.objects.filter(user_ticket=obj).order_by('number_in_ticket')
        # return QuestionTicketDetailSerializer(questions, many=True, context={'request': request}).data

class UserAnswerSerializer(serializers.ModelSerializer):
    user_answer_items = serializers.SerializerMethodField()
    question_id = serializers.IntegerField(source='question.id')
    question_text = serializers.CharField(source='question.question_text')
    
    class Meta:
        model = UserAnswer
        fields = ['question_id', 'question_text', 'correct', 'answer_time', 'created_at', 'user_answer_items']

    def get_user_answer_items(self, obj):
        user_answer_items = UserAnswerItem.objects.filter(user_answer=obj)
        return UserAnswerItemSerializer(user_answer_items, many=True).data

class UserAnswerItemSerializer(serializers.ModelSerializer):
    answer_varient_id = serializers.IntegerField(source='answer_varient.id')
    answer_varient_text = serializers.CharField(source='answer_varient.answer_text')
    correct = serializers.BooleanField(source='answer_varient.correct')

    class Meta:
        model = UserAnswerItem
        fields = ['answer_varient_id', 'answer_varient_text', 'correct', 'order_answer']

class QuestionTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTicket
        fields = '__all__'

class UserCheckSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCheckSkills
        fields = '__all__'

class UserCheckSkillsQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCheckSkillsQuestion
        fields = ['id', 'user_check_skills', 'question', 'number_in_check', 'user_answer', 'status']