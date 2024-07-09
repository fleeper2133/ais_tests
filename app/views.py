from django.http import HttpRequest
from inertia import render

def index(request):
    props = {
        "title": "title"
    }
    return render(request, "App", props=props)