from django.urls import path
from .views import SurveysView, SurveyResponsesView

urlpatterns = [
    path('surveys/', SurveysView.as_view(), name='surveys'),
    path('survey-responses/', SurveyResponsesView.as_view(), name='survey-responses'),
]
