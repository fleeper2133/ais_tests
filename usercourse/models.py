from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from course.models import Course, Testing, Ticket, QuestionList, Question, Varient
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
    
# Курсы пользователя
class UserCourse(models.Model):
    stat = [
        ('New', 'Новый'),
        ('In progress', 'В процессе'),
        ('Completed', 'Пройденный'),
        ('Delayed', 'Отложенный'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, db_index=True, null=True, blank=True)
    start_date = models.DateField()
    progress = models.PositiveIntegerField()
    status = models.CharField(max_length=255, default='New', choices=stat, null=True, blank=True)
    last_visited = models.DateTimeField(default=timezone.now)
    #для отзыва по курсу
    selected = models.BooleanField(default=False)  # как избранный
    review_text = models.TextField(null=True, blank=True)
    mark = models.PositiveIntegerField(null=True, blank=True)

    # написать функцию, которая автоматически вычисляет прогресс курса, на основании сданных билетов из тестирования
    def calculate_progress(self):
        tickets = UserTicket.objects.filter(user=self.user, ticket__testing__course=self.course)
        completed_tickets = tickets.filter(status='Done').count()
        total_tickets = Ticket.objects.filter(testing__course=self.course).count()

        if total_tickets > 0:
            self.progress = int((completed_tickets / total_tickets) * 100)
        else:
            self.progress = 0
        self.save()
    #модернизировать и интегрировать вместе с вопросами с excelent из всех?

# Вопросы по заданию от пользователя
class TaskQuestion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    message = models.TextField()

# Связь конкретного пользователя и конкретного вопроса 
class UserQuestion(models.Model):
    degree = [
        ('New', 'Новый'),
        ('Bad', 'Плохо'),
        ('Satisfactorily', 'Удовлетворительно'),
        ('Good', 'Хорошо'),
        ('Excellent', 'Блистательно'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    memorization = models.CharField(max_length=255, choices=degree, default='New')
    selected = models.BooleanField()  # как избранный
    correct_count = models.PositiveIntegerField(default=0)
    incorrect_count = models.PositiveIntegerField(default=0)
    average_answer_time = models.DurationField(default=timedelta()) #проверить на изменение при миграциях (удалить скобки при необходимости)
    force_downgrade_flag = models.BooleanField(default=False)
    consecutive_incorrect_count = models.PositiveIntegerField(default=0)

    #степень запоминания
    def update_memorization(self):
        if self.force_downgrade_flag:
            self.memorization = 'Bad'
        else:
            total_attempts = self.correct_count + self.incorrect_count
            if total_attempts == 0:
                self.memorization = 'New'
            else:
                correct_ratio = self.correct_count / total_attempts
                if correct_ratio < 0.25:
                    self.memorization = 'Bad'
                elif correct_ratio < 0.5:
                    self.memorization = 'Satisfactorily'
                elif correct_ratio < 0.75:
                    self.memorization = 'Good'
                else:
                    self.memorization = 'Excellent'
        self.save()

    def update_counts_and_average_time(self):
        answers = UserAnswer.objects.filter(user=self.user, question=self.question)
        self.correct_count = answers.filter(correct=True).count()
        self.incorrect_count = answers.filter(correct=False).count()
        total_time = sum((answer.answer_time for answer in answers), timedelta())
        self.average_answer_time = total_time / answers.count() if answers.exists() else timedelta()
        self.update_memorization()

    #последовательность последних неправильных ответов
    def update_consecutive_incorrect(self):
        answers = UserAnswer.objects.filter(user=self.user, question=self.question).order_by('-id')
        self.consecutive_incorrect_count = 0
    
        for answer in answers:
            if answer.correct:
                break
            self.consecutive_incorrect_count += 1
        
        self.force_downgrade_flag = (self.consecutive_incorrect_count >= 3)
        self.update_memorization()


# Билет пользователя
class UserTicket(models.Model):
    variety = [
        ('Not started', 'Не пройден'),
        ('Done','Сдан'),
        ('Failed','Не сдан'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, db_index=True)
    status = models.CharField(max_length=255, choices=variety, default='Not started')
    attempt_count = models.PositiveIntegerField() #номер попытки
    right_answers = models.PositiveIntegerField(default=0) #количество правильных ответов в билете
    time_ticket = models.DurationField(default=timedelta())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE)
    
    # Автоматическое заполнение поля user_course
    def save(self, *args, **kwargs):
        if not self.user_course:
            try:
                self.user_course = UserCourse.objects.get(user=self.user, course=self.ticket.testing.course)
            except UserCourse.DoesNotExist:
                pass # Если нет подходящего UserCourse, оставляем поле пустым
        super(UserTicket, self).save(*args, **kwargs)

    # автоматический подсчёт номера попытки *
    def update_attempt_count(self):
        self.attempt_count = UserTicket.objects.filter(user=self.user, ticket=self.ticket).count()
        self.save()

    # автоматический подсчёт количества правильных ответов в билете
    def update_right_answers(self):
        right_answers = QuestionTicket.objects.filter(user_ticket=self, status='Right').count()
        self.right_answers = right_answers
        self.save()

    # автоматический подсчёт статуса билета, на основании правильных ответов пользователя. От 60% правильных
    def update_status(self):
        if self.right_answers / self.ticket.question_count >= 0.6:
            self.status = 'Done'
        else:
            self.status = 'Failed'
        self.save()

# Ответ пользователя
class UserAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_index=True)
    correct = models.FloatField(default=0.0) #1 - полностью правильно
    answer_time = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)

    #написать функцию, которая автоматически определяет правильность, обращаться к UserAnswerItem и Varient
    def check_correctness(self):
        correct_answers = self.question.varient_set.filter(correct=True)
        total_correct_count = correct_answers.count()
        selected_correct_count = self.useransweritem_set.filter(answer_varient__in=correct_answers).count()
        selected_answers_count = self.useransweritem_set.count()
        incorrect_answers_count = selected_answers_count - selected_correct_count

        if total_correct_count > 0:
            correctness_score = selected_correct_count / total_correct_count - incorrect_answers_count / selected_answers_count
            self.correct = max(correctness_score, 0)  # Процент правильности не может быть отрицательным
        else:
            self.correct = 0.0

        self.save(update_fields=['correct'])

class UserAnswerItem(models.Model):
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE)
    answer_varient = models.ForeignKey(Varient, on_delete=models.CASCADE)
    order_answer = models.PositiveIntegerField(default=1)

# Вопрос билета
class QuestionTicket(models.Model):
    variety = [
        ('Not Answered', 'Не отвечен'),
        ('Right','Верно'),
        ('Wrong','Не верно'),
    ]
    user_ticket = models.ForeignKey(UserTicket, on_delete=models.CASCADE)
    number_in_ticket = models.PositiveIntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_index=True, null=True, blank=True)
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=255, choices=variety, default='Not Answered')

    # подтягивать статус из последнего UserAnswer
    def update_status(self):
        latest_user_answer = UserAnswer.objects.filter(user=self.user_ticket.user, question=self.user_answer.question).latest('id')
        self.status = 'Right' if latest_user_answer.correct == 1.0 else 'Wrong'
        self.save()

    # номер в билете брать из модели QuestionList
    def update_number_in_ticket(self):
        try:
            question_list_entry = QuestionList.objects.get(ticket=self.user_ticket.ticket, question=self.user_answer.question)
            self.number_in_ticket = question_list_entry.number_in_ticket
        except QuestionList.DoesNotExist:
            self.number_in_ticket = None
        self.save()

# Проверка знаний пользователя (check your self)
class UserCheckSkills(models.Model):
    variety = [
        ('Easy', 'Легко'),
        ('Medium', 'Средне'),
        ('Hard', 'Сложно'),
        ('Extrem', 'Невозможно'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question_count = models.PositiveIntegerField()  # Число выбранных вопросов
    status = models.CharField(max_length=255, choices=[('In Progress', 'В процессе'), ('Completed', 'Завершено')])
    difficulty = models.CharField(max_length=255, choices=variety, default='Medium', null=True, blank=True)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE, null=True, blank=True)

    def update_status(self):
        # Проверка, все ли вопросы были отвечены
        unanswered_questions = self.usercheckskillsquestion_set.filter(status='Not Answered').count()
        if unanswered_questions == 0:
            self.status = 'Completed'
        else:
            self.status = 'In Progress'
        self.save()
        
# Вопросы в проверке знаний пользователя (тренинг)
class UserCheckSkillsQuestion(models.Model):
    variety = [
        ('Not Answered', 'Не отвечен'),
        ('Right','Верно'),
        ('Wrong','Не верно'),
    ]
    user_check_skills = models.ForeignKey(UserCheckSkills, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number_in_check = models.PositiveIntegerField()  # Номер вопроса в тренинге
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=255, choices=variety, default='Not Answered')
    
    # подтягивать статус из последнего UserAnswer
    def update_status(self):
        try:
            latest_user_answer = UserAnswer.objects.filter(user=self.user_check_skills.user, question=self.question).latest('id')
            self.status = 'Right' if latest_user_answer.correct == 1.0 else 'Wrong'
            self.user_answer = latest_user_answer
            self.save()
        except UserAnswer.DoesNotExist:
            self.status = 'Not Answered'
            self.save()
    
    # Проверка всех ответов и обновление статуса
    def check_all_answers(self):
        for question in self.user_check_skills.usercheckskillsquestion_set.all():
            question.update_status()