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
    class Meta:
        model = Course
        fields = '__all__'

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

class CourseQuestionDetailSerializer(serializers.ModelSerializer):
    selected = serializers.SerializerMethodField()
    varients = VarientSerializer(source='varient_set', many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'name', 'question_text', 'course', 'selected', 'varients']

    def get_selected(self, obj):
        user = self.context['request'].user
        user_question = UserQuestion.objects.filter(user=user, question=obj).first()
        return user_question.selected if user_question else False

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

class UserTicketSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = UserTicket
        fields = ['id', 'ticket', 'time_ticket', 'status', 'user', 'attempt_count', 'updated_at', 'right_answers', 'questions']

    def get_questions(self, obj):
        question_list = QuestionList.objects.filter(ticket=obj.ticket).order_by('number_in_ticket')
        return QuestionListSerializer(question_list, many=True).data

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'

class UserAnswerItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswerItem
        fields = '__all__'

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
