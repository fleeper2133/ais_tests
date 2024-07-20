import pytest
# from django.contrib.auth.models import User
from users.models import CustomUser
from course.models import Course, Testing, Ticket, Question, QuestionList, LearningMaterial, Varient
from usercourse.models import UserCourse, TaskQuestion, UserQuestion, UserTicket, UserAnswer, QuestionTicket, UserCheckSkills, UserCheckSkillsQuestion, UserAnswerItem
from datetime import timedelta
from django.utils import timezone
import random

@pytest.fixture
def create_test_data():
    user = CustomUser.objects.create_user(password='olpassword123', email='oleg_test_user@example.com')
    
    course = Course.objects.create(
        name='Test Course', 
        description='A test course', 
        version='1.0', 
        available_until=timezone.now() + timedelta(days=365), 
        question_count=10, 
        image_link='courses/default.png'
    )
    
    testing = Testing.objects.create(course=course, description='Sample testing for tickets', price=1000)
    
    ticket1 = Ticket.objects.create(name='Ticket 1', difficulty='medium', question_count=10, testing=testing)
    ticket2 = Ticket.objects.create(name='Ticket 2', difficulty='medium', question_count=10, testing=testing)
    
    learning_material = LearningMaterial.objects.create(
        title='Sample Material',
        author='Author Name',
        year_of_issue=2021,
        document_link='https://example.com/material/1'
    )
    
    difficulties = ['easy', 'medium', 'hard', 'extrem']
    questions = []
    
    for _ in range(40):
        for i, difficulty in enumerate(difficulties):
            for j in range(3 if difficulty != 'extrem' else 1):
                question = Question.objects.create(
                    name=f'Question {i*3 + j + 1}',
                    question_text='Sample question text?',
                    topic='Sample Topic',
                    difficulty=difficulty,
                    course=course,
                    explanation_material=learning_material,
                    right_answer_count=1,
                    answer_count=4
                )
                for k in range(4):
                    Varient.objects.create(
                        question=question,
                        answer_number=k+1,
                        answer_text=f'Answer {k+1}',
                        correct=(k == 0)  # First answer is correct for simplicity
                    )
                questions.append(question)
    
    QuestionList.objects.create(ticket=ticket1, number_in_ticket=1, question=questions[0])
    QuestionList.objects.create(ticket=ticket1, number_in_ticket=2, question=questions[1])
    QuestionList.objects.create(ticket=ticket1, number_in_ticket=3, question=questions[2])
    QuestionList.objects.create(ticket=ticket2, number_in_ticket=1, question=questions[3])
    QuestionList.objects.create(ticket=ticket2, number_in_ticket=2, question=questions[4])
    QuestionList.objects.create(ticket=ticket2, number_in_ticket=3, question=questions[5])
    
    user_course = UserCourse.objects.create(user=user, course=course, start_date=timezone.now(), progress=50)
    
    user_ticket1 = UserTicket.objects.create(user=user, ticket=ticket1, status='Not started', attempt_count=1, right_answers=0, time_ticket=timedelta(minutes=30), user_course=user_course)
    user_ticket2 = UserTicket.objects.create(user=user, ticket=ticket2, status='Not started', attempt_count=1, right_answers=0, time_ticket=timedelta(minutes=30), user_course=user_course)
    user_ticket3 = UserTicket.objects.create(user=user, ticket=ticket2, status='Not started', attempt_count=1, right_answers=0, time_ticket=timedelta(minutes=30), user_course=user_course)
    
    user_questions = []
    for question in questions:
        user_question = UserQuestion.objects.create(
            user=user,
            question=question,
            memorization='New',
            selected=True,
            correct_count=1,
            incorrect_count=2,
            average_answer_time=timedelta(seconds=30)
        )
        user_questions.append(user_question)
    
    user_answers = []
    for question in questions:
        for i in range(1, 5):
            varient = Varient.objects.get(question=question, answer_number=i)
            user_answer = UserAnswer.objects.create(
                user=user,
                question=question,
                correct=varient.correct,
                answer_time=timedelta(seconds=30)
            )
            UserAnswerItem.objects.create(
                user_answer=user_answer,
                answer_varient=varient,
                order_answer=i
            )
            user_answers.append(user_answer)
    
    question_tickets = []
    for i, question in enumerate(questions[:3]):
        question_ticket = QuestionTicket.objects.create(
            user_ticket=user_ticket1,
            number_in_ticket=i + 1,
            user_answer=user_answers[i],
            status='Right'
        )
        question_tickets.append(question_ticket)
    
    user_check_skills = UserCheckSkills.objects.create(user=user, question_count=5, status='In Progress')
    user_check_skills_questions = []
    for i, question in enumerate(questions[:5]):
        user_check_skills_question = UserCheckSkillsQuestion.objects.create(
            user_check_skills=user_check_skills,
            question=question,
            number_in_check=i + 1,
            user_answer=user_answers[i],
            status='Right'
        )
        user_check_skills_questions.append(user_check_skills_question)
    
    return {
        'user': user,
        'course': course,
        'testing': testing,
        'tickets': [ticket1, ticket2],
        'questions': questions,
        'learning_material': learning_material,
        'user_course': user_course,
        'user_tickets': [user_ticket1, user_ticket2, user_ticket3],
        'user_questions': user_questions,
        'user_answers': user_answers,
        'question_tickets': question_tickets,
        'user_check_skills': user_check_skills,
        'user_check_skills_questions': user_check_skills_questions,
    }

user_count = 10
course_count = 1
#дописать все переменные, использованные, как константы

@pytest.fixture
def create_users():
    users = []
    for i in range(user_count):
        user = CustomUser.objects.create_user(password='olpassword123', email=f'oleg_user_{i}@example.com')
        users.append(user)
    return users

@pytest.fixture
def create_courses():
    courses = []
    for i in range(course_count):
        course = Course.objects.create(
            name=f'Course {i}',
            description='A test course',
            version=f'1.{i}',
            available_until=timezone.now() + timedelta(days=365),
            question_count=random.randint(50, 100),
            image_link='courses/default.png'
        )
        courses.append(course)
    return courses

@pytest.fixture
def create_testings(create_courses):
    testings = []
    for course in create_courses:
        testing = Testing.objects.create(
            course=course,
            description='A testing description',
            price=random.randint(1000, 5000)
        )
        testings.append(testing)
    return testings

@pytest.fixture
def create_tickets(create_testings):
    tickets = []
    for testing in create_testings:
        for i in range(5):
            ticket = Ticket.objects.create(
                name=f'Ticket {i}',
                difficulty=random.choice(['easy', 'medium', 'hard', 'extrem']),
                question_count=random.randint(5,10),
                testing=testing
            )
            tickets.append(ticket)
    return tickets

@pytest.fixture
def create_learning_materials():
    materials = []
    for i in range(100): 
        material = LearningMaterial.objects.create(
            title=f'Title {i}',
            author=f'Author {i}',
            year_of_issue=random.randint(2000, 2023),
            document_link=f'https://example.com/material/{i}'
        )
        materials.append(material)
    return materials

@pytest.fixture
def create_questions(create_courses, create_learning_materials):
    questions = []
    for course in create_courses:
        for i in range(course.question_count):
            explanation_material = random.choice(create_learning_materials)
            question = Question.objects.create(
                name=f'Question {i} for {course.name}',
                question_text='What is the answer?',
                topic='Sample Topic',
                difficulty=random.choice(['easy', 'medium', 'hard', 'extrem']),
                course=course,
                explanation_material=explanation_material
            )
            for j in range(4):
                Varient.objects.create(
                    question=question,
                    answer_number=j + 1,
                    answer_text=f'Answer {j + 1}',
                    correct=(j == 0)  # Первый вариант правильный для простоты
                )
            question.calculate_right_answer_count()
            question.calculate_answer_count()
            questions.append(question)
    return questions

@pytest.fixture
def create_question_lists(create_tickets, create_questions):
    question_lists = []
    for ticket in create_tickets:
        ticket_questions = random.sample(create_questions, k=ticket.question_count)
        for idx, question in enumerate(ticket_questions):
            question_list = QuestionList.objects.create(
                ticket=ticket,
                number_in_ticket=idx + 1,
                question=question
            )
            question_lists.append(question_list)
    return question_lists

@pytest.fixture
def create_user_courses(create_users, create_courses):
    user_courses = []
    for user in create_users:
        for course in create_courses:
            user_course = UserCourse.objects.create(
                user=user,
                course=course,
                start_date=timezone.now(),
                progress=0
            )
            user_courses.append(user_course)
    return user_courses

@pytest.fixture
def create_task_questions(create_users, create_questions):
    task_questions = []
    for user in create_users:
        for question in create_questions:
            task_question = TaskQuestion.objects.create(
                user=user,
                question=question,
                message='I have a question about this task.'
            )
            task_questions.append(task_question)
    return task_questions

@pytest.fixture
def create_user_questions(create_users, create_questions):
    user_questions = []
    for user in create_users:
        for question in create_questions:
            user_question = UserQuestion.objects.create(
                user=user,
                question=question,
                memorization='New',
                selected=random.choice([True, False]),
                correct_count=0,
                incorrect_count=0,
                average_answer_time=timedelta(seconds=0)
            )
            user_questions.append(user_question)
    return user_questions

@pytest.fixture
def create_user_tickets(create_users, create_tickets, create_user_courses):
    user_tickets = []
    for user in create_users:
        for ticket in create_tickets:
            user_course = UserCourse.objects.get(course=ticket.testing.course, user=user)
            user_ticket = UserTicket.objects.create(
                user=user,
                ticket=ticket,
                status='Not started',
                attempt_count=0,
                right_answers=0,
                time_ticket=timedelta(minutes=0),
                user_course=user_course
            )
            user_tickets.append(user_ticket)
    return user_tickets

@pytest.fixture
def create_user_answers(create_users, create_questions):
    user_answers = []
    for user in create_users:
        for question in create_questions:
            user_answer = UserAnswer.objects.create(
                user=user,
                question=question,
                answer_time=timedelta(seconds=random.randint(100, 200)),
                correct=False,
            )
            for i in range(1, 5):
                varient = Varient.objects.get(question=question, answer_number=i)
                UserAnswerItem.objects.create(
                    user_answer=user_answer,
                    answer_varient=varient,
                    order_answer=i
                )
            user_answer.check_correctness()
            user_answers.append(user_answer)
    return user_answers

@pytest.fixture
def create_question_tickets(create_user_tickets, create_question_lists):
    question_tickets = []
    for user_ticket in create_user_tickets:
        question_lists = QuestionList.objects.filter(ticket=user_ticket.ticket)
        for question_list in question_lists:
            user_answer = UserAnswer.objects.create(
                user=user_ticket.user,
                question=question_list.question,
                correct=random.choice([True, False]),
                answer_time=timedelta(seconds=random.randint(100, 200))
            )
            question_ticket = QuestionTicket.objects.create(
                user_ticket=user_ticket,
                number_in_ticket=question_list.number_in_ticket,
                user_answer=user_answer,
                status=random.choice(['Not Answered', 'Right', 'Wrong'])
            )
            question_tickets.append(question_ticket)
    return question_tickets

@pytest.fixture
def create_user_check_skills(create_users):
    user_check_skills = []
    for user in create_users:
        check_skills = UserCheckSkills.objects.create(
            user=user,
            question_count=random.randint(10, 50),
            status=random.choice(['In Progress', 'Completed'])
        )
        user_check_skills.append(check_skills)
    return user_check_skills

@pytest.fixture
def create_user_check_skills_questions(create_user_check_skills, create_questions, create_user_answers):
    user_check_skills_questions = []
    for check_skills in create_user_check_skills:
        for i in range(check_skills.question_count):
            user_answer = random.choice(create_user_answers)
            check_skills_question = UserCheckSkillsQuestion.objects.create(
                user_check_skills=check_skills,
                question=random.choice(create_questions),
                number_in_check=i + 1,
                user_answer=user_answer,
                status=random.choice(['Not Answered', 'Right', 'Wrong'])
            )
            user_check_skills_questions.append(check_skills_question)
    return user_check_skills_questions

@pytest.fixture
def setup_data(
    create_users,
    create_courses,
    create_testings,
    create_tickets,
    create_learning_materials,
    create_questions,
    create_question_lists,
    create_user_courses,
    create_task_questions,
    create_user_questions,
    create_user_tickets,
    create_user_answers,
    create_question_tickets,
    create_user_check_skills,
    create_user_check_skills_questions,):

    # для UserTicket
    for user_ticket in create_user_tickets:
        user_ticket.update_status()
    
    # для UserCourse
    for user_course in create_user_courses:
        user_course.calculate_progress()
    
    # для UserQuestion
    for user_question in create_user_questions:
        user_question.update_memorization()
    
    # для QuestionTicket
    for question_ticket in create_question_tickets:
        question_ticket.update_status()
    
    # для UserCheckSkills
    for user_check_skills in create_user_check_skills:
        user_check_skills.update_status()
    
    # для UserCheckSkillsQuestion
    for user_check_skills_question in create_user_check_skills_questions:
        user_check_skills_question.update_status()

    #  для UserAnswer
    for user_answer in create_user_answers:
        user_answer.check_correctness()

    return {
        'users': create_users,
        'courses': create_courses,
        'testings': create_testings,
        'tickets': create_tickets,
        'learning_materials': create_learning_materials,
        'questions': create_questions,
        'question_lists': create_question_lists,
        'user_courses': create_user_courses,
        'task_questions': create_task_questions,
        'user_questions': create_user_questions,
        'user_tickets': create_user_tickets,
        'user_answers': create_user_answers,
        'question_tickets': create_question_tickets,
        'user_check_skills': create_user_check_skills,
        'user_check_skills_questions': create_user_check_skills_questions,
    }