from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from course.models import Course, Testing, Ticket, Question, QuestionList, LearningMaterial, Varient
from usercourse.models import UserCourse, TaskQuestion, UserQuestion, UserTicket, UserAnswer, QuestionTicket, UserCheckSkills, UserCheckSkillsQuestion, UserAnswerItem
from datetime import timedelta
from django.utils import timezone


class UserTicketTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(password='olpassword123', email='oleg_test_user@example.com')

        self.course = Course.objects.create(
            name='Test Course', 
            description='A test course', 
            version='1.0', 
            available_until=timezone.now() + timedelta(days=365), 
            question_count=100, 
            image_link='courses/default.png'
        )

        self.testing = Testing.objects.create(course=self.course, description='Sample testing for tickets', price=1000)
        
        self.ticket1 = Ticket.objects.create(name='Ticket 1', difficulty='medium', question_count=50, testing=self.testing)
        self.ticket2 = Ticket.objects.create(name='Ticket 2', difficulty='medium', question_count=50, testing=self.testing)
        
        self.learning_material = LearningMaterial.objects.create(
            title='Sample Material',
            author='Author Name',
            year_of_issue=2021,
            document_link='https://example.com/material/1'
        )

        difficulties = ['easy', 'medium', 'hard', 'extrem']
        self.questions = []

        for i in range(100):
            difficulty = difficulties[i % len(difficulties)]
            question = Question.objects.create(
                name=f'Question {i + 1}',
                question_text='Sample question text?',
                topic='Sample Topic',
                difficulty=difficulty,
                course=self.course,
                explanation_material=self.learning_material,
                right_answer_count=1,
                answer_count=4
            )
            for k in range(4):
                Varient.objects.create(
                    question=question,
                    answer_number=k+1,
                    answer_text=f'Answer {k+1}',
                    correct=(k == 0)  # Первый ответ правильный для упрощения
                )
            self.questions.append(question)

        # Привязка первых 50 вопросов к ticket1 и следующих 50 к ticket2
        for i in range(50):
            QuestionList.objects.create(ticket=self.ticket1, number_in_ticket=i + 1, question=self.questions[i])
        for i in range(50, 100):
            QuestionList.objects.create(ticket=self.ticket2, number_in_ticket=i - 49, question=self.questions[i])
        
        self.user_course = UserCourse.objects.create(user=self.user, course=self.course, start_date=timezone.now(), progress=50)
        
        self.user_ticket1 = UserTicket.objects.create(user=self.user, ticket=self.ticket1, status='Not started', attempt_count=1, right_answers=0, time_ticket=timedelta(minutes=30), user_course=self.user_course)
        self.user_ticket2 = UserTicket.objects.create(user=self.user, ticket=self.ticket2, status='Not started', attempt_count=1, right_answers=0, time_ticket=timedelta(minutes=30), user_course=self.user_course)
        self.user_ticket3 = UserTicket.objects.create(user=self.user, ticket=self.ticket2, status='Not started', attempt_count=1, right_answers=0, time_ticket=timedelta(minutes=30), user_course=self.user_course)
        
        self.user_questions = []
        for question in self.questions:
            user_question = UserQuestion.objects.create(
                user=self.user,
                question=question,
                memorization='New',
                selected=True,
                correct_count=1,
                incorrect_count=2,
                average_answer_time=timedelta(seconds=30)
            )
            self.user_questions.append(user_question)
        
        self.user_answers = []
        for question in self.questions:
            for i in range(1, 5):
                varient = Varient.objects.get(question=question, answer_number=i)
                user_answer = UserAnswer.objects.create(
                    user=self.user,
                    question=question,
                    correct=varient.correct,
                    answer_time=timedelta(seconds=30)
                )
                UserAnswerItem.objects.create(
                    user_answer=user_answer,
                    answer_varient=varient,
                    order_answer=i
                )
                self.user_answers.append(user_answer)
        
        self.question_tickets = []
        for i, question in enumerate(self.questions[:50]):
            question_ticket = QuestionTicket.objects.create(
                user_ticket=self.user_ticket1,
                number_in_ticket=i + 1,
                user_answer=self.user_answers[i],
                status='Right'
            )
            self.question_tickets.append(question_ticket)
        
        self.user_check_skills = UserCheckSkills.objects.create(user=self.user, question_count=50, status='In Progress')
        self.user_check_skills_questions = []
        for i, question in enumerate(self.questions[:50]):
            user_check_skills_question = UserCheckSkillsQuestion.objects.create(
                user_check_skills=self.user_check_skills,
                question=question,
                number_in_check=i + 1,
                user_answer=self.user_answers[i],
                status='Right'
            )
            self.user_check_skills_questions.append(user_check_skills_question)

    def test_generate_ticket(self):
        url = reverse('userticket-generate-random-ticket')
        data = {'course_id': self.course.id}

        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        self.assertIn('detail', response.data)

    # def test_smart_generate_check(self):

    #     url = reverse('usercheckskills-smart-generate-check', args=[self.user_check_skills.id])
    #     data = {'course_id': self.course.id}

    #     self.client.force_authenticate(user=self.user)

    #     response = self.client.post(url, data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('questions', response.data)
    #     self.assertIsInstance(response.data['questions'], list)
    #     self.assertTrue(len(response.data['questions']) > 0)  # Check that questions are not empty



    # def test_check_answers(self):
    #     # Создаем UserCheckSkills и UserCheckSkillsQuestion
    #     check_skills = UserCheckSkills.objects.create(user=self.user, question_count=20)
    #     check_skills_questions = [
    #         UserCheckSkillsQuestion.objects.create(user_check_skills=check_skills, question=q) for q in self.questions[:20]
    #     ]

    #     # Отправляем ответы на вопросы
    #     url = reverse('usercheckskills-check-answer', args=[check_skills.id])
    #     for question in check_skills_questions:
    #         response = self.client.post(url, {'question_id': question.question.id, 'answers': [1]}, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertIn('is_correct', response.data)
