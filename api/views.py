# Course/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=False, methods=['get'], url_path='user-courses')
    def user_courses(self, request):
        user_courses = Course.objects.filter(user=request.user)
        user_courses_serializer = CourseSerializer(user_courses, many=True)

        other_courses = Course.objects.exclude(user=request.user)[:3]
        other_courses_serializer = CourseSerializer(other_courses, many=True)

        response_data = {
            'user_courses': user_courses_serializer.data,
            'other_courses': other_courses_serializer.data
        }

        return Response(response_data)
