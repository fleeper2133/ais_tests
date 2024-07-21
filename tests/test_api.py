import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status



@pytest.mark.django_db
def test_generate_random_ticket(create_test_data):
    data = create_test_data
    user = data['user']
    course = data['course']
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('userticket-generate-random-ticket')
    response = client.post(url, {'course_id': course.id}, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data 

@pytest.mark.django_db
def test_smart_generate_check(create_test_data):
    data = create_test_data
    user = data['user']
    course = data['course']
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('usercheckskills-smart-generate-check', kwargs={'pk': user.id})
    response = client.post(url, {'course_id': course.id}, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'check_skills' in response.data

@pytest.mark.django_db
def test_generate_ticket_unauthenticated(create_test_data):
    data = create_test_data
    course = data['course']
    client = APIClient()
    url = reverse('userticket-generate-random-ticket')  
    response = client.post(url, {'course_id': course.id}, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_smart_generate_check_unauthenticated(create_test_data):
    data = create_test_data
    user = data['user']
    course = data['course']
    client = APIClient()
    url = reverse('usercheckskills-smart-generate-check', kwargs={'pk': user.id})
    response = client.post(url, {'course_id': course.id}, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
