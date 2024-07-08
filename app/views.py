from django.http import HttpRequest
from inertia import render

def index(request):
    props = {
        
    }
    return render(request, "CourseChoosing", props=props)