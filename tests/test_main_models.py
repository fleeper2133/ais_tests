# Параметризация - проверка нескольких тестовых случаев для 1 сценария.
# То есть функция одна, а вариантов значений - много.

# Фикстуры - создают среду для тестрования.
# Например для авторизации пользователя. Очистка + наполнение кэша. 
# Часто используемые данные для тестов. Для упрощения объявления переменных

#conftest.py - файл для структур, необходимых для всего проекта

#использовать параметризованный тест с фикстурой на готовые ответы пользователя
#  по вопросу(создать отдельно). Тестить уровень запоминания. Возможно строить прогрессию скорости ответа?

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from django.utils import timezone
from datetime import timedelta
from course.models import QuestionList
from usercourse.models import UserCourse, TaskQuestion, UserQuestion, UserTicket, UserAnswer, QuestionTicket, UserCheckSkills, UserCheckSkillsQuestion

# @pytest.mark.django_db
# def test_profile_fields(setup_data):
#     create_users = setup_data['users']
#     for user in create_users:
#         profile = Profile.objects.get(user=user)
#         assert profile.phone.startswith('+')
#         assert profile.type in ['User', 'Teacher', 'Admin']

@pytest.mark.django_db
def test_user_course_fields(setup_data):
    create_user_courses = setup_data['user_courses']
    for user_course in create_user_courses:
        assert user_course.start_date <= timezone.now()
        assert 0 <= user_course.progress <= 100

@pytest.mark.django_db
def test_task_question_fields(setup_data):
    create_task_questions = setup_data['task_questions']
    for task_question in create_task_questions:
        assert task_question.message == 'I have a question about this task.'

@pytest.mark.django_db
def test_user_question_fields(setup_data):
    create_user_questions = setup_data['user_questions']
    for user_question in create_user_questions:
        assert user_question.memorization in ['New', 'Bad', 'Satisfactorily', 'Good', 'Excellent']
        assert user_question.selected in [True, False]
        # Фильтрация ответов по пользователю и вопросу
        answers_count = UserAnswer.objects.filter(user=user_question.user, question=user_question.question).count()
        assert 0 <= user_question.correct_count <= answers_count
        assert 0 <= user_question.incorrect_count <= answers_count
        #хардкод!

@pytest.mark.django_db
def test_user_ticket_fields(setup_data):
    create_user_tickets = setup_data['user_tickets']
    for user_ticket in create_user_tickets:
        assert user_ticket.status in ['Not started', 'Done', 'Failed']
        if user_ticket.status == 'Not started':
            assert 0 == user_ticket.attempt_count 
        else:
            assert 0 <= user_ticket.attempt_count
        assert 0 <= user_ticket.right_answers <= user_ticket.ticket.question_count
        #считаем, что тест может максимально идти 2 часа
        assert timedelta(seconds=0) <= user_ticket.time_ticket <= timedelta(minutes=120)

@pytest.mark.django_db
def test_user_answer_fields(setup_data):
    create_user_answers = setup_data['user_answers']
    for user_answer in create_user_answers:

        assert 0 <= user_answer.correct <= 1
        #Если время меньше, то пользователь не читал вопрос!
        assert timedelta(seconds=5) <= user_answer.answer_time

@pytest.mark.django_db
def test_question_ticket_fields(setup_data):
    create_question_tickets = setup_data['question_tickets']
    for question_ticket in create_question_tickets:
        assert question_ticket.status in ['Not Answered', 'Right', 'Wrong']
        assert 1 <= question_ticket.number_in_ticket <= question_ticket.user_ticket.ticket.question_count # не превышает число вопросов в билете

@pytest.mark.django_db
def test_user_check_skills_fields(setup_data):
    create_user_check_skills = setup_data['user_check_skills']
    for check_skills in create_user_check_skills:
        assert 0 < check_skills.question_count 
        assert check_skills.status in ['In Progress', 'Completed']

@pytest.mark.django_db
def test_user_check_skills_question_fields(setup_data):
    create_user_check_skills_questions = setup_data['user_check_skills_questions']
    for check_skills_question in create_user_check_skills_questions:
        assert check_skills_question.status in ['Not Answered', 'Right', 'Wrong']
        assert 1 <= check_skills_question.number_in_check <= check_skills_question.user_check_skills.question_count