from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import json

# Квалификация
class Qualification(models.Model):
    title = models.TextField()
    code = models.CharField(max_length=10)
    level = models.PositiveIntegerField()

# Блоки вопросов
class Block(models.Model):
    title = models.TextField()
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)

# Нормативные документы
class NormativeDocument(models.Model):
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    document_link = models.URLField(null=True, blank=True)
    
# Курсы
class Course(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    version = models.CharField(max_length=255)
    available_until = models.DateField()
    question_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_link = models.ImageField(null=True, blank=True, upload_to="courses/", default='courses/default.png')
    user_marks = models.PositiveIntegerField(default=0)
    qualification = models.OneToOneField('Qualification', on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    # функция по вычислению оценки курса
    def update_course_mark(self):
        from usercourse.models import UserCourse
        user_courses = UserCourse.objects.filter(course=self)
        total_marks = sum(user_course.mark for user_course in user_courses if user_course.mark is not None)
        mark_count = user_courses.filter(mark__isnull=False).count()
        if mark_count > 0:
            self.user_marks = total_marks / mark_count
        else:
            self.user_marks = 0
        self.save()

# Тестирования
class Testing(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.PositiveIntegerField()

# Билеты
class Ticket(models.Model):
    variety = [
        ('easy', 'Легко'),
        ('medium', 'Средне'),
        ('hard', 'Сложно'),
        ('extrem', 'Невозможно'),
    ]
    #Номер билета или name?
    name = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=255, choices=variety)
    question_count = models.PositiveIntegerField(default=10)
    testing = models.ForeignKey(Testing, on_delete=models.CASCADE)

    #определение сложности билета по входящим в него вопросам
    def determine_difficulty(self):
        questions = Question.objects.filter(course=self.testing.course)
        difficulty_counts = {'easy': 0, 'medium': 0, 'hard': 0, 'extrem': 0,}
        for question in questions:
            difficulty_counts[question.difficulty] += 1
        self.difficulty = max(difficulty_counts, key=difficulty_counts.get)
        self.save()

# Вопросы
class Question(models.Model):
    variety = [
        ('easy', 'Легко'),
        ('medium', 'Средне'),
        ('hard', 'Сложно'),
        ('extrem', 'Невозможно'),
    ]
    name = models.CharField(max_length=255, null=True, blank=True)
    question_text = models.TextField()
    topic = models.CharField(max_length=255, null=True, blank=True) 
    difficulty = models.CharField(max_length=255, choices=variety)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    explanations = models.CharField(max_length=255, default=None,null=True, blank=True)
    explanation_material = models.ForeignKey('LearningMaterial', on_delete=models.SET_NULL, null=True, blank=True)
    right_answer_count = models.PositiveIntegerField(default=1)
    answer_count = models.PositiveIntegerField(default=1)
    ndocument = models.ForeignKey('NormativeDocument', on_delete=models.SET_NULL, null=True, blank=True)
    block = models.ForeignKey('Block', on_delete=models.SET_NULL, null=True, blank=True)

    # написать функции для вычисления
    def calculate_right_answer_count(self):
        self.right_answer_count = self.varient_set.filter(correct=True).count()
        self.save()

    def calculate_answer_count(self):
        self.answer_count = self.varient_set.count()
        self.save()

class Varient(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_number = models.PositiveIntegerField(default=1)
    answer_text = models.TextField()
    correct = models.BooleanField(default=False)
    expert_check = models.BooleanField(default=False)

# Список вопросов
class QuestionList(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, db_index=True)
    number_in_ticket = models.PositiveIntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_index=True)

# Учебные материалы
class LearningMaterial(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year_of_issue = models.PositiveIntegerField()
    document_link = models.URLField(null=True, blank=True)