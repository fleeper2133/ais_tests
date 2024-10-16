from django.urls import path
import landing.views as landing

app_name = "landing"


urlpatterns = [
    path("", landing.index, name="index"),
    path("lk/", landing.lk, name="lk"),
    path("proposals/", landing.proposal, name="proposal"),
    path("notifications/", landing.notif, name="notif"),]