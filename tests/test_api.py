import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from course.models import Course, Ticket, Question
from usercourse.models import UserCourse, UserTicket, UserCheckSkills
from users.models import CustomUser
from datetime import timedelta
from django.utils import timezone
import random

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(create_test_data, api_client):
    user = create_test_data['user']
    api_client.force_authenticate(user=user)
    return api_client

# ----------------------------------------------------------------------------------------

@pytest.mark.django_db
class TestCourseViewSet:
    # Пользователь откладывает курс
    def test_mark_as_delayed_success(self, authenticated_client, create_test_data):
        course = create_test_data['course']
        url = reverse('course-mark-as-delayed', args=[course.id])

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_201_CREATED
        user_course = UserCourse.objects.get(user=create_test_data['user'], course=course)
        assert user_course.status == 'Delayed'
        data = response.json()
        assert data['status'] == 'Курс отмечен как отложенный'
        assert data['user_course']['course'] == course.id
        assert data['user_course']['user'] == create_test_data['user'].id

    def test_mark_as_delayed_already_enrolled(self, authenticated_client, create_test_data):
        user_course = create_test_data['user_course']
        course = user_course.course
        url = reverse('course-mark-as-delayed', args=[course.id])
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_201_CREATED
        user_course.refresh_from_db()
        assert user_course.status == 'Delayed'
        data = response.json()
        assert data['status'] == 'Курс отмечен как отложенный'
        assert data['user_course']['course'] == course.id
        assert data['user_course']['user'] == create_test_data['user'].id

    def test_mark_as_delayed_unauthenticated(self, api_client, create_test_data):
        course = create_test_data['course']
        url = reverse('course-mark-as-delayed', args=[course.id])
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] == 'Пользователь не найден.'

    def test_mark_as_delayed_invalid_course(self, authenticated_client):
        invalid_course_id = -1
        url = reverse('course-mark-as-delayed', args=[invalid_course_id])
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    # Пользователь начинает курс
    def test_start_course_success(self, authenticated_client, create_test_data):
        course = Course.objects.create(
            name='Test Course', 
            description='A test course', 
            version='1.0', 
            available_until=timezone.now() + timedelta(days=365), 
            question_count=100, 
            image_link='courses/default.png'
        )
        url = reverse('course-start-course', args=[course.id])
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_201_CREATED
        assert UserCourse.objects.filter(user=create_test_data['user'], course=course).exists()
        data = response.json()
        assert data['course'] == course.id
        assert data['user'] == create_test_data['user'].id

    def test_start_course_already_enrolled(self, authenticated_client, create_test_data):
        user_course = create_test_data['user_course']
        course = user_course.course
        url = reverse('course-start-course', args=[course.id])
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['detail'] == 'Пользователь уже проходит этот курс.'

    def test_start_course_unauthenticated(self, api_client, create_test_data):
        course = create_test_data['course']
        url = reverse('course-start-course', args=[course.id])
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] == 'Пользователь не найден.'

    def test_start_course_invalid_course(self, authenticated_client):
        invalid_course_id = 9999
        url = reverse('course-start-course', args=[invalid_course_id])
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

# ----------------------------------------------------------------------------------------
# Детальная информация о билете пользователя

@pytest.mark.django_db
class TestTicketViewSet:

    def test_detail_user_ticket_success(self, authenticated_client, create_test_data):
        ticket = Ticket.objects.create(name='Ticket 1', difficulty='medium', question_count=10, testing=create_test_data['testing'])
        url = reverse('ticket-detail-user-ticket', args=[ticket.id])
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        user_ticket = UserTicket.objects.get(ticket=ticket, user=create_test_data['user'])
        data = response.json()
        assert data['ticket'] == ticket.id
        assert data['user'] == create_test_data['user'].id
        assert data['attempt_count'] == 1 

    def test_detail_user_ticket_already_exists(self, authenticated_client, create_test_data):
        user_ticket = create_test_data['user_tickets'][0]
        ticket = user_ticket.ticket
        url = reverse('ticket-detail-user-ticket', args=[ticket.id])
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_201_CREATED
        user_ticket.refresh_from_db()
        data = response.json()
        assert data['ticket'] == ticket.id
        assert data['user'] == create_test_data['user'].id
        assert data['attempt_count'] == 2

    def test_detail_user_ticket_unauthenticated(self, api_client, create_test_data):
        ticket = create_test_data['tickets'][0]
        url = reverse('ticket-detail-user-ticket', args=[ticket.id])
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] == 'Пользователь не найден.'

    def test_detail_user_ticket_no_user_course(self, authenticated_client, create_test_data):
        user = create_test_data['user']
        course = create_test_data['course']
        UserCourse.objects.filter(user=user, course=course).delete()
        ticket = create_test_data['tickets'][0]
        url = reverse('ticket-detail-user-ticket', args=[ticket.id])
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['detail'] == 'Пользовательский курс не найден.'

    def test_detail_user_ticket_invalid_ticket(self, authenticated_client):
        invalid_ticket_id = -1
        url = reverse('ticket-detail-user-ticket', args=[invalid_ticket_id])
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

# ----------------------------------------------------------------------------------------
# Детальная информация по вопросу

@pytest.mark.django_db
class TestQuestionViewSet:

    def test_get_question_detail_success(self, authenticated_client):
        question = Question.objects.get(id=1)
        url = reverse('question-detail', args=[question.id])
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        print(data)
        assert data['name'] == question.name
        assert data['question_text'] == question.question_text
        assert "explanations" in data
        assert "normative_documents" in data
        assert "varients" in data

    def test_get_question_detail_unauthenticated(self, api_client, create_test_data):
        question = create_test_data['questions'][0]
        url = reverse('question-detail', args=[question.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_question_detail_invalid_question(self, authenticated_client):
        invalid_question_id = -1
        url = reverse('question-detail', args=[invalid_question_id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_question_detail_with_no_varients(self, authenticated_client, create_test_data):
        question = create_test_data['questions'][0]
        question.varient_set.all().delete()
        url = reverse('question-detail', args=[question.id])
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'varients' in data
        assert len(data['varients']) == 0

    def test_get_question_detail_with_no_normative_document(self, authenticated_client, create_test_data):
        question = create_test_data['questions'][0]
        question.ndocument = None
        question.save()
        url = reverse('question-detail', args=[question.id])
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'normative_documents' in data
        assert data['normative_documents'] is None

# ----------------------------------------------------------------------------------------

@pytest.fixture
def create_test_data_course_history(create_test_data):
    user = CustomUser.objects.create_user(password='test_password123', email='test_user@example.com')
    course = create_test_data['course']
    user_course = UserCourse.objects.create(user=user, course=course, start_date=timezone.now(), progress=0, status='In Progress')

    UserCheckSkills.objects.create(user=user, user_course=user_course, status='Completed', difficulty='easy', question_count=10)
    UserTicket.objects.create(user=user, ticket=create_test_data['tickets'][0], user_course=user_course, status='Completed', attempt_count=1, right_answers=5, time_ticket=timedelta(minutes=30))

    return {
        'user': user,
        'user_course': user_course,
        'check_skills': UserCheckSkills.objects.all(),
        'tickets': UserTicket.objects.all(),
    }

@pytest.mark.django_db
class TestUserCourseViewSet:

    @pytest.mark.parametrize('is_authenticated, expected_status', [
        (True, status.HTTP_200_OK),
        (False, status.HTTP_401_UNAUTHORIZED),
    ])
    def test_course_history(self, create_test_data_course_history, is_authenticated, expected_status):
        user_course = create_test_data_course_history['user_course']
        user = create_test_data_course_history['user']

        client = APIClient()
        if is_authenticated:
            client.force_authenticate(user=user)
        url = reverse('usercourse-course-history', args=[user_course.id])
        
        response = client.get(url)
        
        assert response.status_code == expected_status
        if is_authenticated:
            data = response.json()
            assert len(data) == 2  # Проверка на количество событий
            assert data[0]['type'] == 'check_skill'
            assert data[1]['type'] == 'ticket'

    def test_course_history_content(self, create_test_data_course_history):
        user_course = create_test_data_course_history['user_course']
        user = create_test_data_course_history['user']

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('usercourse-course-history', args=[user_course.id])
        
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert len(data) == 2
        
        check_skill_event = data[0]
        assert check_skill_event['type'] == 'check_skill'
        assert check_skill_event['status'] == 'Completed'
        assert check_skill_event['difficulty'] == 'easy'
        assert check_skill_event['question_count'] == 10

        ticket_event = data[1]
        assert ticket_event['type'] == 'ticket'
        assert ticket_event['status'] == 'Completed'
        assert ticket_event['attempt_count'] == 1
        assert ticket_event['right_answers'] == 5

# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------

# @pytest.mark.django_db
# def test_generate_random_ticket(create_test_data):
#     data = create_test_data
#     user = data['user']
#     user_course = data['user_course']
#     client = APIClient()
#     client.force_authenticate(user=user)
#     url = reverse('userticket-generate-random-ticket')
#     response = client.post(url, {'user_course_id': user_course.id}, format='json')

#     assert response.status_code == status.HTTP_201_CREATED
#     assert 'id' in response.data 

# @pytest.mark.django_db
# def test_smart_generate_check(create_test_data):
#     data = create_test_data
#     user = data['user']
#     user_course = data['user_course']
#     client = APIClient()
#     client.force_authenticate(user=user)
#     url = reverse('usercheckskills-smart-generate-check', kwargs={'pk': user.id})
#     response = client.post(url, {'user_course_id': user_course.id}, format='json')

#     assert response.status_code == status.HTTP_201_CREATED
#     assert 'check_skills' in response.data

# @pytest.mark.django_db
# def test_generate_ticket_unauthenticated(create_test_data):
#     data = create_test_data
#     user_course = data['user_course']
#     client = APIClient()
#     url = reverse('userticket-generate-random-ticket')  
#     response = client.post(url, {'course_id': user_course.id}, format='json')

#     assert response.status_code == status.HTTP_401_UNAUTHORIZED

# @pytest.mark.django_db
# def test_smart_generate_check_unauthenticated(create_test_data):
#     data = create_test_data
#     user = data['user']
#     user_course = data['user_course']
#     client = APIClient()
#     url = reverse('usercheckskills-smart-generate-check', kwargs={'pk': user.id})
#     response = client.post(url, {'user_course_id': user_course.id}, format='json')

#     assert response.status_code == status.HTTP_401_UNAUTHORIZED