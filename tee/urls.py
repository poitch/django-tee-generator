from django.urls import path

from tee import views

app_name = "tee"
urlpatterns = [
    path("create/<str:shape>/<str:color>/<str:text_color>/<str:font>/<path:sentence>/<str:filename>.png", views.GeneratorView.as_view(), name="generator"),
]