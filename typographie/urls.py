from django.urls import path

from .views import TypographieFilter

urlpatterns = [
    path("typographie/", TypographieFilter.as_view(), name="typographie"),
]
