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

class QuestionDetailSerializer(serializers.ModelSerializer):
    normative_documents = NormativeDocumentSerializer(source='ndocument', read_only=True)

    class Meta:
        model = Question
        fields = ['name', 'question_text', 'explanations', 'normative_documents']

class VarientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Varient
        fields = '__all__'

class QuestionListSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = UserTicket
        fields = '__all__'

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
