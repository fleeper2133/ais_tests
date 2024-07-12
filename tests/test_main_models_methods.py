import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from django.utils import timezone
from datetime import timedelta
from course.models import QuestionList, Question, Course, Ticket, Varient
from usercourse.models import UserCourse, TaskQuestion, UserQuestion, UserTicket, UserAnswer, QuestionTicket, UserCheckSkills, UserCheckSkillsQuestion, UserAnswerItem
from django.db import IntegrityError
from collections import Counter

# Функциональное тестирование моделей


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
def test_question_calculate_right_answer_count(create_test_data):
    questions = create_test_data['questions']

    for question in questions:
        question.calculate_right_answer_count()

        # Получаем ожидаемое значение
        expected_right_answer_count = Varient.objects.filter(question=question, correct=True).count()

        # Перезагружаем объект из базы данных для актуализации данных
        question.refresh_from_db()

        # Проверяем, что вычисленное значение совпадает с ожидаемым
        assert question.right_answer_count == expected_right_answer_count


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
def test_question_calculate_answer_count(create_test_data):
    questions = create_test_data['questions']

    for question in questions:
        question.calculate_answer_count()

        # Получаем ожидаемое значение
        expected_answer_count = Varient.objects.filter(question=question).count()

        # Перезагружаем объект из базы данных для актуализации данных
        question.refresh_from_db()

        # Проверяем, что вычисленное значение совпадает с ожидаемым
        assert question.answer_count == expected_answer_count


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("marks, expected_course_mark", [
    ([5, 4, 3], 4),      
    ([5, 5, 5, 5], 5),  
    ([1, 2, 3, 4, 5], 3),
    ([], 0),              
])
def test_update_course_mark(setup_data, marks, expected_course_mark):
    user_course = setup_data['user_courses'][0]
    course = user_course.course
    
    # Установка оценок для всех пользовательских курсов
    for i, user_course in enumerate(setup_data['user_courses']):
        if i < len(marks):
            user_course.mark = marks[i]
            user_course.save()

    # Вызов функции для обновления оценки курса
    course.update_course_mark()
    
    # Проверка результата
    updated_course = Course.objects.get(id=course.id)
    assert updated_course.user_marks == expected_course_mark


 #-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("completed_tickets, expected_progress", [
    (0, 0),     
    (1, 50),   
    (2, 100), 
])
def test_calculate_progress(create_test_data, completed_tickets, expected_progress):
    setup_data = create_test_data
    for i in range(completed_tickets):
        setup_data['user_tickets'][i].status = 'Done'
        setup_data['user_tickets'][i].save()

    setup_data['user_course'].calculate_progress()
    updated_user_course = UserCourse.objects.get(id=setup_data['user_course'].id)
    assert updated_user_course.progress == expected_progress


 #-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
def test_user_course_progress(create_test_data):
    user_course = create_test_data['user_course']
    user_course.calculate_progress()
    assert 0 <= user_course.progress <= 100


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("correct_count, incorrect_count, expected_memorization", [
    (0, 0, 'New'),
    (1, 4, 'Bad'),
    (3, 4, 'Satisfactorily'),
    (5, 2, 'Good'),
    (7, 1, 'Excellent'),
    (10, 0, 'Excellent'),
    (0, 10, 'Bad'),      
    (2, 2, 'Good'),  
    (21, 25, 'Bad'), #3 mistakes in a row
    (100, 50, 'Good'),     
])
def test_user_question_memorization(create_test_data, correct_count, incorrect_count, expected_memorization):
    user_question = create_test_data['user_questions'][0]
    user_question.correct_count = correct_count
    user_question.incorrect_count = incorrect_count
    if correct_count == 21:
        user_question.force_downgrade_flag = True
    user_question.update_memorization()
    assert user_question.memorization == expected_memorization


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("answers_sequence, expected_consecutive_incorrect_count, expected_force_downgrade_flag", [
    ([True, True, True], 0, False),  
    ([True, False, False, False], 3, True), 
    ([False, False, True, False], 1, False),  
    ([False, True, False, True], 0, False), 
    ([True, False, False, False, False], 4, True),  
    ([False, False, False], 3, True), #Если правильных ответов не было вовсе
    ([False, False], 2, False), 
])
def test_update_consecutive_incorrect(create_test_data, answers_sequence, expected_consecutive_incorrect_count, expected_force_downgrade_flag):
    user_question_help = create_test_data['user_questions'][0]
    question = Question.objects.create(name='Question', question_text='Sample question text?',topic='Sample Topic',difficulty='Medium',course=user_question_help.question.course,explanation_material=user_question_help.question.explanation_material)
    user_question = UserQuestion.objects.create(user=user_question_help.user, question=question, memorization='New', selected=True, correct_count=0, incorrect_count=0, average_answer_time=timedelta(seconds=30))
    
    # Создаем объекты UserAnswer в соответствии с заданной последовательностью
    for correct in answers_sequence:
        UserAnswer.objects.create(user=user_question.user, question=user_question.question, correct=correct, answer_time=timedelta(seconds=30))

    user_question.update_consecutive_incorrect()
    assert user_question.consecutive_incorrect_count == expected_consecutive_incorrect_count
    assert user_question.force_downgrade_flag == expected_force_downgrade_flag


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("correct_count, incorrect_count, expected_correct, expected_incorrect", [
    (3, 2, 4, 5),
    (4, 1, 5, 4),
    (5, 5, 6, 8),
])
def test_user_question_counts_and_time(create_test_data, correct_count, incorrect_count, expected_correct, expected_incorrect):
    user_question = create_test_data['user_questions'][0]
    #хардкод с вариантами правильных ответов
    for i in range(correct_count):
        answ_i = UserAnswer.objects.create(user=user_question.user, question=user_question.question, user_answer='a', correct=True, answer_time=timedelta(seconds=30))
    for i in range(incorrect_count):
        answ_i = UserAnswer.objects.create(user=user_question.user, question=user_question.question, user_answer='b', correct=False, answer_time=timedelta(seconds=30))
    user_question.update_counts_and_average_time()
    assert user_question.correct_count == expected_correct
    assert user_question.incorrect_count == expected_incorrect


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
def test_user_ticket_attempt_count(create_test_data):
    user_ticket = create_test_data['user_tickets'][0]
    user_ticket.update_attempt_count()
    temp = user_ticket.attempt_count  # Считываем текущее значение attempt_count
    user_ticket1 = UserTicket.objects.create(user=user_ticket.user, ticket=user_ticket.ticket, status='Failed', attempt_count=0, right_answers=0, time_ticket=timedelta(minutes=30))
    user_ticket1.update_attempt_count()
    assert user_ticket1.attempt_count == (temp + 1)


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("right_answers, question_count, expected_status", [
    (1, 3, 'Failed'),
    (5, 10, 'Failed'),
    (2, 3, 'Done'),
    (3, 3, 'Done'),
    (6, 10, 'Done'),
])
def test_user_ticket_right_answers(create_test_data, right_answers, question_count, expected_status):
    user_ticket = create_test_data['user_tickets'][2]
    user_ticket.ticket.question_count = question_count
    user_ticket.right_answers = 0
    user_ticket.save()

    questions = create_test_data['questions'][:question_count]
    user = user_ticket.user

    user_answers = []
    for i in range(right_answers):
        user_answer = UserAnswer.objects.create(user=user, question=questions[i], user_answer='a', correct=True, answer_time=timedelta(seconds=30))
        user_answers.append(user_answer)

    for i in range(right_answers, question_count):
        user_answer = UserAnswer.objects.create(user=user, question=questions[i], user_answer='b', correct=False, answer_time=timedelta(seconds=30))
        user_answers.append(user_answer)

    question_tickets = []
    for i, question in enumerate(questions):
        question_ticket = QuestionTicket.objects.create(
            user_ticket=user_ticket, 
            number_in_ticket=i + 1, 
            user_answer=user_answers[i], 
            status='Right' if user_answers[i].correct else 'Wrong'
        )
        question_tickets.append(question_ticket)

    # Обновляем правильные ответы и статус билета
    user_ticket.update_right_answers()
    assert 0 <= user_ticket.right_answers <= user_ticket.ticket.question_count
    assert question_count == user_ticket.ticket.question_count
    assert right_answers == user_ticket.right_answers
    user_ticket.update_status()
    assert user_ticket.status == expected_status


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("ticket_index, expected_difficulty_counts", [
    (0, {'easy': 2, 'medium': 4, 'hard': 3, 'extrem': 1}),  
    (1, {'easy': 1, 'medium': 5, 'hard': 2, 'extrem': 2}),  
])
def test_ticket_determine_difficulty(create_test_data, ticket_index, expected_difficulty_counts):
    tickets = create_test_data['tickets']
    questions = create_test_data['questions']
    ticket = tickets[ticket_index]
    actual_difficulty_counts = Counter(question.difficulty for question in questions if question.course == ticket.testing.course)
    assert ticket.difficulty == max(expected_difficulty_counts, key=expected_difficulty_counts.get)


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
def test_user_ticket_status(create_test_data):
    for user_ticket in create_test_data['user_tickets']:
        question_count = QuestionList.objects.filter(ticket=user_ticket.ticket).count()
        if question_count == 0:
            assert user_ticket.status == 'Not started'
        else:
            user_ticket.update_status()
            if user_ticket.right_answers / question_count >= 0.6:
                assert user_ticket.status == 'Done'
            else:
                assert user_ticket.status == 'Failed'


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("user_answer_texts, correct_answers, expected_correctness", [
    (['a', 'b', 'c'], ['a', 'b', 'c'], 1.0),  # All correct
    (['a', 'b', 'c'], ['a', 'b', 'd'], 2/3),  # 2 correct out of 3
    (['a', 'a', 'a'], ['a', 'b', 'c'], 1/3),  # 1 correct out of 3
    (['a', 'b', 'c'], ['d', 'e', 'f'], 0.0),  # None correct
])
def test_user_answer_correctness(create_test_data, user_answer_texts, correct_answers, expected_correctness):
    question = create_test_data['questions'][0]
    answer_choices = {}
    for i, answer_text in enumerate(['a', 'b', 'c', 'd']):
        is_correct = answer_text in correct_answers
        answer_choices[answer_text] = UserAnswerItem.objects.create(
            user_answer=None,
            answer_varient=None,
            order_answer=i + 1,
            is_correct=is_correct
        )
    question.answer_choices = answer_choices
    question.save()

    user_answers = []
    for user_answer_text in user_answer_texts:
        user_answer = UserAnswer.objects.create(
            user=create_test_data['user'],
            question=question,
            user_answer=user_answer_text,
            answer_time=timedelta(seconds=30)
        )
        user_answers.append(user_answer)

    for user_answer in user_answers:
        user_answer.check_correctness()
    assert user_answers[0].correct == expected_correctness


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("user_answer_text, correct_answer, expected_status", [
    ('a', 'a', 'Right'),
    ('b', 'a', 'Wrong'),
    ('c', 'c', 'Right'),
    ('d', 'a', 'Wrong'),
])
def test_question_ticket_status(create_test_data, user_answer_text, correct_answer, expected_status):
    question = create_test_data['questions'][0]
    question.correct_answer = correct_answer
    question.save()
    for status in ['False', 'True']:
        user_answer = UserAnswer.objects.create(
            user=create_test_data['user'],
            question=question,
            user_answer=user_answer_text,
            correct=status,
            answer_time=timedelta(seconds=30)
        )
        question_ticket = QuestionTicket.objects.create(
            user_ticket=create_test_data['user_tickets'][0],
            number_in_ticket=1,
            user_answer=user_answer,
            status='Wrong',
        )
        user_answer.check_correctness()
        question_ticket.update_status()
        assert question_ticket.status == expected_status


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("number_in_ticket, question_count, expected_result", [
    (1, 3, True),
    (2, 3, True),
    (4, 3, False),  # Invalid case
    (None, 3, None),
])
def test_question_ticket_number_in_ticket(create_test_data, number_in_ticket, question_count, expected_result):
    ticket = create_test_data['tickets'][0]
    ticket.question_count = question_count
    ticket.save()

    if number_in_ticket is None:
        with pytest.raises(IntegrityError):
            QuestionTicket.objects.create(
                user_ticket=create_test_data['user_tickets'][0],
                number_in_ticket=number_in_ticket,
                user_answer=create_test_data['user_answers'][0],
                status='Right'
            )
    else:
        question_ticket = QuestionTicket.objects.create(
            user_ticket=create_test_data['user_tickets'][0],
            number_in_ticket=number_in_ticket,
            user_answer=create_test_data['user_answers'][0],
            status='Right'
        )
        result = question_ticket.get_number_in_ticket()
        if not expected_result:
            assert result is None or not (1 <= question_ticket.number_in_ticket <= ticket.question_count)
        else:
            assert (1 <= question_ticket.number_in_ticket <= ticket.question_count) == expected_result
            assert isinstance(result, int) == expected_result


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("user_answer_text, correct_answer, expected_status", [
    ('a', 'a', 'Right'),
    ('b', 'a', 'Wrong'),
    ('c', 'c', 'Right'),
    ('d', 'a', 'Wrong'),
])
def test_user_check_skills_question_status(create_test_data, user_answer_text, correct_answer, expected_status):
    question = create_test_data['questions'][0]
    question.correct_answer = correct_answer
    question.save()
    for status in ['False', 'True']:
        user_answer = UserAnswer.objects.create(
            user=create_test_data['user'],
            question=question,
            user_answer=user_answer_text,
            correct=status,
            answer_time=timedelta(seconds=30)
        )
        check_skills_question = UserCheckSkillsQuestion.objects.create(
            user_check_skills=create_test_data['user_check_skills'],
            question=question,
            number_in_check=1,
            user_answer=user_answer,
            status=status
        )
        user_answer.check_correctness()
        check_skills_question.update_status()
        assert check_skills_question.status == expected_status


#-------------------------------------------------------------------------------------------------


@pytest.mark.django_db
def test_user_course_progress(create_user_courses):
    for user_course in create_user_courses:
        user_course.calculate_progress()
        assert 0 <= user_course.progress <= 100

@pytest.mark.django_db
def test_user_question_memorization(create_user_questions):
    for user_question in create_user_questions:
        user_question.update_memorization()
        assert user_question.memorization in ['New', 'Bad', 'Satisfactorily', 'Good', 'Excellent']

@pytest.mark.django_db
def test_user_question_counts_and_time(create_user_questions):
    for user_question in create_user_questions:
        user_question.update_counts_and_average_time()
        assert 0 <= user_question.correct_count <= 10
        assert 0 <= user_question.incorrect_count <= 10
        #хардкод!

@pytest.mark.django_db
def test_user_ticket_attempt_count(create_user_tickets):
    for user_ticket in create_user_tickets:
        user_ticket.update_attempt_count()
        assert user_ticket.attempt_count > 0

@pytest.mark.django_db
def test_user_ticket_right_answers(create_user_tickets):
    for user_ticket in create_user_tickets:
        user_ticket.update_right_answers()
        assert 0 <= user_ticket.right_answers <= user_ticket.ticket.question_count

@pytest.mark.django_db
def test_user_ticket_status(create_user_tickets):
    for user_ticket in create_user_tickets:
        user_ticket.update_status()
        assert user_ticket.status in ['Done', 'Failed']

@pytest.mark.django_db
def test_user_ticket_status(create_user_tickets):
    for user_ticket in create_user_tickets:
        question_count = QuestionList.objects.filter(ticket=user_ticket.ticket).count()
        # Проверяем, есть ли вопросы в билете
        if question_count == 0:
            # Если нет вопросов, билет должен быть в статусе "Not started"
            assert user_ticket.status == 'Not started'
        else:
            user_ticket.update_status()
            if user_ticket.right_answers / question_count >= 0.6:
                assert user_ticket.status == 'Done'
            else:
                assert user_ticket.status == 'Failed'

@pytest.mark.django_db
def test_user_answer_correctness(create_user_answers):
    for user_answer in create_user_answers:
        user_answer.check_correctness()
        assert 0 <= user_answer.correct <= 1

@pytest.mark.django_db
def test_question_ticket_status(create_question_tickets):
    for question_ticket in create_question_tickets:
        question_ticket.update_status()
        assert question_ticket.status in ['Right', 'Wrong']

@pytest.mark.django_db
def test_question_ticket_number_in_ticket(create_question_tickets):
    for question_ticket in create_question_tickets:
        number_in_ticket = question_ticket.update_number_in_ticket()
        if number_in_ticket is None:
            assert number_in_ticket is None  # Проверка на отсутствие записи
        else:
            assert 1 <= question_ticket.number_in_ticket <= question_ticket.user_ticket.ticket.question_count
            assert isinstance(number_in_ticket, int)

@pytest.mark.django_db
def test_user_check_skills_question_status(create_user_check_skills_questions):
    for check_skills_question in create_user_check_skills_questions:
        check_skills_question.update_status()
        assert check_skills_question.status in ['Right', 'Wrong']
