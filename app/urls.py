from django.urls import path

app_name = 'app'

import app.views as app

urlpatterns = [
    path("", app.index, name="index")
]
