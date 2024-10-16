from django.http import HttpRequest
from inertia import render


def index(request):
    return render(request, "Index", props={"pageName": "Index"})

def lk(request):
    return render(request, "Lk", props={"pageName": "Lk"})

def proposal(request):
    return render(request, "Proposal", props={"pageName": "Proposal"})

def notif(request):
    return render(request, "Notif", props={"pageName": "Notif"})