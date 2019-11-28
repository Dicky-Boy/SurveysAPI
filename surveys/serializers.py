from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Survey, SurveyResponse

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'survey_name', 'available_places', 'user_id')

class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ('id', 'survey_id', 'user_id', 'created_at')
