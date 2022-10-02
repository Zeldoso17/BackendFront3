from django.urls import path
from . import views

urlpatterns = [
    path('getPlaces/<str:query>', views.getPlaces.as_view())
]
