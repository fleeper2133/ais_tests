from rest_framework import serializers
from course.models import Qualification, Block, NormativeDocument, Course, Testing, Ticket, Question, Varient, QuestionList, LearningMaterial
from usercourse.models import UserCourse, TaskQuestion, UserQuestion, UserTicket, UserAnswer, UserAnswerItem, QuestionTicket, UserCheckSkills, UserCheckSkillsQuestion

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
            return TestingSerializer(testing).data
        return None

class TestingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testing
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

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
        fields = ['id', 'name', 'question_text', 'explanations', 'normative_documents', 'varients', 'selected']

    def get_selected(self, obj):
        user = self.context['request'].user
        user_question = UserQuestion.objects.filter(user=user, question=obj).first()
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
    class Meta:
        model = UserCourse
        fields = '__all__'

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
        question_list = QuestionList.objects.filter(ticket=obj.ticket).order_by('number_in_ticket')
        return QuestionListSerializer(question_list, many=True).data

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